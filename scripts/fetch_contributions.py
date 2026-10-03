"""Fetch live GitHub contribution/stat data for the profile README."""
import json, os, sys
from datetime import date, datetime, timezone
from pathlib import Path
import requests

DEFAULT_USERNAME = "lokendra-s64"
OUT_PATH = Path("data/contributions.json")
API = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    name
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      restrictedContributionsCount
    }
    repositories(ownerAffiliations: OWNER, first: 100, privacy: PUBLIC) {
      nodes { stargazerCount }
    }
  }
}
"""

LEVELS = {"NONE":0, "FIRST_QUARTILE":1, "SECOND_QUARTILE":2,
          "THIRD_QUARTILE":3, "FOURTH_QUARTILE":4}

def fetch(username):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required in GitHub Actions.")
    r = requests.post(
        API,
        json={"query": QUERY, "variables": {"login": username}},
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        timeout=30,
    )
    r.raise_for_status()
    payload = r.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]

def compute_streak(days):
    ordered = sorted(days, key=lambda x: x["date"])
    longest = running = 0
    for d in ordered:
        if d["count"] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    current = 0
    today = date.today().isoformat()
    for d in reversed(ordered):
        if d["date"] > today:
            continue
        if d["count"] > 0:
            current += 1
        else:
            break
    return current, longest

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_USERNAME", DEFAULT_USERNAME)
    user = fetch(username)
    cc = user["contributionsCollection"]
    calendar = cc["contributionCalendar"]
    days = []
    for week in calendar["weeks"]:
        for d in week["contributionDays"]:
            days.append({
                "date": d["date"],
                "level": LEVELS.get(d["contributionLevel"], 0),
                "count": d["contributionCount"],
            })
    current, longest = compute_streak(days)
    stars = sum(n["stargazerCount"] for n in user["repositories"]["nodes"])
    payload = {
        "username": username,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": sorted(days, key=lambda x: x["date"]),
        "total_contributions": calendar["totalContributions"],
        "current_streak": current,
        "longest_streak": longest,
        "commits": cc["totalCommitContributions"],
        "pull_requests": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "stars": stars,
        "restricted_contributions": cc["restrictedContributionsCount"],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("Updated", OUT_PATH)

if __name__ == "__main__":
    main()
