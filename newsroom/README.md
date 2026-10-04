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

## Which model: a readable paper, or a provable one

There are two honest ways to cast this table, and they prove different things.

**A hosted model gives you the paper.** The recommended cast is **DeepSeek V4 Pro**
(`deepseek-v4-pro`), one connection for all three seats. On the 4 October 2026 sweep it
ran the whole flow in under five minutes: 21 searches in the ledger, two sourced and
dated stories (a Strait of Hormuz tanker attack with four source URLs, Starship's first
orbit with five), two `REWRITE` rulings with reasons, a rewrite that answered them, and
a formatted edition with a *Spiked:* line at the foot. That edition is what the
`composed_document` report renders to PDF, and it is what this README's steps produce.

What a hosted model cannot prove is that it *needed* to search. Asked what happened this
week, it may answer from weights that are newer than you think, and the transcript looks
the same either way. The proof that it searched is the `mcp_call_record` ledger — which is
real, and enough for most purposes — not the copy.

**A local model gives you the proof.** `devstral:24b` through Ollama has a training
cutoff and cannot know about a story published four days ago; if the paper carries one,
it looked. That is a stronger claim, and it is why the local cast is kept here as the
alternative. It is also, measured, a much worse newspaper:

- First sweep (4 October 2026): the flow reached its last phase in 3½ minutes, three
  searches were recorded, the world desk filed one real sourced story (a UN General
  Assembly debate, with URL). The tech desk filed nothing sourced, and the editor's
  edition turn did not write the paper.
- Second sweep, same day, after the platform fixes below: the editor's opening turn
  repeated one sentence ("The editor does not write.") to the token ceiling, both desks
  answered in word salad ("You can't you can't have two same."), neither searched, and
  the session was stopped.

The flow itself behaved the same both times — phases advanced, the gate reported
honestly, nothing was invented into the ledger. What a 24B model cannot do reliably is
hold a role while tool-calling inside a multi-actor transcript (see *What this sample
does not do well*). Run the local cast to watch the machinery, and to be able to say
the news could not have been in the weights; run the hosted cast to read the paper.

Both casts use **one connection for the whole roster.** An earlier version cast the
editor and the desks on different local models and was worse than either alone: two
models resident on one iGPU garble each other (on the same prompt, qwen3 alone answered
3 times in 4 in 7–45 s, and with devstral also loaded returned empty 3 times out of 3,
or took 79–220 seconds). The same happens with one model and two requests in flight:
with `OLLAMA_NUM_PARALLEL=2`, an opening prompt devstral answered properly 4 times in 4
on an idle server degenerated 4 times in 5 while another request was being served. A
session only ever sends one request at a time; keep everything else off the Ollama
server while it runs.

---

## Before you start

You need:

- a Pyrrhula deployment you can sign up on, with the bundled **SearXNG** service running
  (the standard install starts it)
- for the recommended cast, a **DeepSeek API key**
- for the local cast instead, **Ollama** on the machine that hosts the deployment, with
  the model pulled, and listening on an address the deployment's containers can reach —
  not only on `127.0.0.1` (a stock host install does that; start it with
  `OLLAMA_HOST=0.0.0.0`), and roughly 16 GB of free memory while a session runs:

```bash
ollama pull devstral:24b
```

## Step 1 — Sign up

Open Pyrrhula and register with any organization name (on a single-tenant install that
already has an owner, log in as the owner instead). You land in **Default Workspace** as
its **steward**. If that workspace already holds something, create a new one
(**Workspaces → New**) and do everything below in it; the bundle brings its own cast and
flow and does not need anything that is already there.

## Step 2 — Choose the Default workflow

Go to **Workflows** and select **Default** — the bundle was authored under it. If you
forget, the import pins it for you anyway; selecting it first just means the pages read
correctly while you work.

## Step 3 — Add the model connection

**Personas** (top nav) **→ Model profiles → New model profile**.

### Recommended: DeepSeek

- **Name**: `DeepSeek V4 Pro` (anything you like)
- **Provider**: `deepseek`
- **API key**: your DeepSeek key
- **Model**: `deepseek-v4-pro`
- leave Max tokens and Endpoint URL blank

Save, then press **Test**: it should say `deepseek/deepseek-v4-pro responded`.

Before the first autonomous run, set a daily cap under **Usage → Limits** (the API is
`PUT /limits`). The sweep's session used about 70 000 tokens across the three seats;
`per_persona_daily_tokens = 600000` is generous and still a ceiling.

### Alternative: a local model through Ollama

- **Name**: `Devstral (local)`
- **Provider**: choose **Other…** and type `ollama_chat` (the UI's "Ollama (local)"
  choice sets `ollama`, which speaks the generate API and cannot call tools)
- **API key**: leave blank
- **Endpoint URL**: your machine's LAN address, port `11434` — e.g.
  `http://192.168.1.20:11434`; see below
