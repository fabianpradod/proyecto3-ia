import json
from pathlib import Path

from preflight.spec import find_linked_files, find_links, find_point_rows, html_to_lines, number_lines

FIXTURES = Path(__file__).parent / "fixtures"


def load_assignment(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def proyecto3_lines():
    return number_lines(html_to_lines(load_assignment("assignment_959073.json")["description"]))


def test_lines_are_numbered_in_order_and_never_empty():
    lines = proyecto3_lines()
    assert [line_id for line_id, _ in lines] == [f"L{i:03d}" for i in range(1, len(lines) + 1)]
    assert all(text.strip() for _, text in lines)


def test_deliverable_dates_come_from_the_visible_text():
    # The <time> chips carry data-ts values (2026-11-04) that disagree with the text shown (Nov 11).
    texts = [text for _, text in proyecto3_lines()]
    exploracion = [text for text in texts if text.startswith("- Exploraci\u00f3n")]
    assert exploracion == [
        "- Exploraci\u00f3n (Nov 11, 2026): lista de tareas y tabla comparativa de las 3 herramientas."
    ]
    assert not any("2026-11-04" in text for text in texts)


def test_rubric_rows_sum_to_the_stated_total():
    rows = find_point_rows(proyecto3_lines())
    criteria = [row for row in rows if not row["is_total"]]
    totals = [row for row in rows if row["is_total"]]
    assert len(criteria) == 6
    assert sum(row["points"] for row in criteria) == 100
    assert [row["points"] for row in totals] == [100]
    assert criteria[1]["criterion"] == "Exploraci\u00f3n de 3 herramientas con tabla comparativa"
    assert criteria[1]["line"].startswith("L")


def test_table_header_is_not_a_point_row():
    rows = find_point_rows(proyecto3_lines())
    assert all(row["criterion"] != "Criterio" for row in rows)


def test_empty_paragraphs_are_dropped_and_nbsp_becomes_space():
    assert html_to_lines("<p>uno</p><p>&nbsp;</p><p>dos&nbsp;tres</p>") == ["uno", "dos tres"]


def test_headings_and_list_items_keep_a_marker():
    html = "<h2>Requisitos</h2><ul><li>Primero</li><li>Segundo <strong>fuerte</strong></li></ul>"
    assert html_to_lines(html) == ["# Requisitos", "- Primero", "- Segundo fuerte"]


def test_list_item_with_nested_list_keeps_its_own_text():
    assert html_to_lines("<ul><li>Padre<ul><li>Hijo</li></ul></li></ul>") == ["- Padre", "- Hijo"]


def test_accents_are_normalized_to_one_form():
    # Canvas stores some accents decomposed (o + U+0301); quotes must match either way.
    assert html_to_lines("<p>Evaluacio\u0301n</p>") == ["Evaluaci\u00f3n"]


def test_br_splits_lines():
    assert html_to_lines("<p>uno<br>dos</p>") == ["uno", "dos"]


def test_linked_files_are_listed_once_per_file():
    html = load_assignment("assignment_958579.json")["description"]
    assert find_linked_files(html) == [
        {"id": 13140488, "name": "Proyecto 2 \u2013 Evaluaci\u00f3n de proyectos de otros grupos.docx"}
    ]


def test_no_linked_files_in_proyecto3():
    assert find_linked_files(load_assignment("assignment_959073.json")["description"]) == []


def test_other_links_are_listed_apart_from_files():
    html = (
        '<p><a href="https://docs.google.com/document/d/abc">Rubrica</a>'
        ' <a href="/courses/1/files/9?wrap=1" data-api-returntype="File">datos.csv</a>'
        ' <a href="https://github.com/x/files/123">repo</a></p>'
    )
    assert find_linked_files(html) == [{"id": 9, "name": "datos.csv"}]
    assert find_links(html) == [
        {"text": "Rubrica", "href": "https://docs.google.com/document/d/abc"},
        {"text": "repo", "href": "https://github.com/x/files/123"},
    ]
