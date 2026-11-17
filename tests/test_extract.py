import zipfile

import pytest

from preflight.extract import ExtractError, docx_text, extract_folder, pdf_text, pptx_text

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
REL = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'


def make_zip(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return path


def make_docx(path, body, prolog=""):
    return make_zip(path, {"word/document.xml": f'{prolog}<w:document {W}><w:body>{body}</w:body></w:document>'})


def para(text, style=None):
    props = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{props}<w:r><w:t>{text}</w:t></w:r></w:p>"


def slide(*texts):
    paras = "".join(f"<a:p><a:r><a:t>{t}</a:t></a:r></a:p>" for t in texts)
    return f'<p:sld {A} {P}><p:cSld><p:spTree><p:sp><p:txBody>{paras}</p:txBody></p:sp></p:spTree></p:cSld></p:sld>'


def notes(text):
    return (
        f'<p:notes {A} {P}><p:cSld><p:spTree>'
        '<p:sp><p:nvSpPr><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>1</a:t></a:r></a:p></p:txBody></p:sp>'
        f'<p:sp><p:nvSpPr><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>'
        '</p:spTree></p:cSld></p:notes>'
    )


def make_pptx(path):
    rels = (
        f'<Relationships {REL}><Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" '
        'Target="../notesSlides/notesSlide7.xml"/></Relationships>'
    )
    return make_zip(path, {
        "ppt/slides/slide1.xml": slide("Clustering", "K-means"),
        "ppt/slides/slide2.xml": slide("Metodo del codo"),
        "ppt/slides/slide10.xml": slide("Conclusiones"),
        "ppt/slides/_rels/slide1.xml.rels": rels,
        "ppt/notesSlides/notesSlide7.xml": notes("Explicar la inercia"),
    })


def make_pdf(path, text):
    stream = f"BT /F1 18 Tf 20 100 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R"
        b" /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    path.write_bytes(out)
    return path


def test_docx_keeps_headings_paragraphs_and_table_rows(tmp_path):
    table = (
        "<w:tbl><w:tr><w:tc>" + para("Modelo") + "</w:tc><w:tc>" + para("F1") + "</w:tc></w:tr>"
        "<w:tr><w:tc>" + para("XGBoost") + "</w:tc><w:tc>" + para("0.91") + "</w:tc></w:tr></w:tbl>"
    )
    body = para("Resultados", "Heading1") + "<w:p><w:r><w:t>Hola </w:t></w:r><w:r><w:t>mundo</w:t></w:r></w:p>" + table
    assert docx_text(make_docx(tmp_path / "a.docx", body)).splitlines() == [
        "# Resultados", "Hola mundo", "Modelo | F1", "XGBoost | 0.91",
    ]


def test_docx_does_not_expand_external_entities(tmp_path):
    prolog = '<?xml version="1.0"?><!DOCTYPE w:document [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
    path = make_docx(tmp_path / "xxe.docx", "<w:p><w:r><w:t>a&x;b</w:t></w:r></w:p>", prolog=prolog)
    assert "root" not in docx_text(path)


def test_pptx_without_presentation_xml_orders_slides_numerically_and_adds_notes(tmp_path):
    assert pptx_text(make_pptx(tmp_path / "deck.pptx")).splitlines() == [
        "## Slide 1", "Clustering", "K-means", "Notes: Explicar la inercia",
        "## Slide 2", "Metodo del codo",
        "## Slide 3", "Conclusiones",
    ]


def test_pptx_follows_the_order_in_presentation_xml(tmp_path):
    # After reordering slides in PowerPoint, file names no longer match the shown order.
    path = make_pptx(tmp_path / "deck.pptx")
    r = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    presentation = f'<p:presentation {P} {r}><p:sldIdLst><p:sldId id="256" r:id="rId9"/><p:sldId id="257" r:id="rId3"/></p:sldIdLst></p:presentation>'
    rels = (
        f'<Relationships {REL}>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>'
        '<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide10.xml"/>'
        '</Relationships>'
    )
    with zipfile.ZipFile(path, "a") as archive:
        archive.writestr("ppt/presentation.xml", presentation)
        archive.writestr("ppt/_rels/presentation.xml.rels", rels)
    lines = pptx_text(path).splitlines()
    assert lines[:2] == ["## Slide 1", "Conclusiones"]
    assert lines[2:4] == ["## Slide 2", "Clustering"]
    assert "Metodo del codo" not in lines  # slide2.xml is not in the presentation: hidden or deleted


def test_pdf_text_is_split_by_page(tmp_path):
    text = pdf_text(make_pdf(tmp_path / "doc.pdf", "Hola PDF"))
    assert text.splitlines()[0] == "## Page 1"
    assert "Hola PDF" in text


def test_oversized_member_is_refused(tmp_path):
    path = make_docx(tmp_path / "big.docx", para("x" * 5000))
    with pytest.raises(ExtractError):
        docx_text(path, max_bytes=1000)


def test_not_a_zip_is_an_extract_error(tmp_path):
    path = tmp_path / "broken.docx"
    path.write_bytes(b"not a zip")
    with pytest.raises(ExtractError):
        docx_text(path)


def test_extract_folder_mirrors_tree_outside_the_source(tmp_path):
    source = tmp_path / "entrega"
    (source / "docs").mkdir(parents=True)
    (source / ".git").mkdir()
    make_docx(source / "docs" / "informe.docx", para("Informe"))
    make_pptx(source / "deck.pptx")
    make_pdf(source / "anexo.pdf", "Anexo")
    make_docx(source / ".git" / "ignored.docx", para("no"))
    (source / "broken.docx").write_bytes(b"not a zip")
    (source / "notes.md").write_text("plain text is read directly", encoding="utf-8")
    before = sorted(p.relative_to(source) for p in source.rglob("*"))

    out = tmp_path / "out"
    manifest = {entry["source"]: entry for entry in extract_folder(source, out)}

    assert sorted(p.relative_to(source) for p in source.rglob("*")) == before
    assert set(manifest) == {"docs/informe.docx", "deck.pptx", "anexo.pdf", "broken.docx"}
    assert (out / "docs" / "informe.docx.txt").read_text(encoding="utf-8") == "Informe\n"
    assert manifest["docs/informe.docx"]["text"] == "docs/informe.docx.txt"
    assert manifest["deck.pptx"]["chars"] > 0
    assert "error" in manifest["broken.docx"] and "text" not in manifest["broken.docx"]


def test_extract_refuses_an_output_folder_inside_the_audited_folder(tmp_path):
    source = tmp_path / "entrega"
    source.mkdir()
    with pytest.raises(ExtractError):
        extract_folder(source, source / "work")
    assert list(source.iterdir()) == []
