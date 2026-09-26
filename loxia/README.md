# loxia — agents working on a real repository

The other samples build a table and let it talk. This one points a table at a repository
that already exists, on a git host, with its own build and its own failing tests, and asks
it to do work that ends in a pull request somebody has to review.

**loxia** is a terminal Emby music client written in Rust — ratatui for the interface,
libmpv2 for playback. Nothing about it was written for Pyrrhula, which is the point: it
has a real dependency that will not compile without a system library, a test suite with
pre-existing failures, and a maintainer who has opinions about its documentation.

## What is different about this sample

There is no `.pyr` here. A bundle carries a cast, its briefs and its flow — it has never
carried a repository registration, because that is half configuration and half
credential, and a bundle holds neither by design.

So this sample is two pieces:

- **the cast** comes from [`../pyrrhula/pyrrhula.pyr`](../pyrrhula/pyrrhula.pyr) — an
  architect, a tiered bench of four developers, and QA. The same bench works on any
  codebase; nothing in it is specific to Pyrrhula's own source.
- **the repository** is declared in [`repos.json`](repos.json) beside this file, and the
  token to reach it is read from your secrets directory when you set the tenant up.

## Before you start

- a Pyrrhula deployment with delegated coding enabled (a container engine it can reach)
- a GitHub token with **Contents: write** and **Pull requests: write** on the repository
  you are pointing at
- a container image with a Rust toolchain **and libmpv**, reachable from wherever your
  agents build

### The build image

loxia does not compile against a stock Rust image: `libmpv2` links against libmpv, and
`pkg-config` has to find it. You can express that two ways.

**As setup commands** — simplest, and re-run on every delegation:

```json
"runtime": "custom",
"runtime_image": "docker.io/library/rust:1.97.1-bookworm",
"setup_cmds": [
  "rustup component add rustfmt clippy",
  "apt-get update -qq && apt-get install -y -qq --no-install-recommends libmpv-dev pkg-config"
]
```

**Or baked into an image** — what `repos.json` here does. Six work items meant six
identical `apt-get` fetches before any code was written; the image does it once:

```dockerfile
FROM docker.io/library/rust:1.97.1-bookworm
RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends git ca-certificates pkg-config libmpv-dev \
 && rm -rf /var/lib/apt/lists/*
RUN rustup component add rustfmt clippy
# Fail here rather than inside an agent's container days later.
RUN pkg-config --exists mpv && cargo --version && cargo clippy --version && git --version
```

Build it and push it somewhere your executor can pull from. On a local k3s that is the
registry the cluster already trusts — no public registry involved:

```bash
podman build -t localhost:5000/loxia-build:1 -f loxia-build.Containerfile .
podman push --tls-verify=false localhost:5000/loxia-build:1
```

`repos.json` then names it as the `rust-mpv` runtime, and every repository in the tenant
can select that name instead of repeating the image.

### The preview image

Building loxia and *running* it need different images. The build image carries the Rust
toolchain and `libmpv-dev`; a preview starts from an artifact that is already compiled, so
what it needs is the runtime half — `libmpv2`, a terminfo database, and something that can
put a terminal on an HTTP port.

loxia has no web interface at all, which is exactly the case the static-site default gets
wrong: it would serve a directory listing containing one executable. `repos.json` gives it
a real recipe instead — `ttyd`, which puts the TUI in a browser tab:

```json
"preview_image": "localhost:5000/loxia-preview:5",
"preview_cmd": "chmod +x ./loxia-player && ttyd -p 8080 -W ./loxia-player",
"preview_port": 8080,
"preview_env": { "TERM": "xterm-256color" }
```

Build and push it the same way, and **give it a new tag every time**:

```bash
podman build -t localhost:5000/loxia-preview:5 -f loxia-preview.Containerfile .
podman push --tls-verify=false localhost:5000/loxia-preview:5
```

Rebuilding under the tag already in `repos.json` is the one thing to avoid. A node that
has pulled that tag once keeps its copy — the pull policy is `IfNotPresent` — so the
preview goes on running days-old bytes while the registry holds the fix, and the symptom
is whatever the old image lacked (here it was `python3: not found`) rather than anything
that says "stale image". Bump the tag, bump this file, and the pull is unavoidable.

The same three fields can live in the repository instead, as `pyrrhula-preview.json` at
its root — see `docs/previews.md` in the Pyrrhula repo for which layer wins. They are here
because loxia is somebody else's repository and this sample should not require a commit to
it.

## Setting it up

