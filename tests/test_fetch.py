import json
from datetime import datetime, timezone
from pathlib import Path

from preflight.fetch import assignment_rows, build_meta, render_spec, to_local

FIXTURES = Path(__file__).parent / "fixtures"
TZ = "America/Guatemala"


def load_assignment(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def graded_submission():
    return {
        "workflow_state": "graded",
        "submitted_at": "2026-08-25T00:28:20Z",
        "late": False,
        "missing": False,
        "score": 5.76,
        "attempt": 1,
        "attachments": [{"display_name": "deck.pptx"}],
        "submission_comments": [
            {"author_name": "Profesor", "created_at": "2026-08-26T15:00:00Z", "comment": "-4 falta el codo"}
        ],
    }


def test_due_date_is_shown_in_guatemala_time():
    assert to_local("2026-11-19T05:59:59Z", TZ) == "2026-11-18 23:59"
    assert to_local(None, TZ) is None


def test_meta_summarizes_assignment_and_submission():
    meta = build_meta(46981, load_assignment("assignment_959073.json"), graded_submission(), [], TZ, "2026-11-16T22:00:00Z")
    assert meta["assignment_id"] == 959073
    assert meta["name"] == "Proyecto 3 - Automatiza algo tuyo con IA"
    assert meta["due_local"] == "2026-11-18 23:59"
    assert meta["submission"]["state"] == "graded"
    assert meta["submission"]["attachments"] == ["deck.pptx"]
    assert meta["submission"]["comments"][0]["text"] == "-4 falta el codo"
    assert sum(row["points"] for row in meta["point_rows"] if not row["is_total"]) == 100


def test_meta_handles_no_submission():
    meta = build_meta(46981, load_assignment("assignment_958579.json"), None, [], TZ, "2026-11-16T22:00:00Z")
    assert meta["submission"]["state"] == "unsubmitted"
    assert meta["submission"]["comments"] == []


def test_course_listing_flags_overdue_work_with_no_submission():
    now = datetime(2026, 11, 16, 22, 0, tzinfo=timezone.utc)
    assignments = [
        {"id": 1, "name": "Lab 6 ", "due_at": "2026-09-12T05:59:59Z", "points_possible": 4,
         "submission_types": ["online_upload"], "submission": {"workflow_state": "graded", "score": 0, "submitted_at": None}},
        {"id": 2, "name": "Lab 7", "due_at": "2026-10-17T05:59:59Z", "points_possible": 4,
         "submission_types": ["online_upload"], "submission": {"workflow_state": "graded", "score": 4, "submitted_at": "2026-10-16T23:56:00Z"}},
        {"id": 3, "name": "Proyecto 3", "due_at": "2026-11-19T05:59:59Z", "points_possible": 13.5,
         "submission_types": ["online_upload"], "submission": {"workflow_state": "unsubmitted", "submitted_at": None}},
        {"id": 4, "name": "Hoja en pizarra", "due_at": "2026-11-10T05:59:59Z", "points_possible": 5,
         "submission_types": ["on_paper"], "submission": {"workflow_state": "graded", "score": 5, "submitted_at": None}},
    ]
    rows = {row["id"]: row for row in assignment_rows(assignments, TZ, now)}
    assert rows[1]["flag"] == "overdue, no submission"
    assert rows[1]["name"] == "Lab 6"
    assert rows[2]["flag"] == ""
    assert rows[3]["flag"] == "open, no submission"
    assert rows[4]["flag"] == ""


def test_spec_lists_every_numbered_line():
    assignment = load_assignment("assignment_959073.json")
    meta = build_meta(46981, assignment, None, [], TZ, "2026-11-16T22:00:00Z")
    spec = render_spec(meta)
    assert "Due: 2026-11-18 23:59 (America/Guatemala)" in spec
    assert "\nL001 # Proyecto 3" in spec
    for line in meta["lines"]:
        assert f"{line['id']} {line['text']}" in spec
