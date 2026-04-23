#!/usr/bin/env bash
set -Eeuo pipefail

# =========================
# Config
# =========================
REPO="/Users/xinzhang/daily_paper"
REMOTE="origin"
BRANCH="main"
INTERVAL=600  # 10 minutes

PORT=5001
PIDFILE="/tmp/paper_search_server.pid"
LOGFILE="/tmp/paper_search_server.log"

# =========================
# Helpers
# =========================
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
die() { echo "ERROR: $*" >&2; exit 1; }
git_in_repo() { ( cd "$REPO" && "$@" ); }

fetch_remote() { git_in_repo git fetch "$REMOTE"; }
get_hash() { git_in_repo git rev-parse "${REMOTE}/${BRANCH}" 2>/dev/null | tr -d '\n'; }

# =========================
# Error / Exit
# =========================
on_err() {
  local exit_code=$?
  log "ERROR: command failed at line $1 with exit code $exit_code"
}

on_interrupt() {
  echo
  log "Interrupted. Stopping server..."
  stop_server
  exit 130
}

on_exit() {
  local code=$?
  if [[ $code -eq 0 ]]; then
    log "Supervisor exited normally."
  else
    log "Supervisor exited with error code $code."
  fi
}

trap 'on_err $LINENO' ERR
trap on_interrupt INT TERM
trap on_exit EXIT

# =========================
# Server control
# =========================
stop_server() {
  local pid=""
  if [[ -f "$PIDFILE" ]]; then
    pid="$(cat "$PIDFILE" 2>/dev/null || true)"
  fi

  if [[ -n "${pid:-}" ]] && kill -0 "$pid" >/dev/null 2>&1; then
    log "Stopping server PID=$pid"
    kill "$pid" 2>/dev/null || true

    for _ in {1..15}; do
      if ! kill -0 "$pid" >/dev/null 2>&1; then
        log "Server stopped."
        rm -f "$PIDFILE"
        return 0
      fi
      sleep 1
    done

    log "Force killing server PID=$pid"
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$PIDFILE"
    return 0
  fi

  if pgrep -f "python3 serve_search\.py" >/dev/null 2>&1; then
    log "Stopping stray serve_search.py"
    pkill -f "python3 serve_search\.py" || true
    sleep 1
  fi

  rm -f "$PIDFILE" || true
}

start_server() {
  log "Starting server in background..."
  cd "$REPO"

  : > "$LOGFILE"

  nohup python3 -u serve_search.py \
    --index-dir vector_indices/chunk2500_overlap300_model_embeddinggemma_300m \
    --port "$PORT" >> "$LOGFILE" 2>&1 &

  local pid=$!
  echo "$pid" > "$PIDFILE"
  sleep 2

  if kill -0 "$pid" >/dev/null 2>&1; then
    log "Server started. PID=$pid"
    log "Server log: $LOGFILE"
    return 0
  fi

  log "Server failed to start. Last log:"
  tail -n 50 "$LOGFILE" || true
  return 1
}

# =========================
# Build pipeline
# =========================
run_build_steps() {
  cd "$REPO"

  log "git pull --ff-only"
  git pull --ff-only

  log "Step 1/2: rebuild_faiss (rebuild vector index)"
  if ! python3 -u rebuild_faiss.py; then
    log "WARNING: rebuild_faiss.py failed (non-fatal), continuing..."
  fi

  log "Step 2/2: wiki_build (agent builds wiki)"
  if ! bash wiki_build.sh; then
    log "WARNING: wiki_build.sh failed (non-fatal), continuing..."
  fi
}

restart_all() {
  log "===== Restart begin ====="
  stop_server
  run_build_steps
  start_server
  log "===== Restart done ====="
}

# =========================
# Main
# =========================
[[ -d "$REPO/.git" ]] || die "Repo not found: $REPO"

log "paper_search_server supervisor starting"
log "Repo: $REPO"
log "Watching: ${REMOTE}/${BRANCH}"
log "Interval: ${INTERVAL}s"
log "Port: $PORT"

log "Initial fetch..."
fetch_remote
last_remote="$(get_hash)"
[[ -n "$last_remote" ]] || die "Cannot resolve ${REMOTE}/${BRANCH}"
log "Baseline remote hash: $last_remote"

restart_all

while true; do
  sleep "$INTERVAL"

  log "Checking remote updates..."
  if ! fetch_remote; then
    log "Fetch failed; retry next cycle."
    continue
  fi

  remote_now="$(get_hash || true)"
  if [[ -z "${remote_now:-}" ]]; then
    log "Cannot resolve ${REMOTE}/${BRANCH}; retry next cycle."
    continue
  fi

  if [[ "$remote_now" != "$last_remote" ]]; then
    log "Remote update detected: $last_remote -> $remote_now"

    if restart_all; then
      last_remote="$remote_now"
    else
      log "Restart failed. Will retry next cycle."
    fi
  fi
done
