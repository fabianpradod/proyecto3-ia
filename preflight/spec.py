"""Turn a Canvas description (HTML) into numbered lines that findings can cite."""

import re
import unicodedata

from bs4 import BeautifulSoup, Comment, NavigableString

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCKS = HEADINGS | {
    "address", "article", "aside", "blockquote", "caption", "dd", "div", "dl", "dt",
    "figcaption", "figure", "footer", "header", "hr", "li", "main", "nav", "ol", "p",
    "pre", "section", "table", "tbody", "tfoot", "thead", "ul",
}
SKIP = {"script", "style", "noscript", "colgroup", "col"}
FILE_PATH = re.compile(r"/files/(\d+)")
NUMBER = re.compile(r"^\d+(?:[.,]\d+)?$")


def normalize(text):
    # NFC because Canvas mixes composed and decomposed accents, which breaks exact quote matching.
    text = unicodedata.normalize("NFC", text.replace("\xa0", " "))
    return re.sub(r"\s+", " ", text).strip()


def html_to_lines(html):
    soup = BeautifulSoup(html or "", "lxml")
    lines = []
    _walk(soup.body or soup, lines, "")
    return lines


def _marker(tag_name):
    if tag_name in HEADINGS:
        return "# "
    if tag_name == "li":
        return "- "
    return ""


def _walk(node, lines, marker):
    # Inline content accumulates into one line; block tags, <br> and table rows end it.
    buffer = []

    def flush():
        text = normalize("".join(buffer))
        buffer.clear()
        if text:
            lines.append(marker + text)

    def visit(parent):
        for child in parent.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, NavigableString):
                buffer.append(str(child))
            elif child.name in SKIP:
                continue
            elif child.name == "br":
                flush()
            elif child.name == "tr":
                flush()
                cells = [normalize(cell.get_text(" ")) for cell in child.find_all(["td", "th"], recursive=False)]
                row = " | ".join(cell for cell in cells if cell)
                if row:
                    lines.append(row)
            elif child.name in BLOCKS:
                flush()
                _walk(child, lines, _marker(child.name))
            else:
                visit(child)

    visit(node)
    flush()


def number_lines(lines):
    return [(f"L{index:03d}", text) for index, text in enumerate(lines, start=1)]


def find_point_rows(numbered):
    rows = []
    for line_id, text in numbered:
        cells = [cell.strip() for cell in text.split(" | ")]
        if len(cells) < 2 or not NUMBER.match(cells[-1]):
            continue
        points = float(cells[-1].replace(",", "."))
        criterion = " | ".join(cells[:-1])
        rows.append({
            "line": line_id,
            "criterion": criterion,
            "points": int(points) if points.is_integer() else points,
            "is_total": criterion.lower().startswith("total"),
        })
    return rows


def _canvas_file_id(link):
    target = link.get("data-api-endpoint") or link.get("href") or ""
    match = FILE_PATH.search(target)
    if not match:
        return None
    is_canvas = (
        link.get("data-api-returntype") == "File"
        or "instructure_file_link" in (link.get("class") or [])
        or target.startswith("/")
    )
    return int(match[1]) if is_canvas else None


def find_linked_files(html):
    files, seen = [], set()
    for link in BeautifulSoup(html or "", "lxml").find_all("a"):
        file_id = _canvas_file_id(link)
        if file_id is None or file_id in seen:
            continue
        seen.add(file_id)
        files.append({"id": file_id, "name": normalize(link.get("title") or link.get_text())})
    return files


def find_links(html):
    links = []
    for link in BeautifulSoup(html or "", "lxml").find_all("a", href=True):
        href = link["href"]
        if _canvas_file_id(link) is not None or href.startswith(("#", "mailto:")):
            continue
        links.append({"text": normalize(link.get_text()), "href": href})
    return links
