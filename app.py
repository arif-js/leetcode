"""Vercel WSGI entrypoint for the dashboard."""

from __future__ import annotations

import json
import mimetypes
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.parse import unquote

from dashboard.dashboard import (
    DASHBOARD_DIR,
    ROOT,
    load_problems,
    load_profile_stats,
)


def response(start_response, status: str, body: bytes, content_type: str):
    start_response(
        status,
        [
            ("Content-Type", content_type),
            ("Content-Length", str(len(body))),
            ("X-Content-Type-Options", "nosniff"),
        ],
    )
    return [body]


def json_response(start_response, status: str, data: dict[str, object]):
    return response(
        start_response,
        status,
        json.dumps(data).encode("utf-8"),
        "application/json; charset=utf-8",
    )


def application(environ, start_response):
    path = unquote(environ.get("PATH_INFO", "/"))

    if path == "/api/problems":
        try:
            data = {
                "problems": load_problems(),
                "generatedAt": date.today().isoformat(),
            }
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError):
            return json_response(
                start_response,
                "503 Service Unavailable",
                {"error": "Dashboard problem data is unavailable."},
            )
        return json_response(start_response, "200 OK", data)

    if path == "/api/profile":
        try:
            stats = load_profile_stats()
        except (URLError, TimeoutError, json.JSONDecodeError, ValueError):
            return json_response(
                start_response,
                "502 Bad Gateway",
                {"error": "LeetCode profile stats are unavailable."},
            )
        return json_response(start_response, "200 OK", stats)

    if path == "/":
        path = "/dashboard.html"

    if path.startswith("/solutions/"):
        filename = path.removeprefix("/solutions/")
        if Path(filename).name != filename:
            return response(start_response, "404 Not Found", b"Not found", "text/plain")
        file_path = ROOT / filename
        if not file_path.is_file() or file_path.suffix not in {".js", ".py"}:
            return response(start_response, "404 Not Found", b"Not found", "text/plain")
    elif path in {"/dashboard.html", "/dashboard.css", "/dashboard.js"}:
        file_path = DASHBOARD_DIR / path.removeprefix("/")
    else:
        return response(start_response, "404 Not Found", b"Not found", "text/plain")

    try:
        body = file_path.read_bytes()
    except OSError:
        return response(start_response, "404 Not Found", b"Not found", "text/plain")
    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    if content_type.startswith("text/") or content_type in {
        "application/javascript",
        "application/json",
    }:
        content_type += "; charset=utf-8"
    return response(start_response, "200 OK", body, content_type)
