"""Convert docx, pptx and pdf files to plain text the audit agent can read and search.

Text always goes to a separate folder; the audited folder is never written to.
"""

import posixpath
import re
import zipfile
from pathlib import Path

from lxml import etree
from pypdf import PdfReader

from .spec import normalize

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
NOTES_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
SLIDE_FILE = re.compile(r"ppt/slides/slide(\d+)\.xml$")
# Word style ids for headings; Spanish Word stores "Titulo 1" as "Ttulo1".
HEADING_STYLES = ("heading", "title", "titulo", "ttulo")
SKIP_DIRS = {"node_modules", "__pycache__", "venv"}
MAX_BYTES = 50 * 1024 * 1024

# Office files are untrusted input: never resolve entities or reach the network while parsing.
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


class ExtractError(Exception):
    pass


def _open_zip(path):
    try:
        return zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as error:
        raise ExtractError(f"not a readable Office file ({error})") from None


def _parse(archive, name, max_bytes):
    info = archive.getinfo(name)
    if info.file_size > max_bytes:
        raise ExtractError(f"{name} unpacks to {info.file_size} bytes, over the {max_bytes} byte limit")
    try:
        return etree.fromstring(archive.read(name), PARSER)
    except etree.XMLSyntaxError as error:
        raise ExtractError(f"{name} is not valid XML ({error})") from None


def _lines_to_text(lines):
    return "\n".join(lines) + "\n" if lines else ""


# Word

def _word_paragraph(paragraph):
    parts = []
    for node in paragraph.iter():
        if node.tag == W + "t" and node.text:
            parts.append(node.text)
        elif node.tag in (W + "tab", W + "br", W + "cr"):
            parts.append(" ")
    return normalize("".join(parts))


def _is_heading(paragraph):
    style = paragraph.find(f"{W}pPr/{W}pStyle")
    value = (style.get(W + "val") or "").lower() if style is not None else ""
    return value.startswith(HEADING_STYLES)


def _word_blocks(parent, lines):
    for child in parent:
        if child.tag == W + "p":
            text = _word_paragraph(child)
            if text:
                lines.append(("# " if _is_heading(child) else "") + text)
        elif child.tag == W + "tbl":
            for row in child.findall(W + "tr"):
                cells = [" ".join(filter(None, map(_word_paragraph, cell.iter(W + "p")))) for cell in row.findall(W + "tc")]
                row_text = " | ".join(cell for cell in cells if cell)
                if row_text:
                    lines.append(row_text)
        elif child.tag == W + "sdt":
            content = child.find(W + "sdtContent")
            if content is not None:
                _word_blocks(content, lines)


def docx_text(path, max_bytes=MAX_BYTES):
    with _open_zip(path) as archive:
        if "word/document.xml" not in archive.namelist():
            raise ExtractError("no word/document.xml inside")
        root = _parse(archive, "word/document.xml", max_bytes)
    lines = []
    body = root.find(W + "body")
    if body is not None:
        _word_blocks(body, lines)
    return _lines_to_text(lines)


# PowerPoint

def _drawing_paragraphs(element):
    lines = []
    for paragraph in element.iter(A + "p"):
        text = normalize("".join(node.text or "" for node in paragraph.iter(A + "t")))
        if text:
            lines.append(text)
    return lines


def _resolve(base_dir, target):
    return target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base_dir, target))


def _slide_names(archive, max_bytes):
    names = set(archive.namelist())
    if {"ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"} <= names:
        rels = _parse(archive, "ppt/_rels/presentation.xml.rels", max_bytes)
        targets = {rel.get("Id"): rel.get("Target", "") for rel in rels.iter(REL + "Relationship")}
        ordered = []
        for slide_id in _parse(archive, "ppt/presentation.xml", max_bytes).iter(P + "sldId"):
            name = _resolve("ppt", targets.get(slide_id.get(R + "id"), ""))
            if name in names:
                ordered.append(name)
        if ordered:
            return ordered
    numbered = sorted((int(match[1]), name) for name in names if (match := SLIDE_FILE.match(name)))
    return [name for _, name in numbered]


def _notes_for(archive, slide_name, max_bytes):
    rels_name = posixpath.join(posixpath.dirname(slide_name), "_rels", posixpath.basename(slide_name) + ".rels")
    if rels_name not in archive.namelist():
        return []
    for rel in _parse(archive, rels_name, max_bytes).iter(REL + "Relationship"):
        notes_name = _resolve(posixpath.dirname(slide_name), rel.get("Target", ""))
        if rel.get("Type") == NOTES_REL and notes_name in archive.namelist():
            lines = []
            for shape in _parse(archive, notes_name, max_bytes).iter(P + "sp"):
                placeholder = shape.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
                if placeholder is not None and placeholder.get("type") == "body":
                    lines.extend(_drawing_paragraphs(shape))
            return lines
    return []


def pptx_text(path, max_bytes=MAX_BYTES):
    lines = []
    with _open_zip(path) as archive:
        for position, name in enumerate(_slide_names(archive, max_bytes), start=1):
            lines.append(f"## Slide {position}")
            lines.extend(_drawing_paragraphs(_parse(archive, name, max_bytes)))
            notes = _notes_for(archive, name, max_bytes)
            if notes:
                lines.append("Notes: " + " ".join(notes))
    return _lines_to_text(lines)


# PDF

def pdf_text(path, max_bytes=MAX_BYTES):
    if Path(path).stat().st_size > max_bytes:
        raise ExtractError(f"over the {max_bytes} byte limit")
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            raise ExtractError("the PDF is encrypted")
        lines = []
        for number, page in enumerate(reader.pages, start=1):
            lines.append(f"## Page {number}")
            lines.extend(text for text in map(normalize, (page.extract_text() or "").splitlines()) if text)
    except ExtractError:
        raise
    except Exception as error:  # pypdf raises many types on malformed input
        raise ExtractError(f"could not read the PDF ({type(error).__name__})") from None
    return _lines_to_text(lines)


# Folders

EXTRACTORS = {".docx": docx_text, ".pptx": pptx_text, ".pdf": pdf_text}


def iter_files(folder):
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder)
        if any(part.startswith(".") or part in SKIP_DIRS for part in relative.parts[:-1]):
            continue
        if path.is_file():
            yield path, relative


def extract_folder(folder, out_dir, max_bytes=MAX_BYTES):
    folder, out_dir = Path(folder).resolve(), Path(out_dir).resolve()
    if out_dir == folder or folder in out_dir.parents:
        raise ExtractError(f"the output folder {out_dir} is inside the audited folder; pick one outside it")
    manifest = []
    for path, relative in iter_files(folder):
        extractor = EXTRACTORS.get(path.suffix.lower())
        if extractor is None or path.name.startswith("~$"):  # ~$ files are Office lock files
            continue
        entry = {"source": relative.as_posix()}
        try:
            text = extractor(path, max_bytes=max_bytes)
        except ExtractError as error:
            entry["error"] = str(error)
        else:
            target = out_dir / (relative.as_posix() + ".txt")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            entry.update(text=relative.as_posix() + ".txt", chars=len(text))
        manifest.append(entry)
    return manifest