1. **Sign up**, choose **Workflows → Software Development**, add a model connection and
   import [`../pyrrhula/pyrrhula.pyr`](../pyrrhula/pyrrhula.pyr) — steps 1 to 5 of the
   [pyrrhula sample](../pyrrhula/README.md), which this one borrows its cast from.
2. **Register the build runtime.** **Repos → Build runtimes**: name `rust-mpv`, image
   `localhost:5000/loxia-build:1` (the image you built above), no setup commands.
3. **Register the repository.** **Repos → Register**, with the values from
   [`repos.json`](repos.json) — the file is the form, as data:

   | field | value |
   |---|---|
   | Name / Key | `loxia` |
   | Import from | `https://github.com/tuturu742/loxia-player` |
   | Access token | your GitHub token (Contents: write, Pull requests: write) |
   | Git provider | GitHub |
   | Runtime | `rust-mpv` |
   | Test command | `cargo test --workspace --lib --bins --tests` |
   | Build command | `cargo build --release --bin loxia-player && mkdir -p .pyrpkg && cp target/release/loxia-player .pyrpkg/ && tar czf loxia.tar.gz -C .pyrpkg .` |
   | Artifact file | `loxia.tar.gz` |
   | Preview recipe | image `localhost:5000/loxia-preview:5`, command `chmod +x ./loxia-player && ttyd -p 8080 -W ./loxia-player`, port `8080`, environment `TERM=xterm-256color` |

   The token is sealed on save and never shown again. Registration clones the repository
   into the hosted store; **Analyze repos** afterwards builds the knowledge graph the
   planning phases read.
4. **Start a session** on the *Plan, implement, review* flow with the architect as
   supervisor and the bench as participants, and select the `loxia` repository when you
   create it — that is what makes delegated work available to the phases that ask for it.

## What it should be able to do

- **Plan against the real codebase.** Run *Analyze repos* first; the planning discussion
  should reference files that exist rather than files a model would expect.
- **Delegate work that lands.** Each work item becomes a branch and a pull request opened
  by the bot's own identity, not the repository owner's.
- **Review what came back**, against the actual diff, and refuse to merge a red build.
- **Preview a branch.** A preview serves a build artifact, and the artifact is produced by
  a delegation: the agent's container runs the test command, then the build command, and
  uploads `loxia.tar.gz` when the build exits clean. There is no button that builds a
  repository on its own — the build is part of doing the work, not a separate step. Once a
  delegation on a branch has produced the artifact, start a preview on that branch and the
  player comes up in a terminal in the browser, reading the recipe above rather than the
  static-site default.

  **This repository cannot produce one yet, and that is the sample working as intended.**
  The build step runs only when the test command passed, and loxia's trunk has failing
  snapshot tests on purpose — they are what makes the review scenario real, because a
  reviewer that approves a red build is a reviewer that is not reading. So a delegation
  here reports `tests failed`, the build is skipped, no artifact is uploaded, and there is
  nothing to preview. Preview a branch once the tests on it are green: the agents fixing
  them is the same loop, one increment further on.

That last one is worth expecting rather than fearing: loxia has five failing snapshot
tests on `master`, so a reviewer that approves everything is a reviewer that is not reading.

### What is actually wrong with them

Not stale fixtures. `loxia_core::local_hour_minute` renders through
`jiff::tz::TimeZone::system()`, and the header and the now-playing history both print a
clock through it, so the rendered output depends on the timezone of whatever machine ran
the test. The committed `.snap` files were generated in one zone and the test container
runs in another, which is why the diffs show the same layout an hour or two apart.

This is worth knowing before you judge a fix, because one obvious move is wrong on its
own. Running `cargo insta accept` and committing the result, with nothing else changed,
pins the fixtures to whatever zone that particular run happened to be in: the suite goes
green there and breaks for everyone whose machine disagrees, which is the same bug facing
the other way.

What makes accepting correct is pinning the zone first, so that every run agrees. Two
ways do that, and both are legitimate:

- **Pin the environment.** An `[env]` table in `.cargo/config.toml` setting `TZ = "UTC"`
  fixes the zone for processes cargo launches -- build scripts and test binaries -- and
  leaves an already-built `loxia-player` alone, so the shipped player still shows the
  user's real local time. Regenerated fixtures are then portable.
- **Pin the input.** A zone-taking variant of `local_hour_minute`, with production
  passing the system zone and the tests a fixed one. Heavier, and the better shape if the
  clock ever needs to be controlled per test rather than per run.

So the question to ask of a green branch is not whether it touched `loxia-core`. It is
whether anything in it makes the zone the same on every machine. If the only change is
regenerated `.snap` files, it does not, and the branch is green by luck.
