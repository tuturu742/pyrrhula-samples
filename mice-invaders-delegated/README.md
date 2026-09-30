# Mice Invaders — the building version

A studio lead and a senior developer building the cat-vs-mice game **in a real repository**:
Godot 4, GDScript, tests that run headless. The developer works through a **coding
harness** — an agent loop with a shell inside its own container, which reads the project,
writes the rules and their tests, runs the suite and iterates before anything is committed.

**Why this sample exists.** There is already a
[`mice-invaders`](../mice-invaders/) sample here, and it is a *conversation*: two agents
discussing the same game, no repository, no execution engine, a minute to run. This one
does the work. Read that one first if you want to see how the pair reasons; read this one
to see a pull request come out of it.

It is also the sample that exercises the awkward case: **the runtime Pyrrhula does not
ship.** Godot is not one of the built-in runtimes, so the delegated container needs an
image you build yourself, which is a genuine part of using this platform on a real project
and is therefore not hidden here.

---

## Before you start

- A Pyrrhula deployment with an **execution engine** configured (a Docker or Podman socket,
  or Kubernetes). See `docs/exec-engines.md`.
- A deployment that **offers a coding harness** (`opencode` is a built-in; an administrator
  can withhold it — step 7 says how to tell).
- **A container registry the engine can pull from**, and the ability to build an image.
  Even a local registry is fine. Step 2.
- A model API key. Built and tested on **DeepSeek** (`deepseek-chat`).
- A **GitHub account and a token** — two accounts, if you want the review to be real.

---

## Step 1 — Fork the repository

Fork **[tuturu742/mice-invaders](https://github.com/tuturu742/mice-invaders)**.

Its `main` is deliberately a scaffold: a Godot project file, a small test runner, one
self-test that keeps a fresh clone green, and a README. The working rules live in a pull
request on the upstream repo, built by this sample.

**Fork rather than use the upstream directly.** You have no push access there and never
will: delegated work pushes branches and opens pull requests under the credential *you*
give Pyrrhula, and that credential has to own the repository it writes to.

## Step 2 — Build the runtime image

The container needs **Godot** to run the tests and **Node** because the harness installs
itself with `npm i -g` into that same container. A Godot-only image fails at setup before
the agent ever starts.

`godot.Dockerfile`:

```dockerfile
FROM docker.io/library/node:20-bookworm
ARG GODOT_VERSION=4.3-stable

RUN apt-get update \
 && apt-get install -y --no-install-recommends unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/godot.zip \
      "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/Godot_v${GODOT_VERSION}_linux.x86_64.zip" \
 && unzip -q /tmp/godot.zip -d /tmp \
 && mv "/tmp/Godot_v${GODOT_VERSION}_linux.x86_64" /usr/local/bin/godot \
 && chmod +x /usr/local/bin/godot \
 && rm -rf /tmp/godot.zip

ENV HOME=/root
ENV XDG_DATA_HOME=/root/.local/share
ENV XDG_CONFIG_HOME=/root/.config

RUN godot --headless --version
```

Build it, then **push it to a registry** — including on a socket engine:

```sh
podman build -t localhost/pyr-godot-node:4.3 -f godot.Dockerfile .

# A local registry is enough, if you do not already have one:
podman run -d --name pyr-registry --restart=always \
  -p 127.0.0.1:5000:5000 -v pyr-registry:/var/lib/registry docker.io/library/registry:2

podman push --tls-verify=false localhost/pyr-godot-node:4.3 localhost:5000/pyr-godot-node:4.3
```

> **A socket engine pulls too.** It is tempting to assume that a Podman or Docker socket
> engine, running containers on the same host, can use an image you just built there. It
> cannot: Pyrrhula asks the engine to pull every image before provisioning, so a bare
> `localhost/...` name has no registry behind it and the delegation fails at provisioning.

> **A plain-HTTP registry has to be trusted, not merely reachable**, or the pull fails with
> `server gave HTTP response to HTTPS client` — which reads like a broken image rather than
> a registry setting. Rootless Podman: `~/.config/containers/registries.conf`
>
> ```toml
> [[registry]]
> location = "localhost:5000"
> insecure = true
> ```
>
> k3s: `mirrors:` in `/etc/rancher/k3s/registries.yaml`, then restart k3s.

> Pyrrhula does not build this image for you. An image builder is on the roadmap and is not
> in the product yet, so a custom runtime is currently an image an operator builds and
> hosts. There is nothing in the UI that does it, which is why this step is spelled out.

## Step 3 — Make the GitHub token(s)

A classic personal access token with the **`repo`** scope, able to push to your fork.
Pyrrhula seals it; it is never displayed again and never reaches the container.

**Optional, and worth it:** a *second* account's token, because GitHub will not let an
account approve a pull request it opened. The second account has to be a **collaborator on
your fork** first, or its token sees a `404`.

## Step 4 — Sign up

Register with any organization name. You land in **Default Workspace** as its **steward**.

## Step 5 — Choose the Software Development workflow

**Before importing.** **Workflows** → **Software Development** — the workflow that grants
repository access at all.

## Step 6 — Add your model connection

**Personas** (top nav) **→ Model profiles → New model profile**: name `DeepSeek`, provider
`deepseek`, model `deepseek-chat`, and your API key.

## Step 7 — Import the project

Workspace → **Export / import** (top right) → upload
[`mice-invaders-delegated.pyr`](mice-invaders-delegated.pyr).

The bundle carries **the cast and nothing else**: 2 personas, `Studio Lead Ash` and
`Senior Developer Juno`. No flow — selecting the workflow in step 5 already provided *Plan,
Implement, Review, Merge*, and a second copy would appear in the picker under the same name.

The report will say, twice, that a persona was **bound to a placeholder (connection did not
travel)**. That is expected, and it is the next step: a sample must not ship anybody's API
key.

**Read the import report.** If it says

> `harness:dev wanted 'opencode', which this deployment does not offer`

the run still works, but on the one-shot path — the model answers with whole files and never
executes anything, so the test-and-fix loop this sample is about will not happen. A harness
*key* travels in a bundle; the command never does, and the key is resolved against your
deployment's own registry.

## Step 8 — Point the pair at your connection

**Personas** → open `Studio Lead Ash` and `Senior Developer Juno` → set **Connection (model
agent)**. Confirm `Senior Developer Juno` shows **Harness: `opencode`** on the roster.

## Step 9 — Register your fork

**Repos → New repo**:

| Field | Value |
|---|---|
| Key | `mice-invaders` |
| Name | `Mice Invaders` |
| Source URL | `https://github.com/<you>/mice-invaders` |
| Access token | the token from step 3 |
| Runtime | `custom` |
| Runtime image | `localhost:5000/pyr-godot-node:4.3` |
| Test command | `godot --headless --path . --script tests/run_tests.gd` |

**If you made a second token:** open the repo → **Persona credentials** → bind
`Studio Lead Ash` to it.

## Step 10 — Set a daily cap

**Usage → Limits** → a **per-persona daily token cap**. A successful run here costs roughly
**40k–80k** tokens; a few hundred thousand is ample and stops a confused run with an "on
hold" note rather than a bill.

## Step 11 — Start the session

New session:

- **Process definition**: `Plan, Implement, Review, Merge`
- **Supervisor**: `Studio Lead Ash`
- **Participant**: `Senior Developer Juno`
- **Repos**: your fork
- **Agenda**:

```
Build Mice Invaders -- Space Invaders, except the player is a cat and the invaders are mice
-- starting with the rules that need no scene at all.

Create exactly ONE work item, with a description that stands alone -- a coding agent reads
only it -- asking for all of:

- scripts/formation.gd: a plain RefCounted class, no scene dependencies, holding the
  swarm's rules: lay out a grid of mice (rows, columns, spacing, an origin); step the
  formation sideways by its current speed; when any mouse would cross a left or right
  bound, drop the whole formation by one row and reverse direction instead of stepping;
  and report how fast it should be moving given how many mice are left, so the swarm
  speeds up as it is destroyed and is fastest with one mouse remaining.
- tests/test_formation.gd extending res://tests/test_case.gd, covering the initial layout,
  a plain step, the edge case that drops and reverses, and the speed-up at full strength,
  half strength and one mouse left.
- Read tests/run_tests.gd FIRST and follow the contract it already sets: every method named
  test_* is run, assertions come from the base class, no test framework is added.
- `godot --headless --path . --script tests/run_tests.gd` must exit 0 before the item is
  done, and tests/test_scaffold.gd should be deleted once there are real tests, since it
  exists only to keep a fresh clone green.
- README.md left alone.

Keep the rules pure and the numbers explicit. A reviewer should read the test file and know
what the swarm does without opening the implementation.
```

Do **not** press *Continue* after creating the session — creating it already starts the
autonomous run, and a second kick races the first.

---

## What you should see

`Studio Lead Ash` turns the agenda into a work item and delegates it. Then, in the
transcript: the container it created (on your custom image), the harness installing itself,
and the agent reading `tests/run_tests.gd` **before** writing tests — which is the
behaviour the persona asks for and the clearest sign the harness is really reading the
repository rather than guessing at it. Then `scripts/formation.gd`, then the suite, then
whatever it got wrong, then the fix.

A bounded summary comes back in Juno's own voice — something like *"10 steps (read ×5, bash
×3, write ×2) · 55,062 tokens — All 5 tests pass"* — and the pull request lands on your
fork, approved by the other account if you bound one.

