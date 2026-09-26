#!/usr/bin/env python3
"""Maintainer tool: re-export a sample bundle through a running Pyrrhula.

Users never generate `.pyr` files -- they export them from the UI. This exists for the
one person maintaining this repository, for the day the bundle format changes: it
imports a bundle into a scratch workspace on a deployment running the new version and
exports it again, so the committed file carries the current format and the version that
produced it. It is not referenced by any sample README, and it is not a build step: a
bundle in this repository is an artefact, not a build output.

Stdlib only. Everything it does is what a person does in the product -- sign in, create
a workspace, import, export -- through the same HTTP API the UI uses.

    python3 tools/roundtrip_bundle.py --api http://localhost:8000 \\
        --organization my-org --email me@example.com --password '...' \\
        hagnaryd-mystery/hagnaryd-mystery.pyr

The export runs as the signed-in principal and in ``participant`` mode, which is the
only mode that produces an unencrypted file, and only for content declared
publishable -- every sample's secrets are. A warning printed by the import (for
example a bundle from a newer platform) is shown and does not stop the round trip.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
import uuid


def _request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
    content_type: str | None = None,
) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _json(method: str, url: str, payload: dict | None, headers: dict[str, str]) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    status, data = _request(
        method, url, headers=headers, body=body, content_type="application/json"
    )
    if status >= 300:
        sys.exit(f"{method} {url} -> {status}: {data.decode(errors='replace')[:400]}")
    return json.loads(data) if data else {}


def _multipart(field: str, filename: str, content: bytes) -> tuple[bytes, str]:
    boundary = f"----pyrrhula-{uuid.uuid4().hex}"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        "Content-Type: application/zip\r\n\r\n"
    ).encode()
    tail = f"\r\n--{boundary}--\r\n".encode()
    return head + content + tail, f"multipart/form-data; boundary={boundary}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bundle", type=pathlib.Path, help="the .pyr to re-export (overwritten)")
    parser.add_argument("--api", required=True, help="API base, e.g. http://localhost:8000")
    parser.add_argument("--organization", required=True, help="organization slug to sign in to")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument(
        "--keep-workspace", action="store_true", help="leave the scratch workspace behind"
    )
    args = parser.parse_args()

    api = args.api.rstrip("/")
    tenant_header = {"X-Pyrrhula-Tenant": args.organization}
    login = _json(
        "POST",
        f"{api}/auth/login",
        {"email": args.email, "password": args.password},
        tenant_header,
    )
    auth = {**tenant_header, "Authorization": f"Bearer {login['access_token']}"}

    stem = args.bundle.stem
    workspace = _json(
        "POST",
        f"{api}/workspaces",
        {"name": f"roundtrip {stem} {time.strftime('%Y-%m-%d %H:%M')}", "key": f"rt-{uuid.uuid4().hex[:8]}"},
        auth,
    )
    workspace_id = workspace["id"]
    print(f"workspace {workspace_id}")

    body, content_type = _multipart("file", args.bundle.name, args.bundle.read_bytes())
    status, data = _request(
        "POST",
        f"{api}/export/import?workspace_id={workspace_id}",
        headers=auth,
        body=body,
        content_type=content_type,
    )
    if status >= 300:
        sys.exit(f"import -> {status}: {data.decode(errors='replace')[:400]}")
    report = json.loads(data)
    for line in report.get("warnings", []):
        print(f"import warning: {line}")
    print(
        f"imported: {len(report.get('imported', []))} items, "
        f"skipped: {len(report.get('skipped', []))}"
    )

    job = _json("POST", f"{api}/export", {"workspace_id": workspace_id, "mode": "participant"}, auth)
    job_id = job["job_id"]
    deadline = time.time() + 300
    while True:
        status, data = _request("GET", f"{api}/export/{job_id}/download", headers=auth)
        if status == 200:
            break
        if status != 409:
            sys.exit(f"download -> {status}: {data.decode(errors='replace')[:400]}")
        if time.time() > deadline:
            sys.exit("export job did not finish within five minutes")
        time.sleep(2)

    args.bundle.write_bytes(data)
    print(f"wrote {args.bundle} ({len(data)} bytes)")

    if not args.keep_workspace:
        status, _ = _request("DELETE", f"{api}/workspaces/{workspace_id}", headers=auth)
        print("scratch workspace archived" if status < 300 else f"could not archive workspace ({status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
