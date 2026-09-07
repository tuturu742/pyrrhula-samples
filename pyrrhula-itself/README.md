# Working on Pyrrhula itself

An architect, an implementer and a reviewer working on the Pyrrhula codebase — the
dogfood sample.

**Why this sample exists.** The interesting part is not that three agents discuss code. It
is that they share a written set of invariants, and the architect's job is to hold the line
on them: if a proposed change would break tenancy isolation, or put secret plaintext where
exclusion should have removed it, or add an UPDATE grant to an append-only table, that is
the objection — not a matter of style.

---

## Before you start

A Pyrrhula deployment and an API key. Built and tested on **DeepSeek** (`deepseek-chat`).

---

## Step 1 — Sign up

Register with any organization name. You land in **Default Workspace** as its **steward**.

## Step 2 — Choose the Software Development workflow

**Before importing.** **Workflows** → **Software Development**.

## Step 3 — Add your model connection

**Personas → Model profiles → New**: name `DeepSeek`, provider `deepseek`, model
`deepseek-chat`, and your API key.

## Step 4 — Import the team

Workspace → **Export / Import** → upload [`pyrrhula-itself.pyr`](pyrrhula-itself.pyr).

You should see **3 personas** (`architect`, `implementer`, `reviewer`), **1 flow** ("Plan,
implement, review"), and the ground rules as a knowledge attachment. No secrets.

## Step 5 — Point the team at your connection

**Personas** → open each of the three → set its **model profile** to your connection.

## Step 6 — Start the session

New session:

- **Flow**: `Plan, implement, review`
- **Supervisor**: `Architect`
- **Participants**: `Implementer`, `Reviewer`
- **Agenda**: something small and real. For example —

```
We want an endpoint that returns the disclosure decisions for one session, so an overseer
can audit what the gate concealed and why. Decide what it should return, who may call it,
and what would have to be tested before it ships.
```

---

## What you should see

The architect breaks the work into one change with a stated definition of done. The
implementer proposes it against the ground rules. The reviewer asks for the failing test
when a fix arrives without one — and says plainly when something is fine.

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
