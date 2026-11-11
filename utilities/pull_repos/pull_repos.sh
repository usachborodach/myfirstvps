#!/usr/bin/env bash
#
# Синхронизация списка git-репозиториев с их remote.
# Запускается из cron, например:
#   */5 * * * * /root/myfirstvps/utilities/pull_repos/pull_repos.sh >> /var/log/sync-repos.log 2>&1
#
set -uo pipefail

# Минимальный PATH для cron-окружения
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

REPOS=(
  /root/ML-AI-Engineer-Interview-Handbook
  /root/myfirstvps
  /root/qanda
)

log() { printf '%s %s\n' "$(date '+%F %T')" "$*"; }

sync_repo() {
  local repo=$1 cur rem

  if [[ ! -d "$repo/.git" ]]; then
    log "skip (not a git repo): $repo"
    return 0
  fi

  if ! git -C "$repo" fetch --quiet --prune; then
    log "fetch failed: $repo"
    return 1
  fi

  cur=$(git -C "$repo" rev-parse HEAD)
  if ! rem=$(git -C "$repo" rev-parse origin/main 2>/dev/null); then
    log "origin/main not found: $repo"
    return 1
  fi

  [[ "$cur" == "$rem" ]] && return 0

  log "pulling: $repo ($cur -> $rem)"
  if git -C "$repo" pull --ff-only --quiet; then
    log "updated: $repo"
  else
    log "pull failed: $repo"
    return 1
  fi
}

for repo in "${REPOS[@]}"; do
  sync_repo "$repo"
done