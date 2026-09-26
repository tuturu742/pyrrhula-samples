#!/usr/bin/env python3
"""The Hägnaryd forensic lab as a standalone MCP server. SPOILERS BELOW.

The referee's answers to every lab request are embedded in this file -- do not read
past this docstring if you intend to play the investigator.

Run it (stdlib only, no installs):

    python3 evidence-server.py --port 8765

then register it on the workspace (Workspace -> MCP servers -> Add):

    key            evidence
    url            http://<host-as-your-deployment-sees-it>:8765
    enabled tools  evidence_check

The bundled flow offers the tool to the inspector's phases only; suspects never see it.

Budgets are not this server's job. It answers whatever it is asked, as often as it is
asked, and keeps no count -- it cannot keep a useful one, because an external MCP server
is sent only the model's arguments and never a trusted session id, so any budget it kept
would be a single pool shared by every game hitting the process.

Pyrrhula holds the limit instead, per session: set "calls/session" to 2 when you attach
this server to a workspace. Two games can then run against one copy of this server
without stealing each other's requests.

Hand-maintained: the answers mirror the inspector's dossier in the bundle.
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

RESULTS = {
  "guest_room_search": "Viktor's briefcase: printouts of his mother's private emails, including the Kastrup correspondence, dated over the last three months. Sofia's bag: a letter on Kastrup Glas Holding paper offering her a country-manager post 'on completion'. Elin's room: nothing beyond the laundry bag. Lager's room: see the clothing request. Marta's rooms: three empty Madeira bottles.",
  "operator_records": "Victim's number, last 24h: outgoing SMS 18:53 to Henrik Lager's number, delivered 18:53, read receipt 18:54. Outgoing call 16:10 to a Copenhagen number registered to Kastrup Glas Holding, 12 minutes. Nothing after 18:53.",
  "phone_search": "Voluntary search of the suspects' phones: Viktor refuses. Elin refuses. Sofia refuses. Lager consents -- the 18:53 message is present, marked read at 18:54. Marta consents -- nothing. The refusals and the read receipt are reported to you.",
  "pre_dinner_clothing": "Elin's room, laundry bag: a green dress, right cuff and right side of the skirt damp when bagged at 23:40; on the cuff a faint brownish trace, presumptively blood, too little for a fast typing -- 'victim or wearer, cannot say tonight'. Lager's room, washbag: a cloth with waxy grease, and a tube of leather grease from the boot room. Viktor's room: nothing. Sofia's room: nothing. Marta's apron: Madeira.",
  "prints_in_the_suite": "The doorstop was wiped. Desk: victim, Sofia, Marta. Bedroom door, inside edge: victim, Marta, and one partial of Elin -- who is the daughter and was in the suite 'last weekend' by her own account.",
  "recover_speech_file": "Laptop unlocked; the speech file recovered. Page 6/6 reads: 'As for the collection, and as for Elin -- eleven pieces are missing from this house, including the three Lindberg vases, sold through a dealer in Malmö whose records I have. The collection goes to the Nationalmuseum intact, on Monday, with those records to the police. Elin is no longer its director. Viktor's altered reports go to the auditors the same morning. I have loved you both. I do not trust either of you.'",
  "study_safe": "The 2023 will: estate to Viktor and Elin equally; Sofia Nyqvist 2,000,000 kr; Marta Sjöberg the gatehouse for life. A handwritten note clipped to it, dated Friday: 'Monday -- Sofia's bequest out. Elin -- see speech.' Also the Kastrup term sheet, signed by Ingeborg.",
  "tower_stairs": "The grease on the third step is the boot-room leather grease. The missing bulb was found in the boot-room bin bearing one clear fingerprint: Henrik Lager. Grease traces on the tower handrail at the height of a man of about 1.80 m."
}


TOOL = {
    "name": "evidence_check",
    "description": (
        "Send a forensic lab request by radio. Results come back immediately. Your "
        "allowance for this interview is limited, so choose carefully."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "request": {
                "type": "string",
                "enum": sorted(RESULTS),
                "description": "The lab request to run.",
            }
        },
        "required": ["request"],
        "additionalProperties": False,
    },
}


def call(request: str) -> dict:
    """Answer a lab request. This server keeps NO budget of its own.

    It cannot: an external MCP server is sent only the model's arguments, never a
    trusted session id, so any count it kept would be one pool shared by every game
    hitting the process -- two concurrent sessions would silently starve each other.
    Pyrrhula holds the real limit, per session, via `max_calls_per_session` on the
    server's registration (the "calls/session" field when you attach it).
    """
    import datetime

    request = request.strip()
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    if request not in RESULTS:
        print(f"[{stamp}] REFUSED unknown request {request!r}", flush=True)
        return {"error": "unknown_request", "available": sorted(RESULTS)}
    print(f"[{stamp}] answered: {request}", flush=True)
    return {"request": request, "result": RESULTS[request]}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("content-length", 0) or 0)
        body = json.loads(self.rfile.read(length) or b"{}")
        method = body.get("method", "")
        if method == "notifications/initialized":
            self.send_response(202)
            self.end_headers()
            return
        if method == "initialize":
            result = {
                "protocolVersion": body.get("params", {}).get("protocolVersion", "2025-03-26"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "hagnaryd-evidence", "version": "1.0"},
            }
        elif method == "tools/list":
            result = {"tools": [TOOL]}
        elif method == "tools/call":
            params = body.get("params", {})
            answer = call(str(params.get("arguments", {}).get("request", "")))
            result = {
                "content": [{"type": "text", "text": json.dumps(answer)}],
                "isError": "error" in answer,
            }
        else:
            error = {"code": -32601, "message": method}
            self._reply({"jsonrpc": "2.0", "id": body.get("id"), "error": error})
            return
        self._reply({"jsonrpc": "2.0", "id": body.get("id"), "result": result})

    def _reply(self, payload: dict) -> None:
        data = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):  # quiet
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="0.0.0.0")
    ns = ap.parse_args()
    print(
        f"Hägnaryd forensic lab listening on {ns.host}:{ns.port} -- "
        "set calls/session in Pyrrhula to limit an interview"
    )
    HTTPServer((ns.host, ns.port), Handler).serve_forever()
