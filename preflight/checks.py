"""Facts about a submission that need no judgment: dates, submission state, files and git.

The audit agent receives these as given facts instead of guessing them. Scores and
professor comments are never used here: when replaying a past assignment they are the answer.
"""

import os
import re
import subprocess
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .extract import iter_files
from .fetch import NO_UPLOAD_TYPES, parse_iso, to_local

MONTHS = {
    "ene": 1, "enero": 1, "jan": 1, "january": 1,
    "feb": 2, "febrero": 2, "february": 2,
    "mar": 3, "marzo": 3, "march": 3,
    "abr": 4, "abril": 4, "apr": 4, "april": 4,
    "may": 5, "mayo": 5,
    "jun": 6, "junio": 6, "june": 6,
    "jul": 7, "julio": 7, "july": 7,
    "ago": 8, "agosto": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "set": 9, "septiembre": 9, "setiembre": 9, "september": 9,
    "oct": 10, "octubre": 10, "october": 10,
    "nov": 11, "noviembre": 11, "november": 11,
    "dic": 12, "diciembre": 12, "dec": 12, "december": 12,
}
MONTH = "|".join(sorted(MONTHS, key=len, reverse=True))
DATE_PATTERNS = [
    re.compile(rf"\b(?P<month>{MONTH})\.?\s+(?P<day>\d{{1,2}})(?:,?\s+(?P<year>\d{{4}}))?\b", re.IGNORECASE),
    re.compile(rf"\b(?P<day>\d{{1,2}})\s+de\s+(?P<month>{MONTH})\.?(?:\s+(?:del?\s+)?(?P<year>\d{{4}}))?\b", re.IGNORECASE),
    re.compile(r"\b(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\b"),
    re.compile(r"\b(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})\b"),
]


def result(check, status, summary, **data):
    return {"check": check, "status": status, "summary": summary, "data": data}


# Dates

def date_mentions(lines, default_year):
    mentions = []
    for line in lines:
        taken = []
        for pattern in DATE_PATTERNS:
            for match in pattern.finditer(line["text"]):
                if any(start < match.end() and match.start() < end for start, end in taken):
                    continue
                month = match["month"]
                month = int(month) if month.isdigit() else MONTHS[month.lower()]
                try:
                    found = date(int(match["year"] or default_year), month, int(match["day"]))
                except ValueError:
                    continue
                taken.append(match.span())
                mentions.append({"line": line["id"], "date": found.isoformat(), "text": match[0], "start": match.start()})
    mentions.sort(key=lambda item: (int(item["line"][1:]), item.pop("start")))
    return mentions


def resolve_as_of(value, meta, now):
    if value in (None, "now"):
        return now
    if value == "due":
        if not meta.get("due_at"):
            raise ValueError("this assignment has no due date, so --as-of due has no meaning")
        return parse_iso(meta["due_at"]) - timedelta(minutes=1)
    moment = datetime.fromisoformat(value)
    return moment if moment.tzinfo else moment.replace(tzinfo=ZoneInfo(meta["timezone"]))


def _local_date(moment, tz):
    return moment.astimezone(ZoneInfo(tz)).date()


def check_deadline(meta, as_of):
    if not meta.get("due_at"):
        return result("deadline", "info", "no due date in Canvas")
    left = parse_iso(meta["due_at"]) - as_of
    hours = round(left.total_seconds() / 3600, 2)
    data = {"due_local": meta["due_local"], "hours_left": hours}
    if left <= timedelta(0):
        return result("deadline", "problem", f"the due date passed {-hours:g} hours ago", **data)
    if left < timedelta(hours=24):
        return result("deadline", "warning", f"{hours:g} hours left", **data)
    return result("deadline", "ok", f"{hours:g} hours left", **data)


def check_submission(meta, as_of):
    if NO_UPLOAD_TYPES.intersection(meta.get("submission_types") or []):
        return result("submission", "info", "submitted outside Canvas", types=meta["submission_types"])
    submission = meta.get("submission") or {}
    submitted = submission.get("submitted_at")
    if submitted and parse_iso(submitted) <= as_of:
        return result("submission", "ok", f"submitted in Canvas on {submission['submitted_local']}",
                      submitted_local=submission["submitted_local"], attempt=submission.get("attempt"))
    past_due = bool(meta.get("due_at")) and parse_iso(meta["due_at"]) <= as_of
    if past_due:
        return result("submission", "problem", "nothing submitted in Canvas and the due date passed")
    return result("submission", "warning", "nothing submitted in Canvas yet")


def check_text_dates(meta, as_of):
    tz = meta["timezone"]
    due = parse_iso(meta["due_at"]) if meta.get("due_at") else None
    default_year = (due or as_of).astimezone(ZoneInfo(tz)).year
    mentions = date_mentions(meta["lines"], default_year)
    today, due_day = _local_date(as_of, tz), _local_date(due, tz) if due else None
    passed = [m for m in mentions if date.fromisoformat(m["date"]) < today and (due_day is None or date.fromisoformat(m["date"]) < due_day)]
    data = {"mentions": mentions, "passed": passed}
    if passed:
        listed = ", ".join(f"{m['date']} ({m['line']})" for m in passed)
        return result("text_dates", "warning", f"dates in the text that already passed: {listed}", **data)
    if mentions:
        return result("text_dates", "info", f"{len(mentions)} dates mentioned in the text", **data)
    return result("text_dates", "ok", "no dates in the text besides the Canvas due date", **data)


# Instructions

