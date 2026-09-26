# Maintainer tools

Nothing in this directory is part of running a sample. Every sample README describes
setup as steps a person takes in the product, and none of them refers to this folder.

## `roundtrip_bundle.py`

Re-exports a committed `.pyr` through a running Pyrrhula: imports it into a scratch
workspace and exports it again, so the file carries the current bundle format and the
version that produced it. For the day the format changes; not a build step, because a
bundle here is an artefact exported from the product, not something generated.

```bash
python3 tools/roundtrip_bundle.py --api http://localhost:8000 \
  --organization my-org --email me@example.com --password '...' \
  hagnaryd-mystery/hagnaryd-mystery.pyr
```

Stdlib only. Sign in, create a workspace, import, export — the same calls the UI makes.
