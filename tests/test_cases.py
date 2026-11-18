from preflight.cases import compare_runs, score_case


def audit_with(*criteria, fechas=()):
    return {"findings": {"criterios": list(criteria), "fechas": [{"linea": line} for line in fechas]}}


def crit(estado, lineas, observacion="", criterio="c", riesgo=None, puntos=None):
    return {"criterio": criterio, "estado": estado, "puntos": puntos, "puntos_en_riesgo": riesgo,
            "citas": [{"linea": line, "texto": "x"} for line in lineas],
            "evidencia": [], "observacion": observacion}


CHECKS = {"results": [{"check": "folder", "status": "problem"}, {"check": "submission", "status": "warning"}]}


def outcomes(case, audit, checks=CHECKS):
    return [(item["esperado"], item["ok"]) for item in score_case(case, audit, checks)]


def test_script_facts_are_compared_by_status():
    case = {"esperado": {"hechos": {"folder": "problem", "submission": "ok"}}}
    assert outcomes(case, audit_with()) == [("hecho folder = problem", True), ("hecho submission = ok", False)]


def test_nothing_may_be_met_when_nothing_was_submitted():
    case = {"esperado": {"sin_cumple": True}}
    assert outcomes(case, audit_with(crit("falta", ["L001"]))) == [("ningun criterio en cumple", True)]
    assert outcomes(case, audit_with(crit("cumple", ["L001"]))) == [("ningun criterio en cumple", False)]


def test_a_complete_submission_may_not_get_invented_gaps():
    case = {"esperado": {"sin_falta": True}}
    assert outcomes(case, audit_with(crit("parcial", ["L001"]))) == [("ningun criterio en falta", True)]
    assert outcomes(case, audit_with(crit("falta", ["L001"]))) == [("ningun criterio en falta", False)]


def test_detection_needs_the_line_the_word_and_a_non_met_status():
    case = {"esperado": {"detecta": [{"lineas": ["L024", "L006"], "palabras": ["colab", "demo"]}]}}
    label = "detecta L024/L006 (colab/demo)"
    assert outcomes(case, audit_with(crit("falta", ["L024"], "No hay link al Colab."))) == [(label, True)]
    assert outcomes(case, audit_with(crit("cumple", ["L024"], "Hay link al Colab."))) == [(label, False)]
    assert outcomes(case, audit_with(crit("falta", ["L021"], "No hay link al Colab."))) == [(label, False)]
    assert outcomes(case, audit_with(crit("parcial", ["L006"], "Falta el PDF."))) == [(label, False)]


def test_detection_ignores_case_and_accents():
    case = {"esperado": {"detecta": [{"lineas": ["L043"], "palabras": ["reflexi"]}]}}
    assert outcomes(case, audit_with(crit("falta", ["L043"], "No hay REFLEXI\u00d3N personal."))) == [("detecta L043 (reflexi)", True)]


def test_dates_must_be_found():
    case = {"esperado": {"fechas": ["L031"]}}
    assert outcomes(case, audit_with(fechas=["L030", "L031"])) == [("fecha en L031", True)]
    assert outcomes(case, audit_with(fechas=["L030"])) == [("fecha en L031", False)]


def test_runs_are_compared_criterion_by_criterion():
    first = audit_with(crit("falta", ["L039"], criterio="Lista", riesgo=10, puntos=10), crit("parcial", ["L041"], criterio="Auto", riesgo=8, puntos=25))
    second = audit_with(crit("parcial", ["L039"], criterio="Lista", riesgo=8, puntos=10), crit("parcial", ["L041"], criterio="Auto", riesgo=8, puntos=25))
    diff = compare_runs([first, second])
    assert diff["risk"] == [18, 16]
    assert diff["changed"] == [{"criterio": "Lista", "estados": ["falta", "parcial"]}]
