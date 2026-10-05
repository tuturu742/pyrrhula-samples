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

## The cast: one local model, through Ollama

The whole roster — chief editor and both desks — runs on **`devstral:24b`** through
Ollama, on one connection. A local model is the right cast for this sample because its
training cutoff makes the claim provable: Devstral cannot know about a story published
this morning, so if the paper carries one, it looked.

What it produced on the 5 October 2026 sweep, on a single Radeon 8060S iGPU, in three
minutes flat: eight tool calls in the ledger (four searches, four page fetches), two
desks each filing a story found by search and read from the fetched page — a death
from plague exposure at a laboratory in Irkutsk (SVT, published that morning) and a new
US federal task force on artificial intelligence (Fox 5 Atlanta, the day before) — the
editor ruling `SPIKE` on one and `REWRITE` on the other with a reason each, the spiked
desk answering "Spiked, understood.", and an edition with one story, its URL and date,
and a SPIKED line naming what was dropped. Every URL in it resolves, and the dates on
the pages match the dates the desks printed.

A word on what took three sweeps to learn. Two earlier passes concluded that a 24B model
"cannot hold a role while tool-calling": the opening turn repeated one sentence to the
token ceiling, the desks answered in word salad. None of that was the model. The same
requests sent straight to Ollama produced the same garbage on the GPU and a clean tool
call on the CPU; the ROCm backend was corrupting every generation on that chip. With
Ollama on its Vulkan backend the model answers the way a capable model does. If a local
run looks like nonsense, suspect the GPU path before the model — *Before you start*
says what to check.

**One connection, one request at a time.** An earlier version cast the editor and the
desks on different local models and was worse than either alone: two models resident on
one iGPU garble each other. A session only ever sends one request at a time; keep
everything else off the Ollama server while it runs, and run Ollama with
`OLLAMA_NUM_PARALLEL=1`.

A hosted model also works — see *A hosted model instead* at the end — but it proves less.

---

## Before you start

You need:

- a Pyrrhula deployment you can sign up on, with the bundled **SearXNG** service running
  (the standard install starts it)
- **Ollama** on the machine that hosts the deployment, with the model pulled:

```bash
ollama pull devstral:24b
```

  It must listen on an address the deployment's containers can reach — not only
  `127.0.0.1` (a stock host install does that; start it with `OLLAMA_HOST=0.0.0.0`) — and
  needs roughly 20 GB of free GPU or unified memory while a session runs (13 GB of
  weights plus a 16k-token context).

**Which backend.** This matters more than anything else in this README. On the machine
the sample was verified on — an AMD Radeon 8060S (Strix Halo, `gfx1151`) integrated GPU —
Ollama's `-rocm` image produced wrong output in every configuration tried: token garbage
with the common `HSA_OVERRIDE_GFX_VERSION=11.0.0` workaround, repetition loops without it,
with flash attention off, with hipBLASLt off, and a hang at small batch sizes. The
standard image with the **Vulkan** backend was correct and as fast (15 tokens/s, all
layers on the GPU). The container that works:

```yaml
image: docker.io/ollama/ollama:0.33.2        # the standard image, not :rocm
devices: ["/dev/dri:/dev/dri"]               # Vulkan needs only the render node
environment:
  - OLLAMA_VULKAN=1
  - OLLAMA_IGPU_ENABLE=1      # without it Ollama drops an integrated GPU and runs on the CPU
  - OLLAMA_NUM_PARALLEL=1
  - OLLAMA_HOST=0.0.0.0
```

Ollama's log should say `inference compute ... library=Vulkan ... (RADV GFX1151)`. On a
discrete NVIDIA or AMD card the default backend is probably fine; the test that settles
it either way is at the end of step 3.

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

**Personas** (top nav) **→ Model profiles → New model profile**:

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
it fills, so a model that falls into a repetition loop would never finish its turn on its
own. Pyrrhula caps every Ollama turn at **4096 output tokens** unless the connection says
otherwise, so the failure is bounded without any setting; `2000` halves the time such a
turn would waste and is still well above anything a turn here needs — the edition is the
longest, at a few hundred words. Leave it blank if you would rather not tune anything.
Sampling temperatures travel with the personas in the bundle (0.15 for the desks, 0.2
for the editor — Mistral's own recommendation for Devstral is 0.15 for agentic use;
0.6 made the desks announce "I'll search for that" instead of calling the tool).

**The test that matters.** "Responded" only proves the endpoint answers. Before the
first session, ask the model one real question through Ollama's own CLI
(`ollama run devstral:24b "Name three rivers"`) and read the answer. If it is not
three rivers — repeated fragments, `<x|x|x|`, a sentence looping — the GPU backend is
corrupting output and no prompt will fix it: see *Which backend* above. On the sweep
machine the broken backend was obvious from the first line of any answer, and the
same request on the CPU (`"options": {"num_gpu": 0}` through the API) was correct;
that comparison is the one that settles it.

## Step 4 — Import the bundle

Workspace → **Export / import** (top right) → upload [`newsroom.pyr`](newsroom.pyr).

