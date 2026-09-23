# A preview environment for loxia: ttyd plus the shared libraries the built binary links
# against at runtime.
#
# The build image (loxia-build.Containerfile) carries the Rust toolchain and libmpv-DEV;
# this one carries neither. A preview extracts an artifact that is already compiled, so
# what it needs is the runtime half: libmpv2, a terminfo database good enough for a
# full-screen TUI, and something that can put a terminal on an HTTP port.
#
# python is in the base for the platform's own static-site fallback -- an image used for
# previews should still be able to serve one if the recipe ever falls back to the
# default, and the published ttyd image is Alpine with no Python at all.
FROM docker.io/library/python:3.12-slim-bookworm

RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends \
      ca-certificates \
      ncurses-term \
      libmpv2 \
 && rm -rf /var/lib/apt/lists/*

ADD https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 /usr/local/bin/ttyd
RUN chmod +x /usr/local/bin/ttyd

ENV TERM=xterm-256color

# Fail here rather than in a preview container nobody is watching: an image that cannot
# find libmpv gives the player a dynamic-link error on startup, which reads as a broken
# build of the application rather than a missing package in the preview image.
RUN ttyd --version \
 && ldconfig -p | grep -q libmpv
