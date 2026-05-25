#!/bin/bash
# Auto-rebuild on file changes
# Usage: ./docker/dev-watch.sh

set -e
cd "$(dirname "$0")/.."

echo "[watch] Watching for changes in .cgi .pl .js .php .html .css files..."
echo "[watch] Press Ctrl+C to stop."

LAST_BUILD=0

while true; do
  # Find the most recently modified source file
  LATEST=$(find . \( -name "*.cgi" -o -name "*.pl" -o -name "*.js" -o -name "*.php" -o -name "*.html" -o -name "*.css" -o -name "Dockerfile" -o -name "docker-compose.yml" -o -path "./docker/*" \) \
    ! -path "*/node_modules/*" ! -path "*/ckeditor/*" ! -path "*/kcfinder/*" \
    -exec stat -f "%m" {} \; 2>/dev/null | sort -rn | head -1)

  if [ -z "$LATEST" ]; then
    sleep 3
    continue
  fi

  if [ "$LATEST" -gt "$LAST_BUILD" ]; then
    echo ""
    echo "[watch] Change detected at $(date '+%H:%M:%S'), rebuilding..."
    docker compose up -d --build
    LAST_BUILD=$(date +%s)
    echo "[watch] Done. Watching for changes..."
  fi

  sleep 2
done