The report should list **3 personas** (`chief-editor`, `tech-desk`, `world-desk`),
**1 flow** (`daily-edition`, "Daily edition"), **2 knowledge attachments** (the house
style and a page about the paper), and the vocabulary *bound to the one already here*.
It will also say each persona was "bound to placeholder (connection did not travel)" —
that is step 5. If the organization has imported this bundle before, the two knowledge
attachments arrive under forked keys (`house-style-imported-2`); that is harmless.

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

Fetches are recorded in the ledger like searches (`web_fetch | fetch`). Some sites
refuse an unattended fetch and the row says `failed`; the desks are told to fetch
another result or file from the snippet, attributing it to the publication, and that is
what they do.

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

Then run it. On the sweep machine a session takes three to five minutes: the opener in
about 15 seconds, a desk turn with its searches and fetches in one to two minutes, the
edition in half a minute.

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

- **Search, provably.** Every search and fetch is a row in `mcp_call_record`, recorded by
  the platform whatever the model says about it. That ledger is the evidence, not the
  copy.
- **Refuse to invent.** A desk whose search returns nothing usable files nothing and says
  so. The house style is explicit that this is a legitimate outcome and writing from
  memory is not.
- **Be edited.** The chief editor rules `RUN`, `REWRITE` or `SPIKE` on each story with a
  reason. Spiked stories are named at the foot of the edition. A one-story paper that is
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

The gate counts read-only calls — searches and fetches — as well as side-effecting ones.
The session emits a `phase_requirement` event when the beat closes; on the sweep's clean
run it said `"produced": {"tool_calls": 7}, "decision": "met"`, and on a run where
neither desk searched it said `"produced": 0, "required": 2, "decision": "repeat"` and
sent the desks round again. Both are the gate working.

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

**The date comes from the page, not the result.** The search tool hands the model a
title, a URL and a snippet; the engines' own dates are not passed through on the current
release. That is why the desks are told to fetch the page and take the date off it, and
why a desk that could not open the page prints `date unknown` rather than guessing.

One trap worth knowing. An engine name SearXNG does not recognise **does not error — it
silently searches the default set instead**. `ecosia`, `baidu news`, `brave news`,
`yandex news` and `marginalia` each appeared to return 84 excellent results until the
per-result `engine` field showed not one came from the engine asked for.

## What this sample does not do well

Honesty is cheaper than a surprise.

**Runs vary.** Five sessions on the sweep day, same bundle and same model, gave: a
one-story paper that was true (the run described above); a two-story paper in which one
story was a 2023 engineering blog post the desk marked `date unknown` and the editor ran
anyway; a run where the world desk searched twice, found nothing it would stand behind,
and filed nothing — which the house style allows and the edition said so; and, before
the prompts were tightened, a run where both desks searched the example query from the
instructions instead of their beats and the editor filled an empty slot with a story
she had not been given, URL included. The flow reached its last phase every time, in
three to five minutes.

**What a 24B model gets wrong**, in rough order of frequency: a desk *announces* a tool
call ("I'll try fetching the pages again") instead of making it, and the turn ends with
no story; a rewrite turn answers the other desk's ruling, or writes the other desk's
lines; a search is made of the literal example in an instruction rather than the beat;
an undated or old page is treated as this week's news. The bundle's phase prompts now
name each of these, and the low temperatures help, but none is eliminated.

The flow is built so those failures are **visible rather than silent**, which is the part
worth studying:

- the `reporting` phase reports in a `phase_requirement` event naming `produced` against
  `required`, and goes round again when it is short
- `mcp_call_record` records searches and fetches independently of the prose, so "I
  searched and found nothing" from a desk that never called the tool is contradicted by
  an empty ledger
- an edition with one honest story, or none, beats four padded ones, and the SPIKED
  line at the foot says what was dropped

If a run has visibly gone wrong, pause or archive the session: the running turn
finishes and nothing further is generated. Then read the edition against the ledger
before trusting it, as *Checking that it really did* says.

## A hosted model instead

The same bundle runs on a hosted model with one connection for all three seats; on the
4 October 2026 sweep, `deepseek-v4-pro` (provider `deepseek`, model `deepseek-v4-pro`,
no params) ran the flow in under five minutes with 21 searches, two sourced stories with
nine URLs between them, two `REWRITE` rulings and a rewrite that answered them. It is a
richer paper. What it cannot prove is that it *needed* to search: asked what happened
this week, a hosted model may answer from weights newer than you think, and the
transcript looks the same either way. The ledger is still real, and for most purposes
enough. Set a daily cap under **Usage → Limits** before an autonomous run on a paid key
(`per_persona_daily_tokens = 600000` is generous; that session used about 70 000).

## Checking that it really did

```sql
-- every search and fetch the platform recorded for this session
SELECT created_at, server_key, tool_name, outcome
FROM mcp_call_record WHERE session_id = '<session>';
```

Then read the edition and open a source URL. The dates on the stories should be within
days of the session, and the page's own publication date should agree with what the
desk printed. If the paper is thin, read the SPIKED line at the foot — a short edition
with reasons is this sample working, not failing.