---

## What this sample does not do well

- **There is no game yet.** One work item, the pure rules, tested. No scene, no sprites, no
  player. That is the honest first increment for a headless test container, and the second
  session is where a scene would come from.
- **One pull request is not how the flow behaves by default.** The agenda forces a single
  work item because a showcase should be readable; left alone the lead plans several.
- **The custom image is a real cost.** Roughly 400 MB and a few minutes to build, and it
  has to live somewhere the engine can pull from. On a one-shot engine (Kubernetes, ECS)
  every delegation pulls it again and reinstalls the harness on top — about a minute per
  run. That is the case the roadmap's image builder exists to fix.
- **Godot 4.3 is pinned** in the Dockerfile and in `project.godot`'s `config/features`. A
  newer Godot will open the project and offer to upgrade it; the tests do not care, but the
  version skew is yours to manage.

## Taking it further

- **Add the scene, and a preview.** Previews serve a build artifact over HTTP, and a Godot
  **web export** is exactly that. Add an `export_presets.cfg` with a preset named `Web`,
  set the repo's **Build command** to
  `godot --headless --export-release Web build/web/index.html && tar czf web.tgz -C build/web .`
  and its **Artifact file** to `web.tgz`, and the *Preview deployments* card can then serve
  a playable build of any green branch. Both fields are required — with either missing
  there is no build step at all and **Deploy** has nothing to serve.
- **Compare with the conversation.** Run [`../mice-invaders`](../mice-invaders/) on the same
  agenda and read the two transcripts side by side. One reasons about the work; this one
  does it.
- **Turn the harness off** on `Senior Developer Juno` and run the same agenda: the one-shot
  path writes whole files and never runs the suite. The diff is the argument for harnesses.
