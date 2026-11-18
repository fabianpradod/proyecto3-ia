"""Command line entry point: python -m preflight <command>."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .audit import PROMPT_VERSION, AuditError, run_audit
from .canvas import Canvas, CanvasError, parse_assignment_ref
from .cases import run_cases, write_results
from .checks import resolve_as_of, run_checks
from .config import ConfigError, load_settings
from .export import ExportError, assignment_from_course, build_bookmarklet, read_export
from .extract import ExtractError, extract_folder
from .fetch import assignment_rows, fetch_assignment, import_assignment, to_local
from .report import render_report
from .validate import validate

CANVAS_COMMANDS = {"fetch", "list"}


def format_size(size):
    return f"{size / 1024:.0f} KB" if size else "size unknown"


def print_summary(meta, out_dir, tz):
    criteria = [row for row in meta["point_rows"] if not row["is_total"]]
    totals = [row["points"] for row in meta["point_rows"] if row["is_total"]]
    print(meta["name"])
    print(f"  due: {meta['due_local'] or 'no due date'} ({tz})   points: {meta['points_possible']}")
    print(f"  submission: {meta['submission']['state']}, submitted {meta['submission']['submitted_local'] or 'never'}")
    print(f"  lines: {len(meta['lines'])}   point rows: {len(criteria)}, sum {sum(r['points'] for r in criteria)}, stated total {totals or 'none'}")
    for item in meta["linked_files"]:
        status = item.get("error") or format_size(item.get("size"))
        if item.get("path"):
            status += ", saved to work"
        elif item.get("local_size_mismatch") is not None:
            status += f", a local file with this name is {format_size(item['local_size_mismatch'])}, not the Canvas copy; skipped"
        elif item.get("missing_local"):
            status += ", not found: download it from the Canvas page into the export's folder and import again"
        print(f"  linked file: {item['name']} ({status})")
    for item in meta["links"]:
        print(f"  other link: {item['href']}")
    print(f"  wrote {out_dir}/spec.md, meta.json, assignment.json")


def print_rows(rows):
    print(f"{'id':<8} {'due':<17} {'pts':>5}  {'state':<12} {'score':>6}  {'flag':<23} name")
    for row in rows:
        score = "-" if row["score"] is None else f"{row['score']:g}"
        print(f"{row['id']:<8} {row['due_local']:<17} {row['points'] or 0:>5g}  {row['state']:<12} {score:>6}  {row['flag']:<23} {row['name']}")


def work_root(args, settings):
    return Path(args.out or settings["PREFLIGHT_WORK"]).expanduser()


def cmd_fetch(args, settings, canvas):
    tz = settings["PREFLIGHT_TZ"]
    meta, out_dir = fetch_assignment(canvas, args.course_id, args.assignment_id, work_root(args, settings), tz, download=args.download)
    print_summary(meta, out_dir, tz)


def cmd_list(args, settings, canvas):
    print_rows(assignment_rows(canvas.assignments(args.course), settings["PREFLIGHT_TZ"], datetime.now(timezone.utc)))


def cmd_import(args, settings, canvas):
    export = read_export(args.export)
    tz = settings["PREFLIGHT_TZ"]
    if export["kind"] == "course":
        if args.assignment is None:
            print_rows(assignment_rows(export["assignments"], tz, datetime.now(timezone.utc)))
            return
        export = assignment_from_course(export, args.assignment)
    meta, out_dir = import_assignment(export, work_root(args, settings), tz, search_dir=args.export.parent)
    print_summary(meta, out_dir, tz)


def load_meta(work, assignment_id):
    meta_path = work / str(assignment_id) / "meta.json"
    if not meta_path.exists():
        raise ValueError(f"no data for assignment {assignment_id} at {meta_path}; run import first")
    return json.loads(meta_path.read_text(encoding="utf-8"))


def write_checks(work, meta, folder, as_of_value):
    as_of = resolve_as_of(as_of_value, meta, datetime.now(timezone.utc))
    report = {
        "assignment_id": meta["assignment_id"],
        "as_of": as_of.isoformat(timespec="seconds"),
        "as_of_local": to_local(as_of.isoformat(), meta["timezone"]),
        "folder": str(folder) if folder else None,
        "results": run_checks(meta, folder, as_of),
    }
    out_path = work / str(meta["assignment_id"]) / "checks.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report, out_path


def cmd_check(args, settings, canvas):
    work = work_root(args, settings)
    meta = load_meta(work, args.assignment_id)
    folder = args.folder.expanduser().resolve() if args.folder else None
    report, out_path = write_checks(work, meta, folder, args.as_of)
    print(f"{meta['name']}: checks as of {report['as_of_local']} ({meta['timezone']})")
    for item in report["results"]:
        label = item["status"].upper() if item["status"] == "problem" else item["status"]
        print(f"  {label:<8} {item['check']:<16} {item['summary']}")
    print(f"  wrote {out_path}")


def cmd_audit(args, settings, canvas):
    work = work_root(args, settings)
    meta = load_meta(work, args.assignment_id)
    folder = args.folder.expanduser().resolve()
    report, _ = write_checks(work, meta, folder, args.as_of)
    print(f"Auditing {meta['name']} as of {report['as_of_local']} with {args.model} (prompt {PROMPT_VERSION}); this takes a few minutes")
    audit = run_audit(meta, report, folder, work, args.model)
    with_points = [c for c in audit["findings"]["criterios"] if c["puntos"] is not None]
    for item in audit["findings"]["criterios"]:
        points = f"{item['puntos_en_riesgo'] or 0:g}/{item['puntos']:g}" if item["puntos"] is not None else "-"
        print(f"  {item['estado']:<14} {points:>9}  {item['criterio'][:80]}")
    at_risk = sum(c["puntos_en_riesgo"] or 0 for c in with_points)
    print(f"  points at risk: {at_risk:g} of {sum(c['puntos'] for c in with_points):g}")
    run = audit["run"]
    print(f"  folder unchanged: {'yes' if audit['folder_unchanged'] else 'NO'}   model: {', '.join(run['models']) or args.model}   turns: {run['num_turns']}   time: {(run['duration_ms'] or 0) / 1000:.0f} s")
    if run["permission_denials"]:
        print(f"  blocked tool calls: {len(run['permission_denials'])} (the agent tried to go outside its sandbox)")
    report_path = write_report(work, audit, report)
    validation = audit["validation"]
    counts = validation["counts"]
    if validation["valid"]:
        print(f"  validation: ok ({counts['citations']} citations word for word, {counts['evidence']} evidence entries)")
    else:
        print(f"  validation: {len(validation['issues'])} problems")
        for item in validation["issues"]:
            print(f"    {item['rule']:<20} {item['where']:<26} {item['detail'][:90]}")
    print(f"  wrote {work / str(meta['assignment_id']) / 'audit.json'}")
    print(f"  report: {report_path}")


def write_report(work, audit, checks):
    path = work / str(audit["assignment_id"]) / "reporte.md"
    path.write_text(render_report(audit, checks), encoding="utf-8")
    return path


def cmd_report(args, settings, canvas):
    work = work_root(args, settings)
    base = work / str(args.assignment_id)
    if not (base / "audit.json").exists():
        raise ValueError(f"no audit for assignment {args.assignment_id} at {base}; run audit first")
    audit = json.loads((base / "audit.json").read_text(encoding="utf-8"))
    checks = json.loads((base / "checks.json").read_text(encoding="utf-8")) if (base / "checks.json").exists() else {}
    audit["validation"] = validate(audit)  # re-check with the current rules
    print(write_report(work, audit, checks))


def cmd_cases(args, settings, canvas):
    work = Path(args.out or Path(settings["PREFLIGHT_WORK"]).expanduser() / "casos")
    print(f"Running {args.runs} audits per case, {args.parallel} at a time, with {args.model}; results are written when all finish")
    cases, done = run_cases(args.cases, work, runs=args.runs, parallel=args.parallel, model=args.model, only=args.only)
    for result in done:
        print(f"  {result['case']:<22} run {result['run']}: {'ERROR ' + result['error'][-120:] if 'error' in result else 'done'}")
    print(write_results(cases, done, Path(args.cases).parent))


def cmd_extract(args, settings, canvas):
    folder = args.folder.expanduser().resolve()
    out_dir = args.out or Path(settings["PREFLIGHT_WORK"]).expanduser() / "extract" / folder.name
    manifest = extract_folder(folder, out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    done = [entry for entry in manifest if "text" in entry]
    print(f"Extracted {len(done)} of {len(manifest)} docx/pptx/pdf files from {folder}")
    print(f"  into {out_dir}")
    for entry in manifest:
        status = f"{entry['chars']:>8,} chars" if "text" in entry else f"   error: {entry['error']}"
        print(f"  {status}  {entry['source']}")


def cmd_bookmarklet(args, settings, canvas):
    print(build_bookmarklet())


def build_parser():
    parser = argparse.ArgumentParser(prog="preflight", description="Audit a submission against its Canvas instructions.")
    commands = parser.add_subparsers(dest="command", required=True)

    bookmarklet = commands.add_parser("bookmarklet", help="print the browser bookmark that exports Canvas data")
    bookmarklet.set_defaults(handler=cmd_bookmarklet)

    imported = commands.add_parser("import", help="read a file saved by the bookmarklet")
    imported.add_argument("export", type=Path, help="preflight_<course>_<assignment>.json or preflight_<course>_assignments.json")
    imported.add_argument("--assignment", type=int, help="with a course export: import this assignment instead of listing")
    imported.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    imported.set_defaults(handler=cmd_import)

    check = commands.add_parser("check", help="facts that need no judgment: dates, submission, files and git")
    check.add_argument("assignment_id", type=int, help="assignment id, already imported")
    check.add_argument("folder", type=Path, nargs="?", help="submission folder or repository; it is never written to")
    check.add_argument("--as-of", default="now", help="now (default), due (one minute before the deadline) or a local time like 2026-10-26T18:00")
    check.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    check.set_defaults(handler=cmd_check)

    audit = commands.add_parser("audit", help="checks plus the read-only audit agent")
    audit.add_argument("assignment_id", type=int, help="assignment id, already imported")
    audit.add_argument("folder", type=Path, help="submission folder or repository; it is never written to")
    audit.add_argument("--as-of", default="now", help="now (default), due (one minute before the deadline) or a local time")
    audit.add_argument("--model", default="opus", help="Claude model alias for the agent (default: opus)")
    audit.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    audit.set_defaults(handler=cmd_audit)

    cases = commands.add_parser("cases", help="run the audit on the real cases and score it against casos.yaml")
    cases.add_argument("cases", type=Path, help="cases file, e.g. casos/casos.yaml")
    cases.add_argument("--runs", type=int, default=2, help="audits per case (default 2)")
    cases.add_argument("--parallel", type=int, default=3, help="audits running at the same time (default 3)")
    cases.add_argument("--model", default="opus", help="Claude model alias (default: opus)")
    cases.add_argument("--only", nargs="*", help="case ids to run")
    cases.add_argument("--out", type=Path, help="work folder for the runs (default: <work>/casos)")
    cases.set_defaults(handler=cmd_cases)

    report = commands.add_parser("report", help="write the Spanish report from a saved audit")
    report.add_argument("assignment_id", type=int, help="assignment id, already audited")
    report.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    report.set_defaults(handler=cmd_report)

    extract = commands.add_parser("extract", help="convert a folder's docx, pptx and pdf files to text")
    extract.add_argument("folder", type=Path, help="folder or repository to read; it is never written to")
    extract.add_argument("--out", type=Path, help="output folder (default: <work>/extract/<folder name>)")
    extract.set_defaults(handler=cmd_extract)

    fetch = commands.add_parser("fetch", help="get an assignment through the Canvas API (needs a token)")
    fetch.add_argument("assignment", help="Canvas assignment URL, or an assignment id with --course")
    fetch.add_argument("--course", type=int, help="course id, when the assignment is given as an id")
    fetch.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    fetch.add_argument("--download", action="store_true", help="also download files linked in the description")
    fetch.set_defaults(handler=cmd_fetch)

    listing = commands.add_parser("list", help="list a course's assignments through the Canvas API (needs a token)")
    listing.add_argument("course", type=int, help="course id")
    listing.set_defaults(handler=cmd_list)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    needs_canvas = args.command in CANVAS_COMMANDS
    try:
        if args.command == "fetch":
            # Check the reference before settings, so a typo does not need a token to be reported.
            args.course_id, args.assignment_id = parse_assignment_ref(args.assignment, args.course)
        settings = load_settings(require_token=needs_canvas)
        canvas = Canvas(settings["CANVAS_BASE_URL"], settings["CANVAS_TOKEN"]) if needs_canvas else None
        args.handler(args, settings, canvas)
    except (ConfigError, CanvasError, ExportError, ExtractError, AuditError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
