import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from preflight.checks import date_mentions, resolve_as_of, run_checks
from preflight.fetch import build_meta

FIXTURES = Path(__file__).parent / "fixtures"
TZ = "America/Guatemala"
DUE = "2026-10-27T01:00:00Z"  # Oct 26, 19:00 in Guatemala


def meta_for(submission=None, due_at=DUE, fixture="assignment_959073.json"):
    assignment = json.loads((FIXTURES / fixture).read_text(encoding="utf-8"))
    assignment["due_at"] = due_at
    return build_meta(46981, assignment, submission, [], TZ, "2026-11-16T22:00:00Z")


def by_check(results):
    return {item["check"]: item for item in results}


def at(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


# Dates in the instructions text

@pytest.mark.parametrize("text, expected", [
    ("Exploracion (Nov 11, 2026): tabla", "2026-11-11"),
    ("Informe breve (Nov 18 2026, 2 a 3 paginas)", "2026-11-18"),
    ("Entrega el 18 de noviembre de 2026", "2026-11-18"),
    ("antes del 3 de nov", "2026-11-03"),
    ("fecha 2026-11-04 en ISO", "2026-11-04"),
    ("o el 11/12/2026 en formato local", "2026-12-11"),
])
def test_date_mentions_in_common_formats(text, expected):
    assert [m["date"] for m in date_mentions([{"id": "L001", "text": text}], 2026)] == [expected]


def test_impossible_dates_are_ignored():
    assert date_mentions([{"id": "L001", "text": "Nov 31, 2026 y 45/13/2026"}], 2026) == []


def test_proyecto3_dates_point_to_their_lines():
    found = [(m["line"], m["date"]) for m in date_mentions(meta_for()["lines"], 2026)]
    assert found == [
        ("L030", "2026-11-02"), ("L031", "2026-11-11"), ("L032", "2026-11-18"),
        ("L033", "2026-11-18"), ("L034", "2026-11-18"),
    ]


# Time of the check

def test_as_of_due_means_one_minute_before_the_deadline():
    assert resolve_as_of("due", meta_for(), at("2026-11-16T00:00:00Z")) == at(DUE) - timedelta(minutes=1)


def test_as_of_without_offset_is_local_time():
    assert resolve_as_of("2026-10-26T18:00", meta_for(), None) == at("2026-10-27T00:00:00Z")


# Deadline and submission

def test_deadline_passed_is_a_problem():
    assert by_check(run_checks(meta_for(), None, at("2026-10-28T00:00:00Z")))["deadline"]["status"] == "problem"


def test_deadline_with_less_than_a_day_left_is_a_warning():
    assert by_check(run_checks(meta_for(), None, at("2026-10-26T20:00:00Z")))["deadline"]["status"] == "warning"


def test_replay_ignores_a_submission_made_after_the_check_time():
    submission = {"workflow_state": "graded", "submitted_at": "2026-10-27T00:11:53Z", "score": 13.5}
    before = by_check(run_checks(meta_for(submission), None, at("2026-10-27T00:00:00Z")))["submission"]
    after = by_check(run_checks(meta_for(submission), None, at("2026-10-27T00:59:00Z")))["submission"]
    assert before["status"] == "warning"
    assert after["status"] == "ok"


def test_no_submission_after_the_deadline_is_a_problem():
    result = by_check(run_checks(meta_for({"workflow_state": "graded", "score": 0}), None, at("2026-11-01T00:00:00Z")))
    assert result["submission"]["status"] == "problem"


def test_checks_never_carry_scores_or_comments():
    submission = {"workflow_state": "graded", "submitted_at": "2026-10-27T00:11:53Z", "score": 12.25,
                  "submission_comments": [{"author_name": "Profesor", "comment": "falta el codo"}]}
    dumped = json.dumps(run_checks(meta_for(submission), None, at("2026-10-27T00:59:00Z")))
    assert "12.25" not in dumped and "codo" not in dumped and "score" not in dumped


# Text-only deadlines and rubric

def test_text_deadline_that_already_passed_is_a_warning():
    # Proyecto 3 at Nov 16: Lluvia (Nov 2) and Exploracion (Nov 11) dates in the text have passed.
    result = by_check(run_checks(meta_for(due_at="2026-11-19T05:59:59Z"), None, at("2026-11-16T22:00:00Z")))["text_dates"]
    assert result["status"] == "warning"
    assert [m["line"] for m in result["data"]["passed"]] == ["L030", "L031"]


def test_rubric_rows_matching_the_total_are_ok():
    result = by_check(run_checks(meta_for(), None, at("2026-10-26T00:00:00Z")))["rubric"]
    assert result["status"] == "ok"
    assert result["data"]["total"] == 100


def test_rubric_rows_that_do_not_add_up_are_a_warning():
    meta = meta_for()
    meta["point_rows"][0]["points"] = 15
    assert by_check(run_checks(meta, None, at("2026-10-26T00:00:00Z")))["rubric"]["status"] == "warning"


def test_unread_linked_files_are_a_warning():
    meta = meta_for()
    meta["linked_files"] = [{"id": 1, "name": "rubrica.pdf", "missing_local": True}]
    result = by_check(run_checks(meta, None, at("2026-10-26T00:00:00Z")))["sources"]
    assert result["status"] == "warning"
    assert result["data"]["unread_files"] == ["rubrica.pdf"]


def test_external_links_alone_are_info():
    # Lab 6 links to a Kaggle dataset and tutorials: references, not instructions.
    meta = meta_for()
    meta["links"] = [{"text": "Kaggle", "href": "https://www.kaggle.com/competitions/nlp-getting-started"}]
    result = by_check(run_checks(meta, None, at("2026-10-26T00:00:00Z")))["sources"]
    assert result["status"] == "info"
    assert result["data"]["external_links"] == ["https://www.kaggle.com/competitions/nlp-getting-started"]


# Folder

def test_missing_folder_is_a_problem(tmp_path):
    result = by_check(run_checks(meta_for(), tmp_path / "nope", at("2026-10-26T00:00:00Z")))["folder"]
    assert result["status"] == "problem"


def test_empty_folder_is_a_problem(tmp_path):
    assert by_check(run_checks(meta_for(), tmp_path, at("2026-10-26T00:00:00Z")))["folder"]["status"] == "problem"


def test_folder_inventory_counts_extensions_and_skips_hidden_dirs(tmp_path):
    (tmp_path / "a.ipynb").write_text("{}")
    (tmp_path / "b.ipynb").write_text("{}")
    (tmp_path / "README.md").write_text("x")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "lib.py").write_text("x")
    result = by_check(run_checks(meta_for(), tmp_path, at("2026-10-26T00:00:00Z")))["folder"]
    assert result["status"] == "ok"
    assert result["data"]["by_extension"] == {".ipynb": 2, ".md": 1}


