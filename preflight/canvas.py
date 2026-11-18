"""Minimal read-only Canvas REST client. It only sends GET requests."""

import json
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

ASSIGNMENT_URL = re.compile(r"/courses/(\d+)/assignments/(\d+)")
STATUS_MESSAGES = {
    401: "Canvas rejected the token (401). It may be wrong or expired.",
    403: "Canvas denied access to {path} (403).",
    404: "Canvas has nothing at {path} (404).",
}


class CanvasError(Exception):
    pass


def parse_assignment_ref(ref, course=None):
    match = ASSIGNMENT_URL.search(ref)
    if match:
        return int(match[1]), int(match[2])
    if ref.isdigit() and course:
        return int(course), int(ref)
    raise ValueError("Give a Canvas assignment URL, or an assignment id together with --course.")


def safe_filename(file_id, name):
    base = Path(name.replace("\\", "/")).name.strip() or "file"
    return f"{file_id}_{base}"


def download_file(url, dest, allowed_host, session=None, timeout=60):
    host = urlparse(url).hostname
    if host != allowed_host:
        raise CanvasError(f"Refusing to download from {host}; only {allowed_host} is allowed.")
    name = Path(dest).name
    try:
        response = (session or requests.Session()).get(url, timeout=timeout, stream=True)
    except requests.RequestException as error:
        raise CanvasError(f"Could not download {name}: {type(error).__name__}.") from None
    if response.status_code >= 400:
        raise CanvasError(f"Download of {name} failed with HTTP {response.status_code}.")
    if "text/html" in response.headers.get("Content-Type", ""):
        raise CanvasError(f"Download of {name} returned a web page, probably the login page.")
    with open(dest, "wb") as handle:
        for chunk in response.iter_content(chunk_size=65536):
            handle.write(chunk)
    return dest


class Canvas:
    def __init__(self, base_url, token, session=None, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})

    def _url(self, path):
        return path if path.startswith("http") else f"{self.base_url}/api/v1{path}"

    def _request(self, url, params, path):
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as error:
            raise CanvasError(f"Could not reach Canvas for {path}: {type(error).__name__}.") from None
        if response.status_code in STATUS_MESSAGES:
            raise CanvasError(STATUS_MESSAGES[response.status_code].format(path=path))
        if response.status_code >= 400:
            raise CanvasError(f"Canvas returned HTTP {response.status_code} for {path}.")
        return response

    @staticmethod
    def _json(response):
        text = response.text
        if text.startswith("while(1);"):
            text = text[len("while(1);"):]
        return json.loads(text)

    def get(self, path, params=None):
        return self._json(self._request(self._url(path), params, path))

    def get_all(self, path, params=None):
        items, url, params = [], self._url(path), {**(params or {}), "per_page": 100}
        while url:
            response = self._request(url, params, path)
            items.extend(self._json(response))
            url = response.links.get("next", {}).get("url")
            params = None  # the next link already carries the query string
        return items

    def assignment(self, course_id, assignment_id):
        return self.get(f"/courses/{course_id}/assignments/{assignment_id}")

    def my_submission(self, course_id, assignment_id):
        return self.get(
            f"/courses/{course_id}/assignments/{assignment_id}/submissions/self",
            params={"include[]": ["submission_comments"]},
        )

    def assignments(self, course_id):
        return self.get_all(f"/courses/{course_id}/assignments", {"include[]": ["submission"], "order_by": "due_at"})

    def file_info(self, file_id):
        return self.get(f"/files/{file_id}")

    def download(self, url, dest):
        return download_file(url, dest, urlparse(self.base_url).hostname, session=self.session, timeout=self.timeout)
