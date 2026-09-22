# Mice Invaders

A studio lead and a developer building a small browser game: Space Invaders, except the
player is a cat and the invaders are mice.

**Why this sample exists.** It is the smallest honest version of delivery work — someone
decides what "done" means for one increment, someone else builds it, and the result is
reviewed against the conventions rather than against taste. Two agents, three phases, no
secrets.

---

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

## Step 4 — Import the project

Workspace → **Export / import** (top right) → upload [`mice-invaders.pyr`](mice-invaders.pyr).

You should see **2 personas** (`lead`, `dev`), **1 flow** ("Build and review"), and the
studio conventions as a knowledge attachment. No secrets — this sample has none.

## Step 5 — Point the pair at your connection

**Personas** → open `Studio Lead` and `Game Developer` → set **Connection (model agent)**
to your connection.

## Step 6 — Start the session

New session:

- **Process definition**: `Build and review`
- **Supervisor**: `Studio Lead`
- **Participant**: `Game Developer`
- **Agenda**:

```
Build the cat-vs-mice browser game one increment at a time. Start with the pure rules: the
invader grid layout, how the formation marches and drops a row at an edge, and how it
speeds up as mice are destroyed. Keep the logic testable without a running scene.
```

---

## What you should see

The lead opens by naming **one** increment and what done means for it — not the whole
game. The developer answers with complete GDScript files rather than fragments, keeping
pure logic separate from scene code. The review phase either accepts the work or says
precisely what is wrong with it.

Both agents know the conventions (one increment per turn, complete files, the build stays
green, art is optional so a missing sprite never blocks) because those are in the shared
studio-conventions handbook, which every agent retrieves.

## Taking it further

This sample is the conversation, not the repository. To have the agents actually commit
code, run tests and produce a playable build, register a repo in **Repos** and select it
when you create the session — then the developer can be given real delegated work against
it. That path needs an execution engine configured on your deployment (Docker/Podman,
Kubernetes or AWS), which is a deployment concern rather than something a bundle can carry.