# Git

def git(repo, *args, when=None):
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when} if when else None
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


@pytest.fixture
def repo(tmp_path):
    remote, work = tmp_path / "remote.git", tmp_path / "work"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    work.mkdir()
    git(work, "init", "-q", "-b", "main")
    git(work, "config", "user.name", "Test")
    git(work, "config", "user.email", "test@example.com")
    (work / "informe.md").write_text("v1")
    git(work, "add", "informe.md")
    git(work, "commit", "-q", "-m", "first", when="2026-10-26T18:00:00-06:00")
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-q", "-u", "origin", "main")
    (work / "informe.md").write_text("v2")
    git(work, "commit", "-q", "-am", "fix after deadline", when="2026-10-26T20:00:00-06:00")
    return work


def test_commits_after_the_due_date_are_a_warning(repo):
    result = by_check(run_checks(meta_for(), repo, at("2026-10-27T00:59:00Z")))["git_after_due"]
    assert result["status"] == "warning"
    assert [commit["subject"] for commit in result["data"]["commits"]] == ["fix after deadline"]
    assert result["data"]["commits"][0]["local"] == "2026-10-26 20:00"


def test_unpushed_and_uncommitted_work_are_warnings(repo):
    (repo / "notas.md").write_text("sin commit")
    checks = by_check(run_checks(meta_for(), repo, at("2026-10-27T00:59:00Z")))
    assert checks["git_unpushed"]["status"] == "warning"
    assert checks["git_unpushed"]["data"]["ahead"] == 1
    assert checks["git_uncommitted"]["data"]["changes"] == 1


def test_work_on_a_side_branch_is_a_warning(repo):
    git(repo, "push", "-q", "origin", "main")
    git(repo, "switch", "-q", "-c", "fabian/feature")
    (repo / "extra.md").write_text("x")
    git(repo, "add", "extra.md")
    git(repo, "commit", "-q", "-m", "extra")
    result = by_check(run_checks(meta_for(), repo, at("2026-10-27T00:59:00Z")))["git_branch"]
    assert result["status"] == "warning"
    assert result["data"] == {"branch": "fabian/feature", "default": "origin/main", "not_in_default": 1}


def test_git_checks_do_not_touch_the_index(repo):
    # A stale index makes a plain `git status` rewrite .git/index; the checks must not.
    os.utime(repo / "informe.md", (1, 1))
    index = repo / ".git" / "index"
    before = (index.read_bytes(), index.stat().st_mtime_ns)
    run_checks(meta_for(), repo, at("2026-10-27T00:59:00Z"))
    assert (index.read_bytes(), index.stat().st_mtime_ns) == before


def test_folder_that_is_not_a_repo_reports_it(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    result = by_check(run_checks(meta_for(), tmp_path, at("2026-10-26T00:00:00Z")))["git"]
    assert result["status"] == "info"
    assert result["data"]["is_repo"] is False
