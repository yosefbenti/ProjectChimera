#!/usr/bin/env bash
set -euo pipefail

SPEC_FILE="specs/technical.md"

if [ ! -f "$SPEC_FILE" ]; then
  echo "Spec file $SPEC_FILE not found" >&2
  exit 2
fi

# Basic sanity checks: ensure API Contracts section exists
if grep -q "API Contracts" "$SPEC_FILE"; then
  echo "Found API Contracts in $SPEC_FILE"
  exit 0
else
  echo "API Contracts section missing in $SPEC_FILE" >&2
  exit 1
fi
