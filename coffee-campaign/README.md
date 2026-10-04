# Coffee launch campaign

Four people plan the launch of a single-origin coffee. Two of them know something they are
not allowed to say out loud, and the plan has to be good anyway.

**Why this sample exists.** The murder mystery shows confidential information as a game.
This is the same machinery doing the boring, valuable version: an analyst who knows the
margin is 11% can argue *against* a volume-driven campaign without ever stating the
number, and a planner who learned a competitor's launch date under an NDA can push for an
earlier date without saying why. Neither fact can reach the final campaign document,
because neither is in the brand lead's context when she writes it.

---

> **What's in the workspace's library:** three knowledge sources, one per class —
> a *Policy Document* (brand voice, what may never be said publicly), *Domain
> Context* (the company, the product, the ask), and *Reference Material* (glossary,
> what past launches taught them). The flow budgets them differently per phase, so
> the policy binds the writing while the context feeds the discussion.

## Before you start

A Pyrrhula deployment you can sign up on, and an API key. Built and tested on **DeepSeek**
(`deepseek-chat`).

---

## Step 1 — Sign up

Register with any organization name. You land in **Default Workspace** as its **steward**.

## Step 2 — Choose the Default workflow

**Before importing.** Go to **Workflows** and select **Default**. That is the one whose
vocabulary is the enterprise label set — *Facilitator*, *Contributor* — which is why this
sample reads as a working meeting rather than a game table. ("Enterprise Workflow" names
the label set, not a workflow you can pick.)

If you forget, the import pins it for you anyway; selecting it first just means the page
reads correctly while you work.

## Step 3 — Add your model connection

**Personas** (top nav) **→ Model profiles → New model profile**:

- **Name**: `DeepSeek`
- **Provider**: `deepseek`
- **Model**: `deepseek-chat`
- **API key**: your key

## Step 4 — Import the campaign

Workspace → **Export / import** (top right) → upload [`coffee-campaign.pyr`](coffee-campaign.pyr).

You should see it import **4 personas** (`brand-lead`, `analyst`, `planner`, `skeptic`),
**2 secrets**, **1 flow** ("Campaign round table"), and **3 knowledge sources** attached to
the workspace (*Nordvik launch brief*, *Nordvik communications policy*, *Nordvik reference
shelf*).

On a fresh deployment the first import can take several minutes: it is the first thing that
needs the embedding model, which loads on first use. Let it finish.

## Step 5 — Point the team at your connection

**Personas** → open each of the four → set **Connection (model agent)** to your connection.

## Step 6 — Turn on the disclosure gate

On the workspace page, open the **Settings** tab and check **Secret handling**. The import
sets it to **Trusted to the model** (simplest); switch it to **Gated** to add a per-turn
classifier that decides conceal / hint / reveal for each secret and records why (it needs
a structured-output model — see *Give the gate its own model* below). Set to **Excluded**,
the two confidential facts never enter their holders' context at all, and the session
becomes an ordinary planning meeting.

## Step 7 — Run the session

New session:

- **Process definition**: `Campaign round table`
- **Supervisor**: `Brand Lead`
- **Participants**: `Market Analyst`, `Channel Planner`, `Devil's Advocate`
- **Agenda**:

```
Plan the launch campaign for Nordvik's new single-origin Ethiopian filter roast. Produce
something the company can actually execute: who it is for, what it says, where it runs, in
what order, and how success is measured. The supply is limited to about 9,000 bags and
there will not be more this year.
```

---

## What you should see

**A real discussion, then a close.** Three rounds of discussion — the brand lead opens
each, then the analyst, the planner and the devil's advocate answer in turn (twelve turns)
— then one closing turn in which the brand lead writes the campaign.

**The table knows the business.** Nordvik's channels, the product, the 9,000-bag ceiling —
all from the shared launch brief.

**The two secret-holders steer without telling.** The analyst pushes back on volume
targets; the planner presses for an earlier date and for owning independent cafés rather
than fighting for grocery shelves. Neither says why. Their briefs explicitly permit the
argument and forbid the fact.

**The final campaign is publishable.** The brand lead writes the closing structure —
audience, message, channels, phases, metrics — and it contains neither the margin nor the
competitor. She holds neither secret, and the closing phase grants no secret visibility at
all, so the only way a fact could reach her is by someone saying it at the table, which is
what the holders' briefs (and, if you turned it on, the gate) prevent.

That last point is the one worth checking by hand. Open the **Secrets** page: two secrets,
each held by one participant, and the Brand Lead holds neither. With the gate on, each
holder's turn also leaves a recorded conceal / hint / reveal decision per secret, with the
classifier's reason.

One thing the gate can do that surprises people: it judges from the secret's *gist*, the
holder's persona and the conversation — never from the secret's own "do not say this"
brief — so on an internal-sounding planning turn it may decide **reveal**. The platform
then records the secret as *told* to everyone at the table, the Brand Lead included, and
the Secrets page shows them as holders from that turn on. The campaign stays clean anyway,
because the closing phase grants no secret visibility: what the Brand Lead writes there is
assembled without either secret, whoever holds it by then.

That is why the analyst's and the planner's persona text ends with a one-line
confidentiality note ("you argue from it, you never state it at this table"). The gate
reads the persona, so the note is the one place a holder's *own* discretion reaches the
classifier. Without it, one sweep run recorded two reveals; with it, the next run recorded
none (conceal 5, hint 1). If you write your own holders, keep such a line near the top of
the persona — the gate reads only its first few hundred characters.

## Take the campaign away

On the session page, under **Report**, generate **Composed document**: it renders the
closing turn as written under a *Document* heading, with the recorded facts above it, and
**Download** gives you the PDF. **Transcript** does the same for the whole discussion,
phase by phase; **Session recap** is a model-written summary; **Decision summary** needs a
review click before it will render.

## Things worth knowing

- **Give the gate its own model.** The gate is a strict-JSON classifier, so it needs a
  model that supports structured output — `deepseek-chat` does not, and the gate then
  *fails closed*: everything is concealed and the reason recorded. The holders still argue
  their corner (their briefs keep the motivation), but you never see a deliberate hint.
  Add a second connection under **Personas → Model profiles** (provider `openai`, model
  `gpt-4.1-mini` works) and pick it under **Secret disclosure gate** there. Only the gate
  uses it; the table keeps talking on whatever you like.
- **Making it yours.** The two secrets are ordinary workspace content: open the Secrets
  page and edit them, or add your own, and the same machinery applies.
