"""Run the audit agent (Claude Code, headless) on a read-only snapshot of the submission.

The agent gets only: the numbered instructions, the script-checked facts, an inventory,
a copy of the submission without secrets or binaries, and the extracted text of office
files. Scores and professor comments never reach it. It has Read, Grep and Glob only.
"""

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from string import Template

from .extract import EXTRACTORS, ExtractError, extract_folder, iter_files

PROMPT_VERSION = "v1"
PACKAGE = Path(__file__).parent
MAX_FILE_BYTES = 2 * 1024 * 1024
TIMEOUT_SECONDS = 1800
TOOLS = "Read,Grep,Glob"
BINARY_SUFFIXES = {
    ".joblib", ".pkl", ".pickle", ".npz", ".npy", ".h5", ".hdf5", ".pt", ".pth", ".onnx", ".bin",
    ".zip", ".tar", ".gz", ".7z", ".rar", ".exe", ".dmg", ".parquet", ".feather", ".db", ".sqlite",
    ".xlsx", ".xls", ".doc", ".ppt", ".mp4", ".mov", ".mp3", ".wav",
}
SECRET_SUFFIXES = {".env", ".pem", ".key", ".p12", ".pfx"}
SECRET_NAMES = {"id_rsa", "id_ed25519", "credentials.json", "secrets.json", "token.json"}


class AuditError(Exception):
    pass


def load_schema():
    return json.loads((PACKAGE / "schema.json").read_text(encoding="utf-8"))


def render_prompt(meta, as_of_local):
    template = Template((PACKAGE / "prompts" / f"{PROMPT_VERSION}.md").read_text(encoding="utf-8"))
    return template.substitute(nombre=meta["name"], fecha_revision=as_of_local)


def build_command(prompt, schema, model):
    return [
        "claude", "-p", prompt,
        "--model", model,
        "--output-format", "json",
        "--json-schema", json.dumps(schema),
        "--tools", TOOLS,
        "--permission-mode", "dontAsk",
        "--strict-mcp-config",
        "--no-session-persistence",
        # Skip user settings and the user's global CLAUDE.md, so the audit depends only on the prompt.
        "--setting-sources", "project",
    ]


