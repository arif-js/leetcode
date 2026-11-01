#!/usr/bin/env python3
"""Serve a local dashboard for the solutions listed in README.md."""

from __future__ import annotations

import json
import mimetypes
import re
import subprocess
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
LEETCODE_USERNAME = "arif_-_ul_-"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


PROFILE_QUERY = """
query userProfile($username: String!, $year: Int) {
  matchedUser(username: $username) {
    submitStats { acSubmissionNum { difficulty count } }
    languageProblemCount { languageName problemsSolved }
    userCalendar(year: $year) { totalActiveDays streak submissionCalendar }
  }
  recentAcSubmissionList(username: $username, limit: 20) {
    title
    titleSlug
    timestamp
    lang
  }
}
"""


def load_profile_stats() -> dict[str, object]:
    query = {
        "query": PROFILE_QUERY,
        "variables": {"username": LEETCODE_USERNAME, "year": date.today().year},
    }
    request = Request(
        "https://leetcode.com/graphql/",
        data=json.dumps(query).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/",
            "User-Agent": "curl/8.7.1",
        },
        method="POST",
    )
    with urlopen(request, timeout=10) as response:
        payload = json.load(response)

    try:
        user = payload["data"]["matchedUser"]
        counts = {
            entry["difficulty"]: entry["count"]
            for entry in user["submitStats"]["acSubmissionNum"]
        }
        stats: dict[str, object] = {
            "all": counts["All"],
            "easy": counts["Easy"],
            "medium": counts["Medium"],
            "hard": counts["Hard"],
        }
    except (KeyError, TypeError) as error:
        raise ValueError("LeetCode profile stats were unavailable.") from error

    # The rest is nice to have: a missing field should not sink the whole card.
    languages = user.get("languageProblemCount") or []
    stats["languages"] = sorted(
        (
            {"name": entry["languageName"], "solved": entry["problemsSolved"]}
            for entry in languages
            if entry.get("languageName") and entry.get("problemsSolved")
        ),
        key=lambda entry: (-entry["solved"], entry["name"]),
    )

    calendar = (user.get("userCalendar") or {}).get("submissionCalendar")
    stats["calendar"] = parse_submission_calendar(calendar)
    stats["activeDays"] = (user.get("userCalendar") or {}).get("totalActiveDays")
    stats["streak"] = (user.get("userCalendar") or {}).get("streak")

    recent = payload["data"].get("recentAcSubmissionList") or []
    stats["recent"] = [
        {
            "title": entry["title"],
            "url": f"https://leetcode.com/problems/{entry['titleSlug']}/",
            "lang": entry.get("lang"),
            "solvedAt": timestamp_to_date(entry.get("timestamp")),
        }
        for entry in recent
        if entry.get("title") and entry.get("titleSlug")
    ]

    return stats


def timestamp_to_date(timestamp: str | int | None) -> str | None:
    """Turn a LeetCode epoch-second timestamp into an ISO date."""
    try:
        return date.fromtimestamp(int(timestamp)).isoformat()
    except (TypeError, ValueError, OSError, OverflowError):
        return None


def parse_submission_calendar(raw: str | None) -> dict[str, int]:
    """Collapse LeetCode's per-day submission calendar into per-month totals."""
    if not raw:
        return {}
    try:
        per_day = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {}

    months: dict[str, int] = {}
    for timestamp, count in per_day.items():
        day = timestamp_to_date(timestamp)
        if not day or not isinstance(count, int):
            continue
        months[day[:7]] = months.get(day[:7], 0) + count
    return months


def solution_addition_dates() -> dict[str, str]:
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--format=%cs",
                "--name-only",
                "--",
                "*.js",
                "*.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        snapshot = DASHBOARD_DIR / "solution-dates.json"
        if not snapshot.is_file():
            raise RuntimeError(
                "Git history is unavailable and dashboard/solution-dates.json is missing."
            )
        dates = json.loads(snapshot.read_text(encoding="utf-8"))
        if not isinstance(dates, dict) or not all(
            isinstance(filename, str)
            and isinstance(value, str)
            and DATE_PATTERN.fullmatch(value)
            for filename, value in dates.items()
        ):
            raise ValueError("dashboard/solution-dates.json contains invalid dates.")
        return dates

    dates: dict[str, str] = {}
    current_date: str | None = None

    for line in result.stdout.splitlines():
        if DATE_PATTERN.fullmatch(line):
            current_date = line
        elif line and current_date:
            dates.setdefault(line, current_date)

    return dates


def load_problems() -> list[dict[str, str | None]]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    addition_dates = solution_addition_dates()
    problems: list[dict[str, str | None]] = []

    for line in readme.splitlines():
        if not line.startswith("|") or "./" not in line:
            continue

        solution_match = re.search(r"\]\(\./([^)]*)\)", line)
        leetcode_match = re.search(r"\[Link\]\((https://leetcode\.com/[^)]*)\)", line)
        if not solution_match or not leetcode_match:
            continue

        filename = solution_match.group(1)
        if Path(filename).name != filename or not (ROOT / filename).is_file():
            continue

        title = line[1:].split("|", maxsplit=1)[0].strip()
        problems.append(
            {
                "title": title,
                "filename": filename,
                "language": Path(filename).suffix.removeprefix(".").upper(),
                "solvedAt": addition_dates.get(filename),
                "leetcodeUrl": leetcode_match.group(1),
            }
        )

    return problems


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def send_json(self, status: int, data: dict[str, object]) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/problems":
            self.send_json(
                200,
                {"problems": load_problems(), "generatedAt": date.today().isoformat()},
            )
            return

        if route == "/api/profile":
            try:
                self.send_json(200, load_profile_stats())
            except (URLError, TimeoutError, json.JSONDecodeError, ValueError):
                self.send_json(502, {"error": "LeetCode profile stats are unavailable."})
            return

        if route.startswith("/solutions/"):
            filename = unquote(route.removeprefix("/solutions/"))
            if Path(filename).name != filename:
                self.send_error(404)
                return
            solution = ROOT / filename
            if not solution.is_file() or solution.suffix not in {".js", ".py"}:
                self.send_error(404)
                return
            payload = solution.read_bytes()
            self.send_response(200)
            content_type = mimetypes.guess_type(solution.name)[0] or "application/octet-stream"
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if route == "/":
            self.path = "/dashboard.html"
        super().do_GET()


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DashboardHandler)
    print("LeetCode dashboard: http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
