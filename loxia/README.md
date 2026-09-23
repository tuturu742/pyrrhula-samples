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
"preview_image": "localhost:5000/loxia-preview:1",
"preview_cmd": "chmod +x ./loxia-player && ttyd -p 8080 -W ./loxia-player",
"preview_port": 8080,
"preview_env": { "TERM": "xterm-256color" }
```

Build and push it the same way:

```bash
podman build -t localhost:5000/loxia-preview:1 -f loxia-preview.Containerfile .
podman push --tls-verify=false localhost:5000/loxia-preview:1
```

The same three fields can live in the repository instead, as `pyrrhula-preview.json` at
its root — see `docs/previews.md` in the Pyrrhula repo for which layer wins. They are here
because loxia is somebody else's repository and this sample should not require a commit to
it.

## Setting it up

```bash
python scripts/seed_samples.py \
  --secrets-dir /path/to/secrets \
  --samples-dir /path/to/pyrrhula-samples \
  --samples loxia=pyrrhula
```

`loxia=pyrrhula` means "a tenant called `loxia`, from the `pyrrhula` bundle's cast". The
seed then reads `repos.json` from this directory, registers the runtime it names, seals
your token, and registers the repository.

By hand, it is the same four things: import the cast bundle, register the runtime under
**Repos → Build runtimes**, add the repository under **Repos → Register repo** with its
token, and set its test and build commands.

## What it should be able to do

- **Plan against the real codebase.** Run *Analyze repos* first; the planning discussion
  should reference files that exist rather than files a model would expect.
- **Delegate work that lands.** Each work item becomes a branch and a pull request opened
  by the bot's own identity, not the repository owner's.
- **Review what came back**, against the actual diff, and refuse to merge a red build.
- **Preview a branch.** Build it from **Repos → Builds**, then start a preview: the player
  comes up in a terminal in the browser, reading the recipe above rather than the
  static-site default.

That last one is worth expecting rather than fearing: loxia has five failing snapshot
tests on `main`, so a reviewer that approves everything is a reviewer that is not reading.