def folder_digest(folder):
    folder = Path(folder)
    if not folder.is_dir():
        return "missing"
    digest = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder)
        if ".git" in relative.parts or not path.is_file():
            continue
        digest.update(relative.as_posix().encode())
        digest.update(str(path.stat().st_mtime_ns).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def build_instructions(meta):
    lines = [{"id": line["id"], "text": line["text"]} for line in meta["lines"]]
    for item in meta.get("linked_files") or []:
        path = Path(item["path"]) if item.get("path") else None
        extractor = EXTRACTORS.get(path.suffix.lower()) if path else None
        if extractor is None:
            continue
        try:
            text = extractor(path)
        except ExtractError:
            continue
        for content in [f"# Archivo adjunto: {item['name']}", *text.splitlines()]:
            lines.append({"id": f"L{len(lines) + 1:03d}", "text": content})
    return lines


def _is_secret(name):
    return name.startswith(".") or Path(name).suffix.lower() in SECRET_SUFFIXES or name in SECRET_NAMES


def _format_size(size):
    for unit in ("B", "KB", "MB"):
        if size < 1024 or unit == "MB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024


def _git_ignored(folder, names):
    # Files git ignores are never part of a submitted repository, so they are not audited.
    try:
        proc = subprocess.run(["git", "--no-optional-locks", "-C", str(folder), "check-ignore", "--stdin"],
                              input="\n".join(names), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return set()
    return set(proc.stdout.splitlines()) if proc.returncode == 0 else set()


def _snapshot(folder, agent, text_manifest, max_file_bytes):
    texts = {entry["source"]: entry for entry in text_manifest}
    files = list(iter_files(folder)) if folder.is_dir() else []
    ignored = _git_ignored(folder, [relative.as_posix() for _, relative in files]) if files else set()
    rows, omitted = [], 0
    for path, relative in files:
        name = relative.as_posix()
        if _is_secret(path.name):
            omitted += 1
            continue
        size = path.stat().st_size
        if name in ignored:
            status = "not copied: ignored by git"
        elif name in texts:
            entry = texts[name]
            status = f"text in texto/{entry['text']}" if "text" in entry else f"text extraction failed: {entry['error']}"
        elif path.suffix.lower() in BINARY_SUFFIXES:
            status = "not copied: binary"
        elif size > max_file_bytes:
            status = "not copied: large"
        else:
            target = agent / "entrega" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            status = "copied to entrega/"
        rows.append(f"{name} | {_format_size(size)} | {status}")
    header = ["Submission files (path | size | status)"] if folder.is_dir() else [f"The folder {folder} does not exist."]
    footer = [f"Omitted for safety (hidden files or secrets): {omitted}"] if omitted else []
    return "\n".join(header + rows + footer) + "\n"


def prepare_agent_dir(meta, checks, folder, work_root, max_file_bytes=MAX_FILE_BYTES):
    folder, work_root = Path(folder), Path(work_root)
    agent = work_root / str(meta["assignment_id"]) / "agent"
    if agent.exists():
        shutil.rmtree(agent)  # our own generated cache, rebuilt on every run
    (agent / "entrega").mkdir(parents=True)

    lines = build_instructions(meta)
    header = f"# {meta['name']}\nDue: {meta.get('due_local') or 'no due date'}  Points in the final grade: {meta.get('points_possible')}\n\n"
    (agent / "instrucciones.md").write_text(header + "\n".join(f"{line['id']} {line['text']}" for line in lines) + "\n", encoding="utf-8")
    (agent / "hechos.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = extract_folder(folder, agent / "texto") if folder.is_dir() else []
    (agent / "inventario.txt").write_text(_snapshot(folder, agent, manifest, max_file_bytes), encoding="utf-8")
    return agent


def run_claude(command, cwd):
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except FileNotFoundError:
        raise AuditError("the claude command is not installed or not on PATH") from None
    except subprocess.TimeoutExpired:
        raise AuditError(f"the audit took longer than {TIMEOUT_SECONDS // 60} minutes") from None
    if not proc.stdout.strip():
        raise AuditError(f"claude exited with code {proc.returncode}: {proc.stderr.strip()[-300:]}")
    return proc.stdout


def _findings(raw):
    try:
        envelope = json.loads(raw)
    except json.JSONDecodeError:
        raise AuditError(f"claude did not return JSON: {raw[:200]}") from None
    if envelope.get("is_error"):
        raise AuditError(f"claude reported an error: {envelope.get('result')}")
    findings = envelope.get("structured_output")
    if findings is None:
        try:
            findings = json.loads(envelope.get("result") or "")
        except json.JSONDecodeError:
            raise AuditError("claude returned no structured output") from None
    return envelope, findings


def run_audit(meta, checks, folder, work_root, model, runner=None):
    folder, work_root = Path(folder), Path(work_root)
    before = folder_digest(folder)
    agent = prepare_agent_dir(meta, checks, folder, work_root)
    prompt = render_prompt(meta, checks.get("as_of_local") or "ahora")
    raw = (runner or run_claude)(build_command(prompt, load_schema(), model), agent)
    after = folder_digest(folder)
    envelope, findings = _findings(raw)

    audit = {
        "assignment_id": meta["assignment_id"],
        "name": meta["name"],
        "prompt_version": PROMPT_VERSION,
        "model": model,
        "as_of": checks.get("as_of"),
        "as_of_local": checks.get("as_of_local"),
        "folder": str(folder),
        "folder_digest_before": before,
        "folder_digest_after": after,
        "folder_unchanged": before == after,
        "run": {
            "models": sorted(envelope.get("modelUsage") or {}),
            **{key: envelope.get(key) for key in ("num_turns", "duration_ms", "total_cost_usd", "usage", "permission_denials")},
        },
        "lines": build_instructions(meta),
        "findings": findings,
    }
    out = work_root / str(meta["assignment_id"]) / "audit.json"
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit
