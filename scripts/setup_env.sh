#!/usr/bin/env bash
set -euo pipefail

# Setup a local virtual environment and install dependencies.
# Usage: ./scripts/setup_env.sh [--run-smoke]

VENV_DIR=".venv"
PYTHON_CMD="${PYTHON:-python3}"
RUN_SMOKE=0

if [ "${1-}" = "--run-smoke" ]; then
  RUN_SMOKE=1
fi

echo "Using python: $(command -v "$PYTHON_CMD" 2>/dev/null || echo 'not found')"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  echo "ERROR: Python executable '$PYTHON_CMD' not found. Install Python 3.10+ or set PYTHON env var."
  exit 1
fi

if [ -d "$VENV_DIR" ]; then
  echo "Virtualenv $VENV_DIR already exists. Skipping creation." 
else
  echo "Creating virtual environment in $VENV_DIR..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

echo "Upgrading pip and build tools inside venv..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel

if [ -f requirements.txt ]; then
  echo "Installing requirements from requirements.txt..."
  "$VENV_DIR/bin/pip" install -r requirements.txt
else
  echo "No requirements.txt found; skipping pip install -r requirements.txt"
fi

if [ -f pyproject.toml ]; then
  echo "Installing project in editable mode (pyproject.toml present)..."
  "$VENV_DIR/bin/pip" install -e .
else
  echo "No pyproject.toml found; skipping editable install"
fi

echo
echo "DONE. Activate the environment with:"
echo "  source $VENV_DIR/bin/activate"

if [ "$RUN_SMOKE" -eq 1 ]; then
  echo "Running smoke test: running scripts/reconcile.py --outdir out"
  "$VENV_DIR/bin/python" scripts/reconcile.py --outdir out
  echo "Smoke test complete. Check outputs in ./out/"
fi
