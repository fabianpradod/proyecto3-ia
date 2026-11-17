import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

import pytest

from preflight.canvas import CanvasError, download_file
from preflight.export import ExportError, build_bookmarklet, export_source, read_export
from preflight.fetch import import_assignment

FIXTURES = Path(__file__).parent / "fixtures"
TZ = "America/Guatemala"
NOW = datetime(2026, 11, 16, 22, 0, tzinfo=timezone.utc)


def evaluaciones_export():
    return {
        "format": "preflight-export/1",
        "kind": "assignment",
        "base_url": "https://uvg.instructure.com",
        "course_id": 46981,
        "exported_at": "2026-11-16T22:00:00Z",
        "assignment": json.loads((FIXTURES / "assignment_958579.json").read_text(encoding="utf-8")),
        "submission": {"workflow_state": "graded", "score": 0, "submitted_at": None},
        "files": [
            {"id": 13140488, "display_name": "Evaluacion.docx", "size": 20480,
             "content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
             "url": "https://uvg.instructure.com/files/13140488/download?verifier=abc"},
            {"id": 555, "error": "/files/555 returned 404"},
        ],
    }


def save(tmp_path, data, name="export.json"):
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_reads_an_assignment_export(tmp_path):
    data = read_export(save(tmp_path, evaluaciones_export()), kind="assignment")
    assert data["course_id"] == 46981


def test_rejects_unknown_format(tmp_path):
    with pytest.raises(ExportError):
        read_export(save(tmp_path, {"format": "other"}), kind="assignment")


def test_rejects_wrong_kind(tmp_path):
    with pytest.raises(ExportError):
        read_export(save(tmp_path, {**evaluaciones_export(), "kind": "course"}), kind="assignment")


def test_rejects_invalid_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ExportError):
        read_export(path, kind="assignment")


def test_import_writes_spec_and_meta(tmp_path):
    meta, out_dir = import_assignment(evaluaciones_export(), tmp_path, TZ, now=NOW)
    assert (out_dir / "spec.md").exists() and (out_dir / "meta.json").exists()
    assert meta["assignment_id"] == 958579
    assert meta["submission"]["submitted_at"] is None
    # Only files actually linked in the description count, and the signed url is not kept.
    assert meta["linked_files"] == [{
        "id": 13140488, "name": "Evaluacion.docx", "size": 20480,
        "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }]


def test_import_records_files_the_export_could_not_describe(tmp_path):
    export = evaluaciones_export()
    export["files"] = [{"id": 13140488, "error": "/files/13140488 returned 403"}]
    meta, _ = import_assignment(export, tmp_path, TZ, now=NOW)
    assert meta["linked_files"][0]["error"] == "/files/13140488 returned 403"


def test_import_copies_linked_files_found_next_to_the_export(tmp_path):
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    (downloads / "Evaluacion.docx").write_bytes(b"x" * 20480)
    meta, out_dir = import_assignment(evaluaciones_export(), tmp_path / "work", TZ, search_dir=downloads, now=NOW)
    copied = Path(meta["linked_files"][0]["path"])
    assert copied == out_dir / "files" / "13140488_Evaluacion.docx"
    assert copied.read_bytes() == b"x" * 20480


def test_import_skips_a_same_name_file_whose_size_differs(tmp_path):
    # A file with the template's name but another size is likely the student's own copy,
    # not the instructions, so it must not be treated as instructions.
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    (downloads / "Evaluacion.docx").write_bytes(b"x" * 999)
    meta, _ = import_assignment(evaluaciones_export(), tmp_path / "work", TZ, search_dir=downloads, now=NOW)
    entry = meta["linked_files"][0]
    assert "path" not in entry
    assert entry["local_size_mismatch"] == 999


def test_import_flags_linked_files_not_found_locally(tmp_path):
    meta, _ = import_assignment(evaluaciones_export(), tmp_path / "work", TZ, search_dir=tmp_path, now=NOW)
    assert meta["linked_files"][0]["missing_local"] is True
    assert "path" not in meta["linked_files"][0]


def test_download_refuses_hosts_other_than_canvas(tmp_path):
    with pytest.raises(CanvasError):
        download_file("https://evil.test/files/1", tmp_path / "x", allowed_host="uvg.instructure.com")


def test_bookmarklet_wraps_the_export_source():
    url = build_bookmarklet()
    assert url.startswith("javascript:")
    assert unquote(url[len("javascript:"):]) == export_source()


def test_export_source_only_reads():
    source = export_source()
    for verb in ("POST", "PUT", "PATCH", "DELETE", "method:"):
        assert verb not in source


def test_export_source_has_no_line_comments():
    # If a browser drops the newlines of a bookmark, a // comment would swallow the code after it.
    assert not any(line.strip().startswith("//") for line in export_source().splitlines())
