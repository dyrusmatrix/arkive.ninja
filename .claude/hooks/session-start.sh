#!/bin/bash
set -euo pipefail

# Only run in remote Claude Code on the web sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Setting up arkive.ninja (VDO.Ninja) development environment..."

# Install htmlhint for HTML linting (project has no package manager)
if ! command -v htmlhint &>/dev/null; then
  echo "Installing htmlhint..."
  npm install -g htmlhint --silent
fi

# Install serve for local static file preview
if ! command -v serve &>/dev/null; then
  echo "Installing serve..."
  npm install -g serve --silent
fi

echo "Environment ready."
echo "  - htmlhint: $(htmlhint --version)"
echo "  - serve: $(serve --version 2>/dev/null || echo 'available')"
