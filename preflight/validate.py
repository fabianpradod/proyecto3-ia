"""Check the agent's findings against the instructions and the real folder.

The agent's output is not trusted: every quote must be in its cited line word for word,
every evidence file must exist, and the points must add up. Problems are reported, never
fixed, so a bad finding stays visible in the report.
"""

import re
import unicodedata
from pathlib import Path

from .spec import find_point_rows

# Files of the agent's own folder that it may cite as evidence of absence.
AGENT_FILES = {"inventario.txt", "hechos.json", "instrucciones.md"}
NEEDS_EVIDENCE = {"cumple", "parcial"}


def _norm(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text or "")).strip()


def _issue(where, rule, detail):
    return {"where": where, "rule": rule, "detail": detail}


def _check_quote(lines, quote, where, issues):
    line = lines.get(quote.get("linea"))
    if line is None:
        issues.append(_issue(where, "unknown_line", f"{quote.get('linea')} is not a line of the instructions"))
        return False
    text = _norm(quote.get("texto"))
    if not text or text not in _norm(line):
        issues.append(_issue(where, "quote_not_verbatim", f"{quote.get('texto')!r} is not in {quote['linea']}"))
        return False
    return True


def _evidence_exists(folder, path):
    path = path.strip().rstrip("/")
    if path in AGENT_FILES:
        return True
    if path.startswith("entrega/"):
        path = path[len("entrega/"):]
    elif path.startswith("texto/"):
        path = path[len("texto/"):].removesuffix(".txt")
    return bool(path) and (folder / path).exists()


def _check_points(item, where, rubric, issues):
    points, risk, status = item.get("puntos"), item.get("puntos_en_riesgo"), item.get("estado")
    ok = True
    if points is not None and risk is not None:
        if risk < 0 or risk > points:
            issues.append(_issue(where, "risk_over_points", f"{risk:g} at risk out of {points:g} points"))
            ok = False
        elif (status == "cumple" and risk != 0) or (status == "falta" and risk != points):
            issues.append(_issue(where, "risk_inconsistent", f"status {status} with {risk:g} of {points:g} points at risk"))
            ok = False
    cited_rows = [rubric[quote.get("linea")] for quote in item.get("citas") or [] if quote.get("linea") in rubric]
    if points is not None and cited_rows and points not in cited_rows:
        issues.append(_issue(where, "points_not_in_rubric", f"{points:g} points, but the cited rubric rows say {cited_rows}"))
        ok = False
    return ok


def validate(audit):
    lines = {line["id"]: line["text"] for line in audit["lines"]}
    rows = find_point_rows([(line["id"], line["text"]) for line in audit["lines"]])
    rubric = {row["line"]: row["points"] for row in rows if not row["is_total"]}
    folder = Path(audit["folder"])
    findings = audit["findings"]
    issues, criteria_valid = [], []
    counts = {"citations": 0, "evidence": 0, "criteria": len(findings["criterios"])}

    if audit.get("folder_unchanged") is False:
        issues.append(_issue("folder", "folder_changed", "the audited folder changed during the run"))

    for index, item in enumerate(findings["criterios"]):
        where = f"criterios[{index}]"
        ok = True
        for number, quote in enumerate(item.get("citas") or []):
            counts["citations"] += 1
            ok &= _check_quote(lines, quote, f"{where}.citas[{number}]", issues)
        for number, evidence in enumerate(item.get("evidencia") or []):
            counts["evidence"] += 1
            if item.get("estado") in NEEDS_EVIDENCE and not _evidence_exists(folder, evidence.get("archivo", "")):
                issues.append(_issue(f"{where}.evidencia[{number}]", "evidence_not_found", f"{evidence.get('archivo')} is not in {folder}"))
                ok = False
        ok &= _check_points(item, where, rubric, issues)
        criteria_valid.append(bool(ok))

    for number, quote in enumerate(findings.get("fechas") or []):
        counts["citations"] += 1
        _check_quote(lines, quote, f"fechas[{number}]", issues)

    if rubric:
        stated = sum(rubric.values())
        covered = sum(item["puntos"] for item in findings["criterios"] if item.get("puntos") is not None)
        if covered < stated - 1e-9:
            issues.append(_issue("criterios", "rubric_not_covered", f"criteria cover {covered:g} of {stated:g} rubric points"))

    return {"valid": not issues, "issues": issues, "criteria_valid": criteria_valid, "counts": counts}
