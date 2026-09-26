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

The cast runs on **`devstral:24b`** through Ollama, on your own machine. This is not a
performance preference — it is what makes the claim checkable.

A hosted model asked what happened this week may simply answer, and the transcript looks
the same whether it searched or recited. A local model with a training cutoff cannot know
about a story published four days ago. If the paper carries one, it looked.

Devstral is an agentic instruct model, and it is here because it does **not** think.
`qwen3:30b-a3b` sat in these seats first and writes better prose, but it is a reasoning
model, and with tools in front of it the reasoning did not reliably terminate — turns of
22, 58 and 79 minutes that emitted no copy at all. Measured on the real task (search,
open the page, file the story) against live SearXNG: devstral 25 seconds, both tools,
786 characters of sourced copy on the first attempt.

**One model, not two.** An earlier version cast the editor and the desks on different
models and was worse than either alone. Two models resident on one iGPU garble each
other: on the same prompt, qwen3 alone answered 3 times in 4 in 7–45s, and with devstral
also loaded returned **empty 3 times out of 3**, or took 79–220 seconds. If you swap a
seat to another model here, expect that, and consider `OLLAMA_MAX_LOADED_MODELS=1`.

## Before you start

- a Pyrrhula deployment with the bundled **SearXNG** service running
- **Ollama** reachable from the deployment's containers, with the model pulled:

```bash
ollama pull devstral:24b
```

- roughly 16 GB of free memory while a session runs

No provider API key is needed. Nothing in this sample calls a hosted model.

## Setting it up

1. **Import the bundle.** `newsroom.pyr` carries the three personas, their briefs, the
   house style, and the five-phase flow.

2. **Create the model connection.** Provider `ollama_chat`, model `devstral:24b`, with
   the base URL your containers reach Ollama on — on podman that is usually the default
   gateway rather than `host.containers.internal`, which frequently does not resolve.
   Bind all three personas to it — one connection for the whole roster, so the box
   never holds two models at once.

3. **Register the search server.** On the workspace, **MCP servers** → register, with
   the values from [`mcp.json`](mcp.json) beside this file:

   | field | value |
   |---|---|
   | key | `web_search` |
   | url | `http://searxng:8080` (the bundled SearXNG's in-network address) |
   | allowed tools | `search` |
   | calls/session | blank — research is not rationed here |
   | options | `{"engines": "bing news,duckduckgo news,yahoo news,qwant news,hackernews"}` |

   Then a second one so a desk can open what it found: key `web_fetch`, url
   `https://fetch.local/` (unused — the transport is chosen by the key), allowed tools
   `fetch`. The engines line decides whether this sample works at all; see below.

4. **Tell the session what day it is.** Set the agenda to today's date before starting.
   The cast cannot know it, and a desk that guesses the year searches for the wrong one —
   observed, on the first run: `recent technology news 2023`.

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

`mcp.json` therefore names the engines this sample uses, and the choice decides whether
the sample works at all. The big *web* engines refuse; their **news siblings are separate
engines and are not blocked**. Measured here, one query each:

| engine | results | with a time filter |
|---|---|---|
| `bing news` | 10 | 7 — the only one that honours it |
| `duckduckgo news` | 25 | 0 |
| `yahoo news` | 69 | 0 |
| `qwant news` | 7 | — the only engine that **dates every result** |
| `hackernews` | 30 | 3 |
| `google news` | 0 | 0 |

The set is those news engines plus Hacker News for the technology desk. Together: 72
results for one query, 62 of them dated.

**Desks do not pass `recency`.** News engines are fresh by construction, and the filter
empties two of the four. This was learned the hard way: pointed at Hacker News and
Wikinews alone, ranked by relevance, the freshest result the paper could find was **six
weeks old**, and both desks correctly filed nothing, edition after edition.

One trap worth knowing. An engine name SearXNG does not recognise **does not error — it
silently searches the default set instead**. `ecosia`, `baidu news`, `brave news`,
`yandex news` and `marginalia` each appeared to return 84 excellent results until the
per-result `engine` field showed not one came from the engine asked for.

## What this sample does not do well

Honesty is cheaper than a surprise. The flow completes, the searching is real and the
ledger proves it. The *copy* is another matter.

These local models handle a single-actor task with tools well. What they handle badly is
holding a **role while tool-calling in a multi-actor transcript**. The platform serialises
the conversation as `Name: ...` turns, and a 24B model will cheerfully write everyone's
lines — filing its story and then the editor's reply to it, in one message. Observed
across runs: a desk inventing three stories rather than searching; a desk emitting the
raw tool-definition JSON as message text instead of calling the tool.

The flow is built so those failures are **visible rather than silent**, which is the part
worth studying:

- the `reporting` phase cannot close without recorded tool calls, and says so in a
  `phase_requirement` event naming `produced` against `required`
- `mcp_call_record` records searches independently of the prose, so "I searched and found
  nothing" from a desk that never called the tool is contradicted by an empty ledger
- an edition with two honest stories, or none, beats four padded ones, and the SPIKED
  line at the foot says what was dropped

Be warned that a bad run is worse than thin. Runs here have ended with an "edition" that
was the line `Nadia Brekke: (` repeated until the generation ceiling cut it off — the
model continuing the transcript's own `Name: ...` format instead of writing the paper.
Across the last several runs the flow reached its terminal phase every time, in about
three to twenty minutes, but the quality of what came out ranged from two properly
sourced stories to that.

**So: run this to watch the machinery, not to read the paper.** What is reliable here is
everything the platform does — the phases advance, the requirement gate reports honestly,
the searches happen and are recorded, nothing is fabricated into the ledger. What is not
reliable is a 24B model's prose discipline across a multi-actor transcript.

If you want an edition worth reading, point the connection at a hosted model. The ledger
still proves the searching happened; you only lose the argument that a local model *could
not have known* this week's news, which is what the local cast is here to demonstrate.

## Checking that it really did

```sql
-- every search the platform recorded for this session
SELECT created_at, tool_name, outcome
FROM mcp_call_record WHERE session_id = '<session>';
```

Then read the edition and open a source URL. The dates on the stories should be within
days of the session. If the paper is thin, read the SPIKED line at the foot — a short
edition with reasons is this sample working, not failing.
