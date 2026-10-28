#!/usr/bin/env python3
"""Minimal loopback adapter: submit tasks and record approval intent only."""
import json
import sys
import urllib.error
import urllib.request

API_BASE = "http://127.0.0.1:18082"


def post(path, payload):
    body = json.dumps(payload).encode()
    request = urllib.request.Request(
        API_BASE + path,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def submit(kind, summary, approval_kind=None, approval_summary=None):
    task = post("/tasks", {"kind": kind, "input_summary": summary})
    result = {"task": task}
    if approval_kind:
        result["approval"] = post(
            "/approvals",
            {
                "task_id": task["id"],
                "action_kind": approval_kind,
                "summary": approval_summary or summary,
            },
        )
    return result


if __name__ == "__main__":
    if len(sys.argv) not in (3, 5):
        print("usage: openclaw_task_adapter.py KIND SUMMARY [APPROVAL_KIND APPROVAL_SUMMARY]", file=sys.stderr)
        raise SystemExit(2)
    try:
        print(json.dumps(submit(*sys.argv[1:]), indent=2))
    except urllib.error.HTTPError as exc:
        print(f"adapter_http_error={exc.code}", file=sys.stderr)
        raise SystemExit(1)

