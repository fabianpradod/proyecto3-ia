"""Get one assignment (Canvas API or browser export) and write the files the audit reads."""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .canvas import CanvasError, safe_filename
from .spec import find_linked_files, find_links, find_point_rows, html_to_lines, number_lines

NO_UPLOAD_TYPES = {"on_paper", "none", "not_graded", "external_tool"}


def parse_iso(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def to_local(iso, tz):
    if not iso:
        return None
    return parse_iso(iso).astimezone(ZoneInfo(tz)).strftime("%Y-%m-%d %H:%M")


def summarize_submission(submission, tz):
    submission = submission or {}
    return {
        "state": submission.get("workflow_state", "unsubmitted"),
        "submitted_at": submission.get("submitted_at"),
        "submitted_local": to_local(submission.get("submitted_at"), tz),
        "late": bool(submission.get("late")),
        "missing": bool(submission.get("missing")),
        "score": submission.get("score"),
        "attempt": submission.get("attempt"),
        "attachments": [item.get("display_name") for item in submission.get("attachments") or []],
        "comments": [
            {"author": item.get("author_name"), "date": to_local(item.get("created_at"), tz), "text": item.get("comment", "")}
            for item in submission.get("submission_comments") or []
        ],
    }


def build_meta(course_id, assignment, submission, linked_files, tz, fetched_at):
    description = assignment.get("description")
    numbered = number_lines(html_to_lines(description))
    return {
        "course_id": course_id,
        "assignment_id": assignment["id"],
        "name": (assignment.get("name") or "").strip(),
        "html_url": assignment.get("html_url"),
        "timezone": tz,
        "due_at": assignment.get("due_at"),
        "due_local": to_local(assignment.get("due_at"), tz),
        "unlock_local": to_local(assignment.get("unlock_at"), tz),
        "lock_local": to_local(assignment.get("lock_at"), tz),
        "points_possible": assignment.get("points_possible"),
        "submission_types": assignment.get("submission_types") or [],
        "allowed_extensions": assignment.get("allowed_extensions") or [],
        "submission": summarize_submission(submission, tz),
        "linked_files": linked_files,
        "links": find_links(description),
        "point_rows": find_point_rows(numbered),
        "lines": [{"id": line_id, "text": text} for line_id, text in numbered],
        "fetched_at": fetched_at,
    }


def render_spec(meta):
    header = [
        f"# Instructions: {meta['name']}",
        "",
        f"Course: {meta['course_id']}  Assignment: {meta['assignment_id']}",
        f"Link: {meta['html_url']}",
        f"Due: {meta['due_local'] or 'no due date'} ({meta['timezone']})",
        f"Points in the final grade: {meta['points_possible']}",
        f"Submission types: {', '.join(meta['submission_types']) or 'none'}",
    ]
    if meta["linked_files"]:
        header.append("Files linked in the description: " + "; ".join(item["name"] for item in meta["linked_files"]))
    if meta["links"]:
        header.append("Other links in the description: " + "; ".join(item["href"] for item in meta["links"]))
    body = [f"{line['id']} {line['text']}" for line in meta["lines"]]
    return "\n".join(header + ["", "## Text", ""] + body) + "\n"


def _file_entry(item, info):
    return {
        "id": item["id"],
        "name": info.get("display_name") or item["name"],
        "size": info.get("size"),
        "content_type": info.get("content-type"),
        "url": info.get("url"),
    }


def describe_linked_files(canvas, description):
    linked = []
    for item in find_linked_files(description):
        try:
            linked.append(_file_entry(item, canvas.file_info(item["id"])))
        except CanvasError as error:
            linked.append({**item, "error": str(error)})
    return linked


def linked_from_export(description, files_info):
    by_id = {info.get("id"): info for info in files_info or []}
    linked = []
    for item in find_linked_files(description):
        info = by_id.get(item["id"])
        if info is None:
            linked.append({**item, "error": "not in the export"})
        elif info.get("error"):
            linked.append({**item, "error": info["error"]})
        else:
            linked.append(_file_entry(item, info))
    return linked


def _save_linked_files(linked, out_dir, downloader):
    files_dir = out_dir / "files"
    files_dir.mkdir(exist_ok=True)
    for item in linked:
        if not item.get("url"):
            continue
        dest = files_dir / safe_filename(item["id"], item["name"])
        try:
            downloader(item["url"], dest)
            item["path"] = str(dest)
        except CanvasError as error:
            item["error"] = str(error)


def write_outputs(course_id, assignment, submission, linked, out_root, tz, fetched_at, downloader=None):
    out_dir = Path(out_root) / str(assignment["id"])
    out_dir.mkdir(parents=True, exist_ok=True)
    if downloader:
        _save_linked_files(linked, out_dir, downloader)
    for item in linked:
        item.pop("url", None)  # signed download link, not worth keeping

    meta = build_meta(course_id, assignment, submission, linked, tz, fetched_at)
    (out_dir / "assignment.json").write_text(json.dumps(assignment, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "spec.md").write_text(render_spec(meta), encoding="utf-8")
    return meta, out_dir


def fetch_assignment(canvas, course_id, assignment_id, out_root, tz, download=False, now=None):
    assignment = canvas.assignment(course_id, assignment_id)
    submission = canvas.my_submission(course_id, assignment_id)
    linked = describe_linked_files(canvas, assignment.get("description"))
    fetched_at = (now or datetime.now(timezone.utc)).isoformat(timespec="seconds")
    downloader = canvas.download if download else None
    return write_outputs(course_id, assignment, submission, linked, out_root, tz, fetched_at, downloader)


def _copy_local_files(linked, search_dir, out_dir):
    # File links at UVG carry no signature, so Python cannot download them without the
    # browser login. The user downloads them next to the export and we pick them up.
    files_dir = out_dir / "files"
    for item in linked:
        if item.get("error"):
            continue
        source = Path(search_dir) / item["name"]
        if not source.is_file():
            item["missing_local"] = True
            continue
        local_size = source.stat().st_size
        if item.get("size") is not None and local_size != item["size"]:
            # Same name, other size: likely the student's own copy, not the instructions.
            item["local_size_mismatch"] = local_size
            continue
        files_dir.mkdir(parents=True, exist_ok=True)
        dest = files_dir / safe_filename(item["id"], item["name"])
        shutil.copy2(source, dest)
        item["path"] = str(dest)


def import_assignment(export, out_root, tz, search_dir=None, now=None):
    assignment = export["assignment"]
    linked = linked_from_export(assignment.get("description"), export.get("files"))
    if search_dir is not None:
        _copy_local_files(linked, search_dir, Path(out_root) / str(assignment["id"]))
    fetched_at = export.get("exported_at") or (now or datetime.now(timezone.utc)).isoformat(timespec="seconds")
    return write_outputs(export["course_id"], assignment, export.get("submission"), linked, out_root, tz, fetched_at)


def assignment_rows(assignments, tz, now):
    rows = []
    for item in assignments:
        submission = item.get("submission") or {}
        needs_upload = not NO_UPLOAD_TYPES.intersection(item.get("submission_types") or [])
        flag = ""
        if needs_upload and not submission.get("submitted_at"):
            due = item.get("due_at")
            flag = "overdue, no submission" if due and parse_iso(due) < now else "open, no submission"
        rows.append({
            "id": item["id"],
            "due_local": to_local(item.get("due_at"), tz) or "-",
            "points": item.get("points_possible"),
            "state": submission.get("workflow_state", "unsubmitted"),
            "score": submission.get("score"),
            "flag": flag,
            "name": (item.get("name") or "").strip(),
        })
    return rows
