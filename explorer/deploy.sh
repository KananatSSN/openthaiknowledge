#!/usr/bin/env bash
# Build and (re)start the explorer from a release of otk, on the machine that
# serves it. Run from anywhere inside a clone of openthaiknowledge:
#
#   explorer/deploy.sh            # the newest release tag
#   explorer/deploy.sh v0.4.0     # a given tag
#   explorer/deploy.sh stop
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
compose() { docker compose -f explorer/compose.yml "$@"; }

if [ "${1:-}" = "stop" ]; then
  compose down
  exit 0
fi

docker info >/dev/null 2>&1 || { echo "Docker is not running. Open Docker Desktop and try again." >&2; exit 1; }
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "This clone has local changes; commit or discard them first." >&2
  exit 1
fi

git fetch --quiet --tags origin
tag="${1:-$(git tag --list 'v*' --sort=-v:refname | head -n 1)}"
[ -n "$tag" ] || { echo "No release tag found." >&2; exit 1; }
git -c advice.detachedHead=false checkout --quiet "$tag"
echo "Building the explorer from ${tag}..."
compose up -d --build --remove-orphans

port="${EXPLORER_PORT:-8090}"
for _ in $(seq 1 30); do
  if curl -fsS -o /dev/null "http://127.0.0.1:$port/data/catalog.json"; then
    echo "The explorer ($tag) is up on http://127.0.0.1:$port"
    exit 0
  fi
  sleep 1
done
echo "The explorer did not answer on port $port; see: docker compose -f explorer/compose.yml logs" >&2
exit 1
