# Resolve project root (directory of this script)
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"
export PYTHONUNBUFFERED=1

# Utilities
log() { printf '%s\n' "$*" >&2; }

# Find Python
PYTHON="$(command -v python3 || command -v python || true)"
if [ -z "$PYTHON" ]; then
    log "ERROR: python3 or python is required but not found in PATH."
    exit 1
fi

# Create and activate venv
VENV_DIR="$PROJECT_ROOT/venv"
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtualenv in $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
. "$VENV_DIR/bin/activate"

# Upgrade pip and install requirements if any
pip install --upgrade pip setuptools wheel >/dev/null
if [ -f "$PROJECT_ROOT/Python/requirements.txt" ]; then
    log "Installing Python requirements"
    pip install -r "$PROJECT_ROOT/Python/requirements.txt"
fi

# Prepare logs folder
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

# Ensure we clean up background processes on exit
PIDS=()
cleanup() {
    log "Stopping background processes..."
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" >/dev/null 2>&1; then
            kill "$pid" || true
        fi
    done
    wait || true
}
trap cleanup EXIT INT TERM

# Start Python services (background)
if [ -f "$PROJECT_ROOT/Python/websockets/main.py" ]; then
    log "Starting websockets/main.py"
    (cd "$PROJECT_ROOT/Python/websockets/" && python main.py >> "$LOG_DIR/websockets.log" 2>&1) &
    PIDS+=($!)
else
    log "Warning: websockets/main.py not found (skipping)"
fi

if [ -f "$PROJECT_ROOT/Python/API/main.py" ]; then
    log "Starting API/main.py"
    (cd "$PROJECT_ROOT/Python/API" && uvicorn main:app --host 0.0.0.0 --port 8001 >> "$LOG_DIR/api.log" 2>&1) &
    PIDS+=($!)
else
    log "Warning: API/main.py not found (skipping)"
fi

# Run npm install --production and start Node app
# If there's a "node" subdirectory use it, otherwise use project root
if [ -d "$PROJECT_ROOT/node" ]; then
    NODE_DIR="$PROJECT_ROOT/node"
else
    NODE_DIR="$PROJECT_ROOT"/UI
fi

if command -v npm >/dev/null 2>&1; then
    if [ -f "$NODE_DIR/package.json" ]; then
        log "Running npm install --production in $NODE_DIR"
        (cd "$NODE_DIR" && npm install --production) >/dev/null
    else
        log "Warning: package.json not found in $NODE_DIR (skipping npm install)"
    fi

    if [ -f "$NODE_DIR/app.js" ]; then
        log "Starting Node app.js"
        (cd "$NODE_DIR" && node app.js >> "$LOG_DIR/node.log" 2>&1) &
        PIDS+=($!)
    else
        log "Warning: app.js not found in $NODE_DIR (skipping node start)"
    fi
else
    log "WARNING: npm not found in PATH; skipping Node steps"
fi

# Run Chromium browser (background)
(log "Starting Chromium on host"; DISPLAY=:0 chromium --incognito --noerrdialogs "$CHROMIUM_URL") &
PIDS+=($!)


# If no background services launched, exit
if [ "${#PIDS[@]}" -eq 0 ]; then
    log "No services were started. Exiting."
    exit 1
fi

log "Services started (PIDs: ${PIDS[*]}). Logs: $LOG_DIR"
# Wait for background processes (so script keeps running)
wait