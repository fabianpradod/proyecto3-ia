import json
import subprocess
import zipfile
from pathlib import Path

import pytest

from preflight.audit import (
    PROMPT_VERSION, AuditError, build_command, build_instructions, folder_digest, load_schema,
    prepare_agent_dir, render_prompt, run_audit,
)

TZ = "America/Guatemala"
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def make_meta(tmp_path, linked=()):
    return {
        "assignment_id": 959073, "name": "Proyecto 3", "timezone": TZ, "due_local": "2026-11-18 23:59",
        "points_possible": 13.5,
        "lines": [{"id": "L001", "text": "# Proyecto 3"}, {"id": "L002", "text": "Entregar un README | 10"}],
        "linked_files": list(linked),
        "submission": {"score": 12.25, "comments": [{"text": "falta el codo"}]},
    }


def make_docx(path, text):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", f"<w:document {W}><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>")
    return path


def make_submission(tmp_path):
    folder = tmp_path / "entrega"
    (folder / "notebooks").mkdir(parents=True)
    (folder / ".git").mkdir()
    (folder / ".git" / "config").write_text("[core]")
    (folder / ".env").write_text("CANVAS_TOKEN=secret-canary")
    (folder / "keys.env").write_text("API_KEY=secret-canary")
    (folder / "README.md").write_text("# Pre-flight")
    (folder / "notebooks" / "a.ipynb").write_text("{}")
    (folder / "modelo.joblib").write_bytes(b"\0" * 10)
    (folder / "big.csv").write_bytes(b"x" * 3000)
    make_docx(folder / "informe.docx", "Analisis de errores")
    return folder


def fake_envelope(structured, is_error=False, result="done"):
    return json.dumps({
        "type": "result", "is_error": is_error, "result": result, "structured_output": structured,
        "num_turns": 7, "duration_ms": 61000, "total_cost_usd": 0.42,
        "usage": {"input_tokens": 1000, "output_tokens": 500}, "permission_denials": [],
        "modelUsage": {"claude-opus-5": {"inputTokens": 1000}},
    })


FINDINGS = {
    "resumen": "Faltan 10 puntos.",
    "criterios": [{
        "criterio": "README", "puntos": 10, "estado": "cumple", "puntos_en_riesgo": 0,
        "citas": [{"linea": "L002", "texto": "Entregar un README"}],
        "evidencia": [{"archivo": "README.md", "detalle": "existe"}],
        "observacion": "Hay README.",
    }],
    "fechas": [],
    "no_verificable": [],
}


def test_snapshot_leaves_out_secrets_hidden_folders_binaries_and_large_files(tmp_path):
    folder = make_submission(tmp_path)
    agent = prepare_agent_dir(make_meta(tmp_path), {"results": []}, folder, tmp_path / "work", max_file_bytes=2000)
    copied = sorted(p.relative_to(agent / "entrega").as_posix() for p in (agent / "entrega").rglob("*") if p.is_file())
    assert copied == ["README.md", "notebooks/a.ipynb"]
    inventory = (agent / "inventario.txt").read_text(encoding="utf-8")
    assert "big.csv" in inventory and "modelo.joblib" in inventory and "informe.docx" in inventory
    assert "keys.env" not in inventory and ".env" not in inventory.split()
    assert "secret-canary" not in "".join(p.read_text(errors="ignore") for p in agent.rglob("*") if p.is_file())


def test_files_ignored_by_git_are_listed_but_not_copied(tmp_path):
    folder = make_submission(tmp_path)
    (folder / ".gitignore").write_text("work/\n")
    (folder / "work").mkdir()
    (folder / "work" / "meta.json").write_text('{"score": 12.25}')
    subprocess.run(["git", "init", "-q", str(folder)], check=True)
    agent = prepare_agent_dir(make_meta(tmp_path), {"results": []}, folder, tmp_path / "work_root")
    assert not (agent / "entrega" / "work").exists()
    assert "work/meta.json | 16 B | not copied: ignored by git" in (agent / "inventario.txt").read_text(encoding="utf-8")


def test_office_files_reach_the_agent_as_text(tmp_path):
    agent = prepare_agent_dir(make_meta(tmp_path), {"results": []}, make_submission(tmp_path), tmp_path / "work")
    assert (agent / "texto" / "informe.docx.txt").read_text(encoding="utf-8") == "Analisis de errores\n"


