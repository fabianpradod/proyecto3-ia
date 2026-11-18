import json

import pytest

from preflight.canvas import Canvas, CanvasError, parse_assignment_ref, safe_filename


class FakeResponse:
    def __init__(self, status_code, payload, next_url=None, prefix=""):
        self.status_code = status_code
        self.text = prefix + json.dumps(payload)
        self.links = {"next": {"url": next_url}} if next_url else {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.headers = {}
        self.calls = []

    def get(self, url, params=None, timeout=None, stream=False):
        self.calls.append((url, params))
        return self.responses.pop(0)


def test_parse_assignment_url():
    url = "https://uvg.instructure.com/courses/46981/assignments/959073?return_to=x"
    assert parse_assignment_ref(url) == (46981, 959073)


def test_parse_bare_id_needs_course():
    assert parse_assignment_ref("959073", course=46981) == (46981, 959073)
    with pytest.raises(ValueError):
        parse_assignment_ref("959073")


def test_get_all_follows_next_links():
    session = FakeSession([
        FakeResponse(200, [{"id": 1}], next_url="https://x.test/api/v1/page2"),
        FakeResponse(200, [{"id": 2}]),
    ])
    canvas = Canvas("https://x.test", "secret-token", session=session)
    assert [item["id"] for item in canvas.get_all("/courses/1/assignments")] == [1, 2]
    assert session.calls[0][0] == "https://x.test/api/v1/courses/1/assignments"
    assert session.calls[1] == ("https://x.test/api/v1/page2", None)


def test_rejected_token_error_does_not_leak_the_token():
    canvas = Canvas("https://x.test", "secret-token", session=FakeSession([FakeResponse(401, {})]))
    with pytest.raises(CanvasError) as error:
        canvas.get("/courses/1")
    assert "401" in str(error.value)
    assert "secret-token" not in str(error.value)


def test_token_goes_in_the_header_only():
    session = FakeSession([FakeResponse(200, {"ok": True})])
    Canvas("https://x.test", "secret-token", session=session).get("/courses/1")
    assert session.headers["Authorization"] == "Bearer secret-token"
    assert "secret-token" not in session.calls[0][0]


def test_while_prefix_is_stripped():
    session = FakeSession([FakeResponse(200, {"ok": True}, prefix="while(1);")])
    assert Canvas("https://x.test", "t", session=session).get("/x") == {"ok": True}


def test_safe_filename_drops_path_parts():
    assert safe_filename(7, "../../etc/passwd") == "7_passwd"
    assert safe_filename(7, "Informe final.docx") == "7_Informe final.docx"
