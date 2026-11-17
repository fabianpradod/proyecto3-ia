"""Canvas data saved from the logged-in browser by a bookmarklet, so no API token is needed."""

import json
from pathlib import Path
from urllib.parse import quote

FORMAT = "preflight-export/1"
KINDS = {"assignment", "course"}
SOURCE_PATH = Path(__file__).with_name("export.js")


class ExportError(Exception):
    pass


def export_source():
    return SOURCE_PATH.read_text(encoding="utf-8")


def build_bookmarklet():
    return "javascript:" + quote(export_source(), safe="")


def read_export(path, kind=None):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExportError(f"Could not read {path}: {error}") from None
    if not isinstance(data, dict) or data.get("format") != FORMAT or data.get("kind") not in KINDS:
        raise ExportError(f"{path} is not a pre-flight export (expected format {FORMAT}).")
    if kind and data["kind"] != kind:
        raise ExportError(f"{path} holds a {data['kind']} export; this needs a {kind} export.")
    return data
