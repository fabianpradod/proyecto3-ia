"""Run the pre-flight on real cases and score it against expectations written beforehand."""

import json
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
NOT_MET = {"parcial", "falta"}


def _plain(text):
    decomposed = unicodedata.normalize("NFD", text or "")
    return "".join(c for c in decomposed if not unicodedata.combining(c)).lower()


def _detected(criteria, lines, words):
    for item in criteria:
        if item["estado"] not in NOT_MET:
            continue
        cited = {quote["linea"] for quote in item.get("citas") or []}
        text = _plain(" ".join([item["criterio"], item["observacion"], *(e["detalle"] for e in item.get("evidencia") or [])]))
        if cited & set(lines) and any(_plain(word) in text for word in words):
            return True
    return False


def score_case(case, audit, checks):
    expected = case.get("esperado") or {}
    criteria = audit["findings"]["criterios"]
    statuses = {item["check"]: item["status"] for item in checks.get("results") or []}
    results = []
    for check, status in (expected.get("hechos") or {}).items():
        results.append({"esperado": f"hecho {check} = {status}", "ok": statuses.get(check) == status, "obtenido": statuses.get(check)})
    if expected.get("sin_cumple"):
        results.append({"esperado": "ningun criterio en cumple", "ok": not any(c["estado"] == "cumple" for c in criteria)})
    if expected.get("sin_falta"):
        results.append({"esperado": "ningun criterio en falta", "ok": not any(c["estado"] == "falta" for c in criteria)})
    for item in expected.get("detecta") or []:
        label = f"detecta {'/'.join(item['lineas'])} ({'/'.join(item['palabras'])})"
        results.append({"esperado": label, "ok": _detected(criteria, item["lineas"], item["palabras"])})
    found_dates = {date["linea"] for date in audit["findings"].get("fechas") or []}
    for line in expected.get("fechas") or []:
        results.append({"esperado": f"fecha en {line}", "ok": line in found_dates})
    return results


def compare_runs(audits):
    risk = [sum(c.get("puntos_en_riesgo") or 0 for c in a["findings"]["criterios"] if c.get("puntos") is not None) for a in audits]
    by_name = {}
    for audit in audits:
        for item in audit["findings"]["criterios"]:
            by_name.setdefault(item["criterio"], []).append(item["estado"])
    changed = [{"criterio": name, "estados": states} for name, states in by_name.items()
               if len(states) == len(audits) and len(set(states)) > 1]
    return {"risk": risk, "changed": changed}


def _expand(path, base):
    path = Path(path).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def _run_one(cases_file, course, case, run, work_base, model):
    work = work_base / case["id"] / f"run{run}"
    export = _expand(case.get("exportacion") or course, cases_file.parent)
    python = [sys.executable, "-m", "preflight"]
    import_cmd = python + ["import", str(export), "--out", str(work)]
    if not case.get("exportacion"):
        import_cmd += ["--assignment", str(case["tarea"])]
    folder = _expand(case["carpeta"], REPO)
    audit_cmd = python + ["audit", str(case["tarea"]), str(folder), "--as-of", case.get("momento", "now"), "--model", model, "--out", str(work)]
    log = []
    for command in (import_cmd, audit_cmd):
        proc = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
        log.append(proc.stdout + proc.stderr)
        if proc.returncode != 0:
            return {"case": case["id"], "run": run, "work": work, "error": log[-1].strip()[-400:]}
    return {"case": case["id"], "run": run, "work": work, "log": "".join(log)}


def run_cases(cases_file, work_base, runs=2, parallel=3, model="opus", only=None):
    cases_file = Path(cases_file).resolve()
    spec = yaml.safe_load(cases_file.read_text(encoding="utf-8"))
    cases = [case for case in spec["casos"] if not only or case["id"] in only]
    jobs = [(case, run) for run in range(1, runs + 1) for case in cases]
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        done = list(pool.map(lambda job: _run_one(cases_file, spec["curso"], job[0], job[1], Path(work_base), model), jobs))
    return cases, done


