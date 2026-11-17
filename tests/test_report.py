from preflight.report import render_report

SPANISH = set("\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da\u00f1\u00d1\u00fc\u00dc\u00bf\u00a1")


def make_audit(valid=True):
    criteria = [
        {
            "criterio": "README | entrega", "puntos": 10, "estado": "falta", "puntos_en_riesgo": 10,
            "citas": [{"linea": "L002", "texto": "Entregar un README"}],
            "evidencia": [{"archivo": "README.md", "detalle": "no existe"}],
            "observacion": "No hay README.",
        },
        {
            "criterio": "Presentacion", "puntos": None, "estado": "no_verificable", "puntos_en_riesgo": None,
            "citas": [{"linea": "L003", "texto": "Presentar en clase"}],
            "evidencia": [], "observacion": "Es oral.",
        },
        {
            "criterio": "Notebook", "puntos": 5, "estado": "cumple", "puntos_en_riesgo": 0,
            "citas": [{"linea": "L004", "texto": "Notebook"}],
            "evidencia": [{"archivo": "a.ipynb", "detalle": "corre"}], "observacion": "Cumple.",
        },
    ]
    issues = [] if valid else [{"where": "criterios[0].citas[0]", "rule": "quote_not_verbatim", "detail": "'x' is not in L002"}]
    return {
        "name": "Proyecto 3", "model": "opus", "prompt_version": "v1", "as_of_local": "2026-11-16 21:37",
        "folder_unchanged": True,
        "run": {"models": ["claude-opus-5"], "num_turns": 13, "duration_ms": 157000},
        "findings": {
            "resumen": "Faltan 10 puntos.",
            "criterios": criteria,
            "fechas": [{"entregable": "Exploracion", "fecha": "Nov 11, 2026", "linea": "L031", "texto": "Nov 11, 2026"}],
            "no_verificable": ["La demo en vivo."],
        },
        "validation": {"valid": valid, "issues": issues, "criteria_valid": [valid, True, True],
                       "counts": {"citations": 4, "evidence": 2, "criteria": 3}},
    }


CHECKS = {
    "as_of_local": "2026-11-16 21:37",
    "results": [
        {"check": "deadline", "status": "warning", "summary": "", "data": {"due_local": "2026-11-18 23:59", "hours_left": 5.5}},
        {"check": "submission", "status": "warning", "summary": "", "data": {}},
        {"check": "text_dates", "status": "warning", "summary": "", "data": {"mentions": [], "passed": [{"line": "L031", "date": "2026-11-11", "text": "Nov 11, 2026"}]}},
        {"check": "folder", "status": "problem", "summary": "", "data": {}},
        {"check": "git", "status": "info", "summary": "", "data": {"is_repo": True, "branch": "fabian/preflight", "default": "origin/main", "remote": "x"}},
        {"check": "git_branch", "status": "warning", "summary": "", "data": {"branch": "fabian/preflight", "default": "origin/main", "not_in_default": 5}},
        {"check": "git_unpushed", "status": "warning", "summary": "", "data": {"upstream": None}},
        {"check": "git_after_due", "status": "warning", "summary": "", "data": {"commits": [{"hash": "f0f375f", "local": "2026-10-26 19:49", "subject": "docs: ppt"}]}},
    ],
}


def test_header_and_total_points_at_risk():
    report = render_report(make_audit(), CHECKS)
    assert report.startswith("# Pre-flight: Proyecto 3\n")
    assert "claude-opus-5" in report and "Prompt: v1" in report
    assert "**Puntos en riesgo: 10 de 15.**" in report


def test_criteria_table_escapes_pipes_and_shows_lines():
    report = render_report(make_audit(), CHECKS)
    assert "| README \\| entrega | Falta | 10 de 10 | L002 |" in report
    assert "| Presentacion | No verificable | - | L003 |" in report


def test_each_criterion_quotes_the_instructions_and_lists_evidence():
    report = render_report(make_audit(), CHECKS)
    assert '- L002: "Entregar un README"' in report
    assert "- `README.md`: no existe" in report


def test_script_facts_are_in_spanish_and_problems_come_first():
    report = render_report(make_audit(), CHECKS)
    facts = report.split("## Hechos revisados por script")[1].split("##")[0]
    assert facts.strip().splitlines()[0].startswith("- Problema:")
    assert "Quedan 5.5 horas" in facts
    assert "5 commits de la rama fabian/preflight no est\u00e1n en origin/main" in facts
    assert "nunca se subi\u00f3" in facts
    assert "f0f375f (2026-10-26 19:49)" in facts
    assert "2026-11-11 (L031)" in facts


def test_valid_audit_says_so():
    report = render_report(make_audit(), CHECKS)
    assert "Todas las citas son textuales (4)" in report


def test_invalid_audit_flags_the_criterion_and_lists_issues():
    report = render_report(make_audit(valid=False), CHECKS)
    assert "> Aviso: la validaci\u00f3n encontr\u00f3 problemas en este criterio." in report
    assert "cita no textual" in report and "criterios[0].citas[0]" in report
    assert "Se encontr\u00f3 1 problema." in report


def test_template_text_uses_plain_punctuation():
    report = render_report(make_audit(), CHECKS)
    assert all(ord(c) < 128 or c in SPANISH for c in report)
