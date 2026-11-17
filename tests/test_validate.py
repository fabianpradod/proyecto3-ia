import copy

import pytest

from preflight.validate import validate

LINES = [
    {"id": "L001", "text": "# Proyecto"},
    {"id": "L002", "text": "- Prueben la automatizaci\u00f3n con al menos 3 casos reales."},
    {"id": "L003", "text": "Exploraci\u00f3n (Nov 11, 2026): tabla comparativa."},
    {"id": "L004", "text": "Pruebas con casos reales | 15"},
    {"id": "L005", "text": "Informe | 5"},
    {"id": "L006", "text": "Total | 20"},
]


def criterion(**overrides):
    item = {
        "criterio": "Pruebas", "puntos": 15, "estado": "cumple", "puntos_en_riesgo": 0,
        "citas": [{"linea": "L004", "texto": "Pruebas con casos reales"}],
        "evidencia": [{"archivo": "README.md", "detalle": "tiene la tabla"}],
        "observacion": "Cumple.",
    }
    item.update(overrides)
    return item


def informe(**overrides):
    return criterion(criterio="Informe", puntos=5, citas=[{"linea": "L005", "texto": "Informe"}], **overrides)


def make_audit(folder, criteria=None, fechas=None):
    return {
        "folder": str(folder),
        "folder_unchanged": True,
        "lines": LINES,
        "findings": {
            "resumen": "x",
            "criterios": criteria if criteria is not None else [criterion(), informe()],
            "fechas": fechas or [],
            "no_verificable": [],
        },
    }


@pytest.fixture
def folder(tmp_path):
    (tmp_path / "README.md").write_text("x")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "informe.docx").write_bytes(b"x")
    return tmp_path


def rules(result):
    return [issue["rule"] for issue in result["issues"]]


def test_a_clean_audit_is_valid(folder):
    result = validate(make_audit(folder))
    assert result["valid"] is True and result["issues"] == []
    assert result["counts"] == {"citations": 2, "evidence": 2, "criteria": 2}


def test_altered_quote_is_rejected(folder):
    audit = make_audit(folder, [criterion(citas=[{"linea": "L002", "texto": "Prueben la automatizacion con 3 casos"}]), informe()])
    result = validate(audit)
    assert result["valid"] is False and rules(result) == ["quote_not_verbatim"]
    assert result["issues"][0]["where"] == "criterios[0].citas[0]"


def test_unknown_line_is_rejected(folder):
    audit = make_audit(folder, [criterion(citas=[{"linea": "L999", "texto": "Pruebas"}]), informe()])
    assert rules(validate(audit)) == ["unknown_line"]


def test_quote_matches_regardless_of_accent_encoding_and_spacing(folder):
    quote = "Prueben  la automatizacio\u0301n con al menos"
    audit = make_audit(folder, [criterion(citas=[{"linea": "L004", "texto": "Pruebas con casos reales"}, {"linea": "L002", "texto": quote}]), informe()])
    assert validate(audit)["valid"] is True


def test_dates_are_checked_too(folder):
    fechas = [{"entregable": "Exploracion", "fecha": "Nov 11", "linea": "L003", "texto": "Nov 12, 2026"}]
    assert rules(validate(make_audit(folder, fechas=fechas))) == ["quote_not_verbatim"]


@pytest.mark.parametrize("path", ["README.md", "entrega/README.md", "texto/docs/informe.docx.txt", "docs", "inventario.txt"])
def test_evidence_paths_that_resolve(folder, path):
    audit = make_audit(folder, [criterion(evidencia=[{"archivo": path, "detalle": "x"}]), informe()])
    assert validate(audit)["valid"] is True


def test_missing_evidence_for_a_met_criterion_is_rejected(folder):
    audit = make_audit(folder, [criterion(evidencia=[{"archivo": "resultados/casos.md", "detalle": "x"}]), informe()])
    assert rules(validate(audit)) == ["evidence_not_found"]


def test_a_missing_criterion_may_point_to_what_does_not_exist(folder):
    audit = make_audit(folder, [criterion(estado="falta", puntos_en_riesgo=15, evidencia=[{"archivo": "exploracion/", "detalle": "no existe"}]), informe()])
    assert validate(audit)["valid"] is True


@pytest.mark.parametrize("overrides, rule", [
    ({"estado": "cumple", "puntos_en_riesgo": 5}, "risk_inconsistent"),
    ({"estado": "falta", "puntos_en_riesgo": 10}, "risk_inconsistent"),
    ({"estado": "parcial", "puntos_en_riesgo": 20}, "risk_over_points"),
    ({"estado": "parcial", "puntos_en_riesgo": -1}, "risk_over_points"),
])
def test_points_at_risk_must_fit_the_status(folder, overrides, rule):
    assert rules(validate(make_audit(folder, [criterion(**overrides), informe()]))) == [rule]


def test_points_must_match_the_cited_rubric_row(folder):
    audit = make_audit(folder, [criterion(puntos=20), informe()])
    assert rules(validate(audit)) == ["points_not_in_rubric"]


def test_criteria_must_cover_the_whole_rubric(folder):
    result = validate(make_audit(folder, [criterion()]))
    assert rules(result) == ["rubric_not_covered"]
    assert "15 of 20" in result["issues"][0]["detail"]


def test_criteria_are_marked_individually(folder):
    audit = make_audit(folder, [criterion(citas=[{"linea": "L004", "texto": "inventado"}]), informe()])
    result = validate(audit)
    assert result["criteria_valid"] == [False, True]


def test_a_changed_folder_makes_the_audit_invalid(folder):
    audit = make_audit(folder)
    audit["folder_unchanged"] = False
    assert rules(validate(audit)) == ["folder_changed"]


def test_validate_does_not_modify_the_audit(folder):
    audit = make_audit(folder)
    before = copy.deepcopy(audit)
    validate(audit)
    assert audit == before
