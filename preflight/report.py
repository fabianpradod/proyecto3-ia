"""Render the audit, the script checks and the validation as a Spanish Markdown report."""

from pathlib import Path

import yaml

TEXT = yaml.safe_load((Path(__file__).with_name("report_es.yaml")).read_text(encoding="utf-8"))
LEVEL_ORDER = {"problem": 0, "warning": 1, "ok": 2, "info": 3}


def _num(value):
    return f"{value:g}" if isinstance(value, (int, float)) else str(value)


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def _fact(item):
    check, status, data = item["check"], item["status"], item.get("data") or {}
    values = {key: _num(value) for key, value in data.items() if not isinstance(value, (list, dict))}
    key = f"{check}.{status}"
    if check == "git":
        key = "git.repo" if data.get("is_repo") else "git.norepo"
    elif check == "git_unpushed" and status == "warning" and data.get("upstream") is None:
        key = "git_unpushed.noupstream"
    elif check == "text_dates":
        values["passed"] = ", ".join(f"{m['date']} ({m['line']})" for m in data.get("passed") or [])
        values["count"] = len(data.get("mentions") or [])
    elif check == "rubric":
        values["count"] = len(data.get("criteria") or [])
    elif check == "sources":
        values["unread"] = ", ".join(data.get("unread_files") or [])
        values["count"] = len(data.get("external_links") or [])
    elif check == "file_types":
        values["found"] = ", ".join(data.get("found") or [])
        values["allowed"] = ", ".join(data.get("allowed") or [])
    elif check == "git_after_due":
        commits = data.get("commits") or []
        values["count"] = len(commits)
        values["commits"] = "; ".join(f"{c['hash']} ({c['local']}) {c['subject']}" for c in commits)
    template = TEXT["hechos"].get(key, item.get("summary", ""))
    return f"- {TEXT['niveles'][status]}: {template.format(**values)}"


def _risk_text(item):
    if item.get("puntos") is None:
        return "-"
    risk = item.get("puntos_en_riesgo")
    return f"{_num(risk) if risk is not None else '?'} de {_num(item['puntos'])}"


def render_report(audit, checks):
    t = TEXT["textos"]
    findings, validation = audit["findings"], audit.get("validation") or {}
    criteria = findings["criterios"]
    criteria_valid = validation.get("criteria_valid") or [True] * len(criteria)
    models = ", ".join(audit.get("run", {}).get("models") or []) or audit.get("model", "")
    folder_note = t["carpeta_igual"] if audit.get("folder_unchanged", True) else t["carpeta_cambio"]

    out = [f"# Pre-flight: {audit['name']}", ""]
    out += [t["revision"].format(as_of=audit.get("as_of_local") or checks.get("as_of_local")),
            t["modelo"].format(model=models, prompt=audit.get("prompt_version"), carpeta=folder_note), ""]

    with_points = [c for c in criteria if c.get("puntos") is not None]
    out += [f"## {t['resumen']}", ""]
    if with_points:
        risk = sum(c.get("puntos_en_riesgo") or 0 for c in with_points)
        out += [t["puntos"].format(risk=_num(risk), total=_num(sum(c["puntos"] for c in with_points))), ""]
    else:
        out += [t["sin_puntos"], ""]
    out += [findings["resumen"], ""]

    out += [f"## {t['criterios']}", "", t["tabla"], "|---|---|---|---|"]
    for item in criteria:
        line = item["citas"][0]["linea"] if item.get("citas") else "-"
        out.append(f"| {_cell(item['criterio'])} | {TEXT['estados'][item['estado']]} | {_risk_text(item)} | {line} |")
    out.append("")

    for number, (item, valid) in enumerate(zip(criteria, criteria_valid), start=1):
        out += [f"### {number}. {item['criterio']}", ""]
        risk = _risk_text(item)
        out += [t["estado_linea"].format(estado=TEXT["estados"][item["estado"]], riesgo=risk if risk != "-" else "sin puntos"), ""]
        out += [item["observacion"], ""]
        out += [t["segun"]] + [f'- {q["linea"]}: "{q["texto"]}"' for q in item.get("citas") or []] + [""]
        evidence = item.get("evidencia") or []
        out += [t["evidencia"]] + ([f"- `{e['archivo']}`: {e['detalle']}" for e in evidence] or [f"- {t['sin_evidencia']}"]) + [""]
        if not valid:
            out += [t["aviso"], ""]

    if findings.get("fechas"):
        out += [f"## {t['fechas']}", "", t["tabla_fechas"], "|---|---|---|"]
        out += [f"| {_cell(d['entregable'])} | {_cell(d['fecha'])} | {d['linea']} |" for d in findings["fechas"]] + [""]

    facts = sorted(checks.get("results") or [], key=lambda item: LEVEL_ORDER.get(item["status"], 9))
    if facts:
        out += [f"## {t['hechos']}", ""] + [_fact(item) for item in facts] + [""]

    if findings.get("no_verificable"):
        out += [f"## {t['no_verificable']}", ""] + [f"- {item}" for item in findings["no_verificable"]] + [""]

    out += [f"## {t['validacion']}", ""]
    counts = validation.get("counts") or {}
    if validation.get("valid", True):
        out += [t["valida"].format(citations=counts.get("citations", 0), evidence=counts.get("evidence", 0)), ""]
    else:
        count = len(validation["issues"])
        out += [(t["invalida_uno"] if count == 1 else t["invalida"].format(count=count)), ""]
        out += [f"- {TEXT['validacion'].get(i['rule'], i['rule'])}: `{i['where']}` ({i['detail']})" for i in validation["issues"]] + [""]

    out += ["---", "", t["pie"], ""]
    return "\n".join(out)