def load_run(result, assignment_id):
    base = Path(result["work"]) / str(assignment_id)
    audit = json.loads((base / "audit.json").read_text(encoding="utf-8"))
    checks = json.loads((base / "checks.json").read_text(encoding="utf-8"))
    report = (base / "reporte.md").read_text(encoding="utf-8")
    return audit, checks, report


def _sanitize(text):
    return text.replace(str(Path.home()), "~")


def write_results(cases, done, out_dir):
    from .report import TEXT  # the Spanish labels live with the report text

    t = TEXT["casos"]
    out_dir = Path(out_dir)
    (out_dir / "resultados").mkdir(parents=True, exist_ok=True)
    rows, sections, models, prompts, runs = [], [], set(), set(), 0
    for case in cases:
        results = sorted((r for r in done if r["case"] == case["id"]), key=lambda r: r["run"])
        runs = max(runs, len(results))
        audits, scores, links = [], [], []
        for result in results:
            if "error" in result:
                rows.append(f"| {case['id']} | {result['run']} | {t['error'].format(error=result['error'][:80])} | | | | |")
                continue
            audit, checks, report = load_run(result, case["tarea"])
            name = f"resultados/{case['id']}-run{result['run']}.md"
            (out_dir / name).write_text(_sanitize(report), encoding="utf-8")
            links.append(f"[{t['corrida']} {result['run']}]({name})")
            score = score_case(case, audit, checks)
            audits.append(audit)
            scores.append(score)
            models.update(audit["run"].get("models") or [audit["model"]])
            prompts.add(audit["prompt_version"])
            criteria = audit["findings"]["criterios"]
            count = {s: sum(c["estado"] == s for c in criteria) for s in ("cumple", "parcial", "falta", "no_verificable")}
            with_points = [c for c in criteria if c.get("puntos") is not None]
            risk = f"{sum(c.get('puntos_en_riesgo') or 0 for c in with_points):g} / {sum(c['puntos'] for c in with_points):g}" if with_points else "-"
            validation = audit["validation"]
            valid = t["valida"] if validation["valid"] else t["invalida"].format(count=len(validation["issues"]))
            seconds = (audit["run"].get("duration_ms") or 0) / 1000
            rows.append(f"| {case['id']} | {result['run']} | {sum(s['ok'] for s in score)} / {len(score)} | {risk} | "
                        f"{count['cumple']} / {count['parcial']} / {count['falta']} / {count['no_verificable']} | {valid} | {seconds:.0f} s |")

        section = [f"## {case['nombre']}", "", f"{t['realidad']} {case['realidad']}", ""]
        if scores:
            header = f"| {t['expectativa']} | " + " | ".join(f"{t['corrida']} {r['run']}" for r in results if "error" not in r) + " |"
            section += [header, "|---|" + "---|" * len(scores)]
            for index, item in enumerate(scores[0]):
                marks = " | ".join(t["marca_si"] if score[index]["ok"] else t["marca_no"] for score in scores)
                section.append(f"| {item['esperado']} | {marks} |")
            section.append("")
        if len(audits) > 1:
            diff = compare_runs(audits)
            section.append(t["variacion"].format(risk=", ".join(f"{r:g}" for r in diff["risk"])))
            changed = "; ".join(f"{c['criterio']} ({', '.join(c['estados'])})" for c in diff["changed"])
            section += [t["cambios"].format(changed=changed) if changed else t["sin_cambios"], ""]
        if links:
            section += [f"{t['reportes']} " + ", ".join(links), ""]
        sections += section

    header = [f"# {t['titulo']}", "",
              t["intro"].format(prompt=", ".join(sorted(prompts)), model=", ".join(sorted(models)), runs=runs), "",
              t["tabla"], "|---|---|---|---|---|---|---|"]
    path = out_dir / "resultados.md"
    path.write_text("\n".join(header + rows + [""] + sections), encoding="utf-8")
    return path
