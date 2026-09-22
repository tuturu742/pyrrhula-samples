# A build environment for loxia: Rust plus the pieces its crates link against.
#
# These four things used to run as setup commands on every delegation -- a rustup
# component add and an apt-get install of libmpv-dev, in a fresh container, once per work
# item. Six work items meant six apt fetches of the same packages before any code was
# written. Baking them is the difference between a build environment and a base image
# that has to become one each time.
#
# git and ca-certificates are not optional here: the agent clones over HTTPS before it
# runs anything, so an image without them cannot start.
FROM docker.io/library/rust:1.97.1-bookworm

RUN apt-get update -qq \
 && apt-get install -y -qq --no-install-recommends \
      git \
      ca-certificates \
      pkg-config \
      libmpv-dev \
 && rm -rf /var/lib/apt/lists/*

RUN rustup component add rustfmt clippy

# Fail the build rather than the first delegation that uses it: an image that cannot
# find libmpv is a broken image, and finding that out inside an agent's container turns
# a packaging mistake into a confusing test failure.
RUN pkg-config --exists mpv \
 && cargo --version \
 && cargo clippy --version \
 && cargo fmt --version \
 && git --version
