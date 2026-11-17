"""Command line entry point: python -m preflight <command>."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .canvas import Canvas, CanvasError, parse_assignment_ref
from .config import ConfigError, load_settings
from .export import ExportError, build_bookmarklet, read_export
from .extract import ExtractError, extract_folder
from .fetch import assignment_rows, fetch_assignment, import_assignment

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
        print_rows(assignment_rows(export["assignments"], tz, datetime.now(timezone.utc)))
        return
    meta, out_dir = import_assignment(export, work_root(args, settings), tz, search_dir=args.export.parent)
    print_summary(meta, out_dir, tz)


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
    imported.add_argument("--out", type=Path, help="work folder (default: PREFLIGHT_WORK, ~/.cache/preflight)")
    imported.set_defaults(handler=cmd_import)

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
    except (ConfigError, CanvasError, ExportError, ExtractError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
