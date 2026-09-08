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

## Before you start

A Pyrrhula deployment you can sign up on, and an API key. Built and tested on **DeepSeek**
(`deepseek-chat`).

---

## Step 1 — Sign up

Register with any organization name. You land in **Default Workspace** as its **steward**.

## Step 2 — Choose the Enterprise workflow

**Before importing.** Go to **Workflows** and select **Default** — the workflow whose
vocabulary is the enterprise one ("Enterprise Workflow" is the name of its label set,
not of the workflow you pick here).

## Step 3 — Add your model connection

**Personas** (top nav) **→ Model profiles → New model profile**:

- **Name**: `DeepSeek`
- **Provider**: `deepseek`
- **Model**: `deepseek-chat`
- **API key**: your key

## Step 4 — Import the campaign

Workspace → **Export / import** (top right) → upload [`coffee-campaign.pyr`](coffee-campaign.pyr).

You should see it import **4 personas** (`brand-lead`, `analyst`, `planner`, `skeptic`),
**2 secrets**, **1 flow** ("Campaign round table"), and the launch brief as a knowledge
attachment.

## Step 5 — Point the team at your connection

**Personas** → open each of the four → set **Connection (model agent)** to your connection.

## Step 6 — Turn on the disclosure gate

On the workspace page, open the **Settings** tab and tick **Secret disclosure gate**. Without it the
two confidential facts never enter their holders' context at all, and the session becomes
an ordinary planning meeting.

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

**The table knows the business.** Nordvik's channels, the product, the 9,000-bag ceiling —
all from the shared launch brief.

**The two secret-holders steer without telling.** The analyst pushes back on volume
targets; the planner presses for an earlier date and for owning independent cafés rather
than fighting for grocery shelves. Neither says why. Their briefs explicitly permit the
argument and forbid the fact.

**The final campaign is publishable.** The brand lead writes the closing structure —
audience, message, channels, phases, metrics — and it contains neither the margin nor the
competitor, because neither was ever in her context.

That last point is the one worth checking by hand. Open the **Secrets** page: two secrets,
each held by one participant, and the Brand Lead holds neither.

## Things worth knowing

- **The gate fails closed.** If its model call fails, everything is concealed for that
  turn and the reason is recorded. `deepseek-chat` rejects the structured-output format the
  gate uses, so with DeepSeek you will see conceal every time — the holders still argue
  their corner (their briefs keep the motivation) but you will not see deliberate hints.
  Point the gate at a model with structured output if you want the full behaviour.
- **Making it yours.** The two secrets are ordinary workspace content: open the Secrets
  page and edit them, or add your own, and the same machinery applies.
