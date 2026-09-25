# newsroom — a table that has to look things up

Every other sample in this repository can be run by a model that never leaves its own
weights. A mystery is solved from briefs the bundle carries; a campaign is played out of
a ruleset; a code review reads a diff. Convincing prose is the whole output, and there is
no way to tell, from the transcript, whether anything outside the model was ever
consulted.

**The Vantage** cannot be run that way. It is a two-desk daily paper that must publish
stories about what happened *this week*, with a source URL and a date on every one. A
model writing from memory produces a paper that is either empty or wrong, and both are
visible at a glance.

That is the point of this sample: it is the one whose output is false if the internet was
not reached.

## Why every seat is a local model

The cast runs on **`qwen3:30b-a3b`** through Ollama, on your own machine. This is not a
performance preference — it is what makes the claim checkable.

A hosted model asked what happened this week may simply answer, and the transcript looks
the same whether it searched or recited. A local model with a training cutoff cannot know
about a story published four days ago. If the paper carries one, it looked.

The model is a sparse mixture-of-experts rather than a dense model of the same size,
which matters enormously on a machine where memory capacity is abundant and memory
*bandwidth* is the constraint: 30B parameters total, ~3B active per token. Measured on an AMD
Ryzen AI Max+ 395 with 121 GB of unified memory: **~46 tokens/second**, against a dense
27B on the same box that took over ten minutes for a single turn. Every other sample in
this repository dropped Ollama for exactly that reason.

## Before you start

- a Pyrrhula deployment with the bundled **SearXNG** service running
- **Ollama** reachable from the deployment's containers, with the model pulled:

```bash
ollama pull qwen3:30b-a3b
```

- roughly 20 GB of free memory while a session runs

No provider API key is needed. Nothing in this sample calls a hosted model.

## Setting it up

1. **Import the bundle.** `newsroom.pyr` carries the three personas, their briefs, the
   house style, and the five-phase flow.

2. **Create the model connection.** Provider `ollama_chat`, model `qwen3:30b-a3b`, with
   the base URL your containers reach Ollama on — on podman that is usually the default
   gateway rather than `host.containers.internal`, which frequently does not resolve.
   Bind all three personas to it.

3. **Register the search server**, from [`mcp.json`](mcp.json) beside this file.

4. **Tell the session what day it is.** Set the agenda to today's date before starting.
   The cast cannot know it, and a desk that guesses the year searches for the wrong one —
   observed, on the first run: `recent technology news 2023`.

`scripts/seed_samples.py` in the platform repository does steps 1 to 3 for you.

## The two switches

A search needs **both** of these, and neither is sufficient alone:

- **the persona's own `web_search` flag** — travels in the `.pyr`, per persona
- **the workspace's `web_search` MCP server** — the egress *control*, registered from
  `mcp.json` at setup

A bundle deliberately cannot carry the second: what a tenant may call out to is not the
bundle author's decision.

Worth knowing how this fails, because it does not look like a failure. A persona with the
flag on and no registered server is handed **no search tool at all**, and a model that has
no search tool does not error — it answers. On the first run of this sample the reply was
*"The web search returned no results."* That was true from where the model sat and
completely misleading. **Check `mcp_call_record`, not the prose.**

## What it should be able to do

- **Search, provably.** Every search is a row in `mcp_call_record`, recorded by the
  platform whatever the model says about it. That ledger is the evidence, not the copy.
- **Refuse to invent.** A desk whose search returns nothing usable files nothing and says
  so. The house style is explicit that this is a legitimate outcome and writing from
  memory is not.
- **Be edited.** The chief editor rules `RUN`, `REWRITE` or `SPIKE` on each story with a
  reason. Spiked stories are named at the foot of the edition. A two-story paper that is
  true beats a four-story paper that is padded, and the flow is written so that saying so
  is the normal outcome rather than a failure.
- **Publish.** The edition renders to PDF through the `composed_document` report
  template, which is the one template that does not summarise — for a flow whose output
  *is* the prose, reducing it destroys the deliverable.

## The beat that cannot close without research

The `reporting` phase carries a completion requirement:

```json
"requires": { "tool_calls": 2, "on_unmet": "repeat", "max_repeats": 1 }
```

That is a **floor, not a quota**. Two desks, at least one search each, before the beat may
close. Search as often as you like — there is no `max_calls_per_session` here, unlike the
mystery next door where rationing the forensic lab is the entire case.

It exists because a prompt asking a model to search is a prompt a model may decline, and
this sample's whole claim rests on the searching having happened. `on_unmet: repeat`
nudges once and then moves on: a beat nobody can satisfy must not trap the session.

## About the search results

From an ordinary self-hosted address without API keys, the large search engines refuse:
DuckDuckGo serves a CAPTCHA, Brave, Startpage, Qwant and Yahoo block outright. A refused
search returns **HTTP 200 with zero results**, which is indistinguishable from a model
that chose not to search.

`mcp.json` therefore names the engines this sample actually uses — **Hacker News** and
**Wikinews**. Both answer, both are independent of the blocked set, and everything they
return carries a publication date, which is what lets a story be checked. Technology and
science skew toward the first, world and current affairs toward the second, which is why
the paper has those two desks.

Desks pass `recency: "week"` when they want news. Without it the top results for a
well-covered subject are whatever ranks best, which is usually years old — on one
measurement, results spanning a decade for a query that with a week's window returned
that day's stories.

## Checking that it really did

```sql
-- every search the platform recorded for this session
SELECT created_at, tool_name, outcome
FROM mcp_call_record WHERE session_id = '<session>';
```

Then read the edition and open a source URL. The dates on the stories should be within
days of the session. If the paper is thin, read the SPIKED line at the foot — a short
edition with reasons is this sample working, not failing.