def test_agent_dir_never_holds_scores_or_comments(tmp_path):
    agent = prepare_agent_dir(make_meta(tmp_path), {"results": [{"check": "deadline"}]}, make_submission(tmp_path), tmp_path / "work")
    everything = "".join(p.read_text(errors="ignore") for p in agent.rglob("*") if p.is_file())
    assert "12.25" not in everything and "codo" not in everything
    assert not (agent / "meta.json").exists()


def test_attached_files_continue_the_line_numbers(tmp_path):
    attached = make_docx(tmp_path / "plantilla.docx", "Llenar una fila por grupo")
    meta = make_meta(tmp_path, linked=[{"id": 1, "name": "plantilla.docx", "path": str(attached)}])
    lines = build_instructions(meta)
    assert [line["id"] for line in lines] == ["L001", "L002", "L003", "L004"]
    assert lines[2]["text"] == "# Archivo adjunto: plantilla.docx"
    assert lines[3]["text"] == "Llenar una fila por grupo"


def test_command_limits_tools_and_drops_mcp_servers():
    command = build_command("prompt", load_schema(), "opus")
    assert command[:3] == ["claude", "-p", "prompt"]
    assert command[command.index("--tools") + 1] == "Read,Grep,Glob"
    assert command[command.index("--permission-mode") + 1] == "dontAsk"
    assert "--strict-mcp-config" in command and "--no-session-persistence" in command
    # Without this, the user's global CLAUDE.md reaches the auditor (verified with a probe).
    assert command[command.index("--setting-sources") + 1] == "project"
    assert json.loads(command[command.index("--json-schema") + 1]) == load_schema()


def test_schema_requires_a_citation_per_criterion():
    citas = load_schema()["properties"]["criterios"]["items"]["properties"]["citas"]
    assert citas["minItems"] == 1


def test_prompt_is_fully_rendered(tmp_path):
    prompt = render_prompt(make_meta(tmp_path), "2026-11-16 21:00")
    assert "{" not in prompt and "2026-11-16 21:00" in prompt


def test_run_audit_saves_findings_and_proves_the_folder_did_not_change(tmp_path):
    folder = make_submission(tmp_path)
    calls = []

    def runner(command, cwd):
        calls.append((command, cwd))
        assert (Path(cwd) / "instrucciones.md").exists()
        return fake_envelope(FINDINGS)

    audit = run_audit(make_meta(tmp_path), {"as_of_local": "2026-11-16 21:00", "results": []}, folder,
                      tmp_path / "work", "opus", runner=runner)
    assert audit["findings"] == FINDINGS
    assert audit["folder_unchanged"] is True
    assert audit["prompt_version"] == PROMPT_VERSION and audit["model"] == "opus"
    # The alias resolves to whatever the account offers; keep the id that actually ran.
    assert audit["run"]["models"] == ["claude-opus-5"]
    assert audit["run"]["num_turns"] == 7
    assert calls[0][1] == tmp_path / "work" / "959073" / "agent"
    saved = json.loads((tmp_path / "work" / "959073" / "audit.json").read_text(encoding="utf-8"))
    assert saved["findings"] == FINDINGS
    assert [line["id"] for line in saved["lines"]] == ["L001", "L002"]


def test_a_changed_folder_is_reported(tmp_path):
    folder = make_submission(tmp_path)

    def runner(command, cwd):
        (folder / "README.md").write_text("changed during the run")
        return fake_envelope(FINDINGS)

    audit = run_audit(make_meta(tmp_path), {"results": []}, folder, tmp_path / "work", "opus", runner=runner)
    assert audit["folder_unchanged"] is False


def test_cli_error_becomes_an_audit_error(tmp_path):
    def runner(command, cwd):
        return fake_envelope(None, is_error=True, result="Failed to authenticate")

    with pytest.raises(AuditError, match="Failed to authenticate"):
        run_audit(make_meta(tmp_path), {"results": []}, make_submission(tmp_path), tmp_path / "work", "opus", runner=runner)


def test_folder_digest_changes_with_content(tmp_path):
    folder = make_submission(tmp_path)
    before = folder_digest(folder)
    (folder / "README.md").write_text("otro")
    assert folder_digest(folder) != before
