"""Refresh the dashboard's Git-date snapshot for deployments without .git."""

import json

from dashboard.dashboard import DASHBOARD_DIR, load_problems, solution_addition_dates


def main() -> None:
    all_dates = solution_addition_dates()
    dates = {
        str(problem["filename"]): all_dates[str(problem["filename"])]
        for problem in load_problems()
        if problem["filename"] in all_dates
    }
    snapshot = DASHBOARD_DIR / "solution-dates.json"
    snapshot.write_text(
        json.dumps(dates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {snapshot.relative_to(DASHBOARD_DIR.parent)} with {len(dates)} dates.")


if __name__ == "__main__":
    main()