def check_rubric(meta):
    rows = meta.get("point_rows") or []
    criteria = [{"line": r["line"], "criterion": r["criterion"], "points": r["points"]} for r in rows if not r["is_total"]]
    stated = [r["points"] for r in rows if r["is_total"]]
    if not criteria:
        return result("rubric", "info", "no points table in the instructions text")
    total = sum(item["points"] for item in criteria)
    data = {"criteria": criteria, "total": total, "stated_total": stated[-1] if stated else None}
    if stated and abs(stated[-1] - total) > 1e-9:
        return result("rubric", "warning", f"the criteria add up to {total:g} but the text states {stated[-1]:g}", **data)
    return result("rubric", "ok", f"{len(criteria)} criteria worth {total:g} points", **data)


def check_sources(meta):
    unread = [item["name"] for item in meta.get("linked_files") or [] if not item.get("path")]
    links = [item["href"] for item in meta.get("links") or []]
    data = {"unread_files": unread, "external_links": links}
    if unread:
        # Files attached in Canvas are often templates or rubrics, so not reading them is a risk.
        return result("sources", "warning", f"attached files not read: {', '.join(unread)}", **data)
    if links:
        return result("sources", "info", f"{len(links)} external links (references or data), not read", **data)
    return result("sources", "ok", "all instructions are in the Canvas text", **data)


# Folder and git

def check_folder(folder, tz):
    if not folder.is_dir():
        return result("folder", "problem", f"the folder {folder} does not exist")
    files = [path for path, _ in iter_files(folder)]
    if not files:
        return result("folder", "problem", "the folder is empty")
    latest = max(files, key=lambda path: path.stat().st_mtime)
    by_extension = Counter(path.suffix.lower() or "(none)" for path in files)
    data = {
        "files": len(files),
        "bytes": sum(path.stat().st_size for path in files),
        "by_extension": dict(sorted(by_extension.items())),
        "latest_file": latest.relative_to(folder).as_posix(),
        "latest_modified_local": datetime.fromtimestamp(latest.stat().st_mtime, ZoneInfo(tz)).strftime("%Y-%m-%d %H:%M"),
    }
    return result("folder", "ok", f"{len(files)} files", **data)


def check_file_types(meta, folder):
    allowed = [ext.lower().lstrip(".") for ext in meta.get("allowed_extensions") or []]
    if not allowed:
        return result("file_types", "info", "Canvas does not restrict file types", submission_types=meta.get("submission_types"))
    found = sorted({path.suffix.lower().lstrip(".") for path, _ in iter_files(folder)} & set(allowed)) if folder.is_dir() else []
    if not found:
        return result("file_types", "problem", f"no file of the types Canvas accepts: {', '.join(allowed)}", allowed=allowed)
    return result("file_types", "ok", f"found accepted types: {', '.join(found)}", allowed=allowed, found=found)


def _git(folder, *args):
    # --no-optional-locks keeps `git status` from rewriting .git/index: the folder stays untouched.
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C"}
    try:
        proc = subprocess.run(["git", "--no-optional-locks", "-C", str(folder), *args],
                              capture_output=True, text=True, timeout=30, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def _default_branch(folder):
    head = _git(folder, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if head:
        return head
    for name in ("main", "master"):
        if _git(folder, "rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}") is not None:
            return f"origin/{name}"
    return None


def check_git(folder, meta, tz):
    if not folder.is_dir() or _git(folder, "rev-parse", "--is-inside-work-tree") != "true":
        return [result("git", "info", "not a git repository", is_repo=False)]
    branch = _git(folder, "rev-parse", "--abbrev-ref", "HEAD")
    default = _default_branch(folder)
    results = [result("git", "info", f"git repository on branch {branch}", is_repo=True, branch=branch,
                      default=default, remote=_git(folder, "remote", "get-url", "origin"))]

    status = _git(folder, "status", "--porcelain") or ""
    changes = len(status.splitlines())
    results.append(result("git_uncommitted", "warning" if changes else "ok",
                          f"{changes} uncommitted changes" if changes else "no uncommitted changes", changes=changes))

    upstream = _git(folder, "rev-parse", "--abbrev-ref", "@{upstream}")
    if upstream is None:
        results.append(result("git_unpushed", "warning", f"branch {branch} has no upstream: it was never pushed", upstream=None))
    else:
        ahead = int(_git(folder, "rev-list", "--count", f"{upstream}..HEAD") or 0)
        results.append(result("git_unpushed", "warning" if ahead else "ok",
                              f"{ahead} commits not pushed to {upstream}" if ahead else "everything is pushed",
                              upstream=upstream, ahead=ahead))

    if default and branch != default.split("/", 1)[1]:
        missing = int(_git(folder, "rev-list", "--count", f"{default}..HEAD") or 0)
        data = {"branch": branch, "default": default, "not_in_default": missing}
        if missing:
            results.append(result("git_branch", "warning", f"{missing} commits on {branch} are not in {default}, the branch reviewers see", **data))
        else:
            results.append(result("git_branch", "ok", f"{branch} has nothing missing from {default}", **data))

    if meta.get("due_at"):
        log = _git(folder, "log", f"--since={meta['due_at']}", "--format=%h%x09%cI%x09%s") or ""
        commits = [
            {"hash": short, "local": to_local(when, tz), "subject": subject}
            for short, when, subject in (line.split("\t", 2) for line in log.splitlines())
        ]
        summary = f"{len(commits)} commits dated after the due date ({meta['due_local']})" if commits else "no commits after the due date"
        results.append(result("git_after_due", "warning" if commits else "ok", summary, commits=commits))
    return results


def run_checks(meta, folder, as_of):
    tz = meta["timezone"]
    results = [
        check_deadline(meta, as_of),
        check_submission(meta, as_of),
        check_text_dates(meta, as_of),
        check_rubric(meta),
        check_sources(meta),
    ]
    if folder is not None:
        folder = Path(folder)
        results.append(check_folder(folder, tz))
        results.append(check_file_types(meta, folder))
        results.extend(check_git(folder, meta, tz))
    return results
