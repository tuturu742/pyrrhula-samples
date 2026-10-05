# Working on Pyrrhula itself

A tiered bench — architect, four developers and QA — working on the Pyrrhula codebase.
The dogfood sample.

**Why this sample exists.** The interesting part is not that several agents discuss code.
It is that they share a written set of invariants, and the architect's job is to hold the
line on them: if a proposed change would break tenancy isolation, or put secret plaintext where
exclusion should have removed it, or add an UPDATE grant to an append-only table, that is
the objection — not a matter of style.

---

> **What's in the workspace's library:** three knowledge sources, one per class —
> *Pyrrhula ground rules* (the invariants a change must not break; the `rules` class,
> shown as *Engineering Handbook* under this workflow), *Why this project exists* (who
> this is for, what users actually ask for, the constraints; `lore`, shown as *Review
> Rubric*), and *Project reference shelf* (team glossary, decisions worth remembering;
> `misc`, shown as *Runbook*). The agents read the ground rules to review code and the
> project's purpose to know what the code is for.

## Before you start

A Pyrrhula deployment and an API key. Built and tested on **DeepSeek** (`deepseek-chat`).

---

## Step 1 — Sign up

Register with any organization name. You land in **Default Workspace** as its **steward**.

## Step 2 — Choose the Software Development workflow

**Before importing.** **Workflows** → **Software Development**.

## Step 3 — Add your model connection

**Personas** (top nav) **→ Model profiles → New model profile**: name `DeepSeek`, provider `deepseek`, model
`deepseek-chat`, and your API key.

![The repo knowledge graph: what the analyzed repository achieves, written into workspace knowledge so every agent plans against it](images/repo-graph.png)

## Step 4 — Import the team

Workspace → **Export / import** (top right) → upload [`pyrrhula.pyr`](pyrrhula.pyr).

You should see **6 personas** (`architect`, `staff`, `senior`, `middle`, `junior`, `qa`),
**1 flow** ("Plan, implement, review"), and the ground rules as a knowledge attachment. No
secrets.

## Step 5 — Point the team at your connections

**Personas** → open each one → set **Connection (model agent)**.

Give the **Assistant** persona a connection too: it drafts for you from the chat widget, and
its model is the one that writes the repo analysis in *Taking it further*.

The roster is tiered on purpose: give `staff` and `architect` your strongest model, `senior`
and `qa` something capable, and `middle`/`junior` something cheap and fast. That mix is the
point — a table where every seat runs the same model is an expensive way to get one opinion
repeated. Pointing all six at one connection works too if you are just trying it out.

## Step 6 — Start the session

New session:

- **Process definition**: `Plan, implement, review`
- **Supervisor**: `Architect`
- **Participants**: `Staff Dev`, `Senior Dev`, `Middle Dev`, `Junior Dev`, `QA` (or a
  subset — a smaller table is cheaper and often sharper)
- **Agenda**: something small and real. For example —

```
We want an endpoint that returns the disclosure decisions for one session, so an overseer
can audit what the gate concealed and why. Decide what it should return, who may call it,
and what would have to be tested before it ships.
```

---

## What you should see

The architect breaks the work into one change with a stated definition of done. The
developers propose it against the ground rules, and the tiers show: the staff dev is the
one who says a task is wrong *before* it is started, while the junior asks rather than
guessing. QA asks for the failing test when a fix arrives without one — and says plainly
when something is fine.

Watch for the invariants doing work. On the example agenda above, a good table notices
that the endpoint reads gate decisions and therefore needs a permission check rather than
inlined role logic, and that "who may call it" is the overseer question, not a
convenience.

The rules they are working from are in the shared handbook, which you can read and edit on
the **Knowledge** page — it is ordinary workspace content, not something baked into the
agents.

## Taking it further

To have the team work on a real checkout — reading files, making changes, running the test
suite — register the repository in **Repos** and select it when creating the session. That
needs an execution engine configured on your deployment, which is a deployment concern
rather than something a bundle can carry.
