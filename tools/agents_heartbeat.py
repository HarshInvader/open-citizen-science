#!/usr/bin/env python3
"""Tell the site which of our agents are working, so the live count on the home page is right.

Usage: python3 -I tools/agents_heartbeat.py <kind>:<project>:<id> [...]
  kind = core | subagent, project = mind | origins | indus, id = a stable id (e.g. the T3 thread id, hashed below).
  Add --done to mark them finished.
Reads the token from .local/agent_token (gitignored). Sends only ids and project names.
"""
import hashlib, json, sys, urllib.request
from pathlib import Path

URL = "https://opencitizenscience.org/api/agents"
TOKEN = (Path(__file__).resolve().parent.parent / ".local" / "agent_token").read_text().strip()
done = "--done" in sys.argv
for arg in [a for a in sys.argv[1:] if a != "--done"]:
    kind, project, raw = arg.split(":", 2)
    sid = hashlib.sha256(raw.encode()).hexdigest()[:32]  # never send the raw thread id
    body = dict(id=sid, kind=kind, project=project, **({"status": "done"} if done else {}))
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}", "User-Agent": "open-research-site/1.0"})
    try:
        print(arg.split(":")[0], project, urllib.request.urlopen(req, timeout=20).read().decode())
    except Exception as ex:
        print(arg, "FAILED", ex)