- **Max tokens**: `2000` — optional, see below
- **Model**: `devstral:24b`

Save, then press **Test**: it should say `ollama_chat/devstral:24b responded`.

**Which address.** `localhost` is the container itself, so it never works. Use the
address `ip -4 addr` shows on your wifi or ethernet interface. Measured from inside the
api container of the (rootless podman) compose stack:

| address | Ollama installed on the host | Ollama in its own container, port published |
|---|---|---|
| the host's **LAN IP**, e.g. `http://192.168.1.20:11434` | works | works |
| the compose network's gateway, e.g. `http://10.89.3.1:11434` | does not connect | works |
| `http://host.containers.internal:11434` | resolves, times out | resolves, times out |

The gateway only looks like the host: on rootless podman it reaches ports that podman
itself publishes, not a process listening on the host. The LAN IP works either way, as
long as Ollama listens beyond `127.0.0.1` (see *Before you start*); if it changes when you
change networks, edit the connection.

**Why max tokens.** Ollama's server shifts its context window rather than stopping when
it fills, so a local model that falls into a repetition loop would never finish its turn
on its own. Pyrrhula now caps every Ollama turn at **4096 output tokens** unless the
connection says otherwise, so the failure is bounded without any setting: a looping
opener on the sweep ran to the ceiling and the session moved on. `2000` on the
connection halves the time such a turn wastes (about three minutes instead of six on a
single iGPU) and is still well above anything a turn here needs — the edition is the
longest, at a few hundred words. Leave it blank if you would rather not tune anything.

## Step 4 — Import the bundle

Workspace → **Export / import** (top right) → upload [`newsroom.pyr`](newsroom.pyr).

The report should list **3 personas** (`chief-editor`, `tech-desk`, `world-desk`),
**1 flow** (`daily-edition`, "Daily edition"), **2 knowledge attachments** (the house
style and a page about the paper), and the vocabulary *bound to the one already here*.
It will also say each persona was "bound to placeholder (connection did not travel)" —
that is step 5. On a deployment that reports itself as `0.1.0rc2` it also warns that the
bundle "was written by Pyrrhula 0.1.0, newer than this deployment"; everything still
imports. If the organization has imported this bundle before, the two knowledge
attachments arrive under forked keys (`house-style-imported`); that is harmless.

The bundle carries the three personas, their briefs, the house style, and the five-phase
flow: the editor hands out beats, the desks search and file, the editor rules on each
story, the desks answer the ruling, and the editor writes the edition.

## Step 5 — Point the cast at your connection

Go to **Personas** and open each of the three — Marit Halvorsen (chief editor), Aksel
Rygg (technology) and Nadia Brekke (world). Set **Connection (model agent)** to the
connection from step 3, and save. Leave each one's search switch as it arrived: on for
the two desks, off for the editor.

## Step 6 — Turn on the search

Open the workspace where you imported the bundle, then **Settings → MCP servers →
Register**, with the values from [`mcp.json`](mcp.json) beside this file:

