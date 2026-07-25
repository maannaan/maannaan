#!/usr/bin/env python3
"""
Fetch recent public GitHub events for GITHUB_USER and rewrite the
<!-- START_SECTION:ops_log --> … <!-- END_SECTION:ops_log --> block in README.md.

Uses GITHUB_TOKEN when present (Actions) for higher rate limits; works
unauthenticated for public events otherwise.
"""
import datetime
import os
import re
import sys

import requests

from profile_config import GITHUB_USER

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, "..", "README.md")
START = "<!-- START_SECTION:ops_log -->"
END = "<!-- END_SECTION:ops_log -->"
MAX_LINES = 8

SKIP_TYPES = {
    "WatchEvent",
    "ForkEvent",
    "SponsorshipEvent",
    "MemberEvent",
}


def headers():
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "maannaan-profile-ops-log",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fmt_date(iso):
    try:
        dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return iso[:10] if iso else "????-??-??"


def describe(event):
    etype = event.get("type")
    if etype in SKIP_TYPES:
        return None

    repo = (event.get("repo") or {}).get("name", "unknown")
    date = fmt_date(event.get("created_at", ""))
    payload = event.get("payload") or {}

    if etype == "PushEvent":
        n = payload.get("size") or len(payload.get("commits") or [])
        if n and n > 1:
            return f"{date} · pushed {n} commits to {repo}"
        return f"{date} · pushed to {repo}"

    if etype == "CreateEvent":
        ref_type = payload.get("ref_type", "ref")
        ref = payload.get("ref")
        if ref_type == "repository":
            return f"{date} · created repository {repo}"
        if ref:
            return f"{date} · created {ref_type} {ref} on {repo}"
        return f"{date} · created {ref_type} on {repo}"

    if etype == "DeleteEvent":
        ref_type = payload.get("ref_type", "ref")
        ref = payload.get("ref", "")
        return f"{date} · deleted {ref_type} {ref} on {repo}".rstrip()

    if etype == "PullRequestEvent":
        action = payload.get("action", "updated")
        pr = payload.get("pull_request") or {}
        num = pr.get("number") or payload.get("number")
        if action == "closed" and pr.get("merged"):
            action = "merged"
        if num:
            return f"{date} · {action} PR #{num} on {repo}"
        return f"{date} · {action} PR on {repo}"

    if etype == "IssuesEvent":
        action = payload.get("action", "updated")
        issue = payload.get("issue") or {}
        num = issue.get("number")
        if num:
            return f"{date} · {action} issue #{num} on {repo}"
        return f"{date} · {action} issue on {repo}"

    if etype == "IssueCommentEvent":
        issue = payload.get("issue") or {}
        num = issue.get("number")
        if num:
            return f"{date} · commented on issue #{num} in {repo}"
        return f"{date} · commented on {repo}"

    if etype == "PullRequestReviewEvent":
        pr = payload.get("pull_request") or {}
        num = pr.get("number")
        if num:
            return f"{date} · reviewed PR #{num} on {repo}"
        return f"{date} · reviewed PR on {repo}"

    if etype == "ReleaseEvent":
        release = payload.get("release") or {}
        tag = release.get("tag_name", "release")
        return f"{date} · published {tag} on {repo}"

    if etype == "PublicEvent":
        return f"{date} · open-sourced {repo}"

    if etype == "CommitCommentEvent":
        return f"{date} · commented on a commit in {repo}"

    # Unknown but useful-enough fallback
    nice = etype.replace("Event", "") if etype else "activity"
    return f"{date} · {nice} on {repo}"


def fetch_lines():
    url = f"https://api.github.com/users/{GITHUB_USER}/events/public"
    resp = requests.get(url, headers=headers(), params={"per_page": 30}, timeout=30)
    resp.raise_for_status()
    events = resp.json()
    if not isinstance(events, list):
        print("unexpected API response", file=sys.stderr)
        sys.exit(1)

    lines = []
    seen = set()
    for event in events:
        text = describe(event)
        if not text or text in seen:
            continue
        seen.add(text)
        lines.append(f"- `{text}`")
        if len(lines) >= MAX_LINES:
            break

    if not lines:
        lines = ["- `_no recent public activity_`"]
    return lines


def rewrite_readme(lines):
    with open(README, encoding="utf-8") as f:
        content = f.read()

    if START not in content or END not in content:
        print(f"missing {START} / {END} markers in README.md", file=sys.stderr)
        sys.exit(1)

    block = START + "\n" + "\n".join(lines) + "\n" + END
    updated, n = re.subn(
        re.escape(START) + r".*?" + re.escape(END),
        block,
        content,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        print("failed to rewrite ops_log section", file=sys.stderr)
        sys.exit(1)

    with open(README, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"wrote {len(lines)} ops log lines into {README}")


if __name__ == "__main__":
    rewrite_readme(fetch_lines())