| field | value |
|---|---|
| key | `web_search` |
| url | `http://searxng:8080` (the bundled SearXNG's in-network address) |
| allowed tools | `search` |
| calls/session | blank — research is not rationed here |
| options | `{"engines": "bing news,duckduckgo news,yahoo news,qwant news,hackernews"}` |

Then a second one so a desk can open what it found: key `web_fetch`, url
`https://fetch.local/` (unused — the transport is chosen by the key), allowed tools
`fetch`.

Press **Test** next to each once it is listed. Both should say *reachable, offers 1
tool(s)*. The engines line decides whether this sample works at all; see *About the
search results* below.

**On the current release the second registration does not yet do its job.** The desks
are handed a `fetch_page` tool and call it, but every call comes back "not available to
this workspace in this phase": the platform checks the fetch against a tool list that
names only `search`. The desks notice and say so ("Page fetches were unavailable in this
phase, so I am filing from what the search results state"), and file from snippets with
attribution and no direct quotation, which is what the house style tells them to do
when they could not open the page. Register `web_fetch` anyway — it costs nothing and
starts working when the platform is fixed — and expect no `web_fetch` rows in the
ledger until then.

### The two switches

A search needs **both** of these, and neither is sufficient alone:

- **the persona's own `web_search` flag** — travels in the `.pyr`, per persona
- **the workspace's `web_search` MCP server** — the egress *control*, registered from
  `mcp.json` in this step

A bundle deliberately cannot carry the second: what a tenant may call out to is not the
bundle author's decision.

Worth knowing how this fails, because it does not look like a failure. A persona with the
flag on and no registered server is handed **no search tool at all**, and a model that has
no search tool does not error — it answers. On the first run of this sample the reply was
*"The web search returned no results."* That was true from where the model sat and
completely misleading. **Check `mcp_call_record`, not the prose.**

## Step 7 — Start the edition

Create a new session in the workspace:

- **Process definition**: `Daily edition`
- **Supervisor**: `Marit Halvorsen`
- **Participants**: `Aksel Rygg` and `Nadia Brekke`
- **Agenda**: paste this, **with today's date in it** —

```
Today is <weekday, day month year>. The Vantage's daily edition: the chief editor gives
each desk one beat for this week, each desk searches and files one sourced, dated story,
the editor rules RUN, REWRITE or SPIKE on each, and writes the edition.
```

The date is not decoration. The cast cannot know it, and a desk that guesses the year
searches for the wrong one — observed, on the first run: `recent technology news 2023`.

Then run it. On DeepSeek a session takes about five minutes; on a single iGPU with the
local cast, three to twenty.

When it reaches its last phase, open the session's **Reports**, generate one from the
**Composed document** template and download it as PDF: that is the edition. The report
has a *Recorded facts* section (empty here — nothing in this flow is a deterministic
resolution) and then a **Document** section holding the editor's last message as
written. It is the one template that does not summarise — for a flow whose output *is*
the prose, reducing it destroys the deliverable. The **Transcript** template renders the
whole conversation, phase by phase, the same way, if you want the desks' filings and the
rulings beside the paper.

A report is generated once per event range: asking for the same template again on a
finished session returns the report already made. Fork or re-run the session for a
new one.

---

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
  template (step 7).

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

The gate counts read-only calls — searches — as well as side-effecting ones. The session
emits a `phase_requirement` event when the beat closes; on the DeepSeek run it said
`"produced": {"tool_calls": 13}, "decision": "met"`, and on the local run where neither
desk searched it said `"produced": 0, "required": 2, "decision": "repeat"` and sent the
desks round again. Both are the gate working.

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
results for one query, 62 of them dated. Which of them answer varies from day to day —
on one later day `duckduckgo news` timed out and `yahoo news` returned nothing, and the
other three still gave 47 results — which is why the set is five and not one.

**Desks do not pass `recency`.** News engines are fresh by construction, and the filter
empties two of the four. This was learned the hard way: pointed at Hacker News and
Wikinews alone, ranked by relevance, the freshest result the paper could find was **six
weeks old**, and both desks correctly filed nothing, edition after edition.

One trap worth knowing. An engine name SearXNG does not recognise **does not error — it
silently searches the default set instead**. `ecosia`, `baidu news`, `brave news`,
`yandex news` and `marginalia` each appeared to return 84 excellent results until the
per-result `engine` field showed not one came from the engine asked for.

## What this sample does not do well

Honesty is cheaper than a surprise.

**With the hosted cast**, the weak point is sourcing depth, not discipline. Because page
fetches currently fail (step 6), every story is built from search snippets: several
publications attributed per paragraph, no quotation, and the odd `(date unknown)` where
the engine gave none. The editor's first ruling on the sweep was exactly that — `REWRITE`,
"four publications are attributed and only the Times is sourced, so list the URL and date
for every claim you actually saw or cut the others" — and the rewrite complied. Expect a
thin, correct paper rather than a rich one until fetching works.

**With the local cast**, the problem is the model, and it is a different order of
problem. A 24B model handles a single-actor task with tools well. What it handles badly
is holding a **role while tool-calling in a multi-actor transcript**. The platform
serialises the conversation as `Name: ...` turns, and devstral will cheerfully write
everyone's lines — filing its story and then the editor's reply to it, in one message.
Observed across runs: a desk inventing three stories rather than searching; a desk
emitting the raw tool-definition JSON as message text instead of calling the tool; an
opening turn that repeats one sentence to the ceiling; desk turns that are not sentences
at all.

The flow is built so those failures are **visible rather than silent**, which is the part
worth studying:

- the `reporting` phase reports in a `phase_requirement` event naming `produced` against
  `required`, and goes round again when it is short
- `mcp_call_record` records searches independently of the prose, so "I searched and found
  nothing" from a desk that never called the tool is contradicted by an empty ledger
- an edition with two honest stories, or none, beats four padded ones, and the SPIKED
  line at the foot says what was dropped

Be warned that a bad local run is worse than thin. Runs here have ended with an
"edition" that was the line `Nadia Brekke: (` repeated until the generation ceiling cut
it off. Across the last several local runs the flow reached its terminal phase almost
every time, in about three to twenty minutes, but the quality of what came out ranged
from two properly sourced stories to that. If a local run has visibly gone wrong, pause
or archive the session: the running turn finishes and nothing further is generated.

## Checking that it really did

```sql
-- every search the platform recorded for this session
SELECT created_at, server_key, tool_name, outcome
FROM mcp_call_record WHERE session_id = '<session>';
```

Then read the edition and open a source URL. The dates on the stories should be within
days of the session. If the paper is thin, read the SPIKED line at the foot — a short
edition with reasons is this sample working, not failing.
