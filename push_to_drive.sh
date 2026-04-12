#!/usr/bin/env bash
set -euo pipefail

REMOTE="gdrive"
DEST_FOLDER="buildco3"
FILTER_FILE=".rclone-filters"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

# Default to dry-run for safety
DRY_RUN="--dry-run"
if [[ "${1:-}" == "--go" ]]; then
    DRY_RUN=""
    shift
fi

rclone copy "$SRC_DIR" "${REMOTE}:${DEST_FOLDER}" \
    --filter-from "${SRC_DIR}/${FILTER_FILE}" \
    --progress \
    $DRY_RUN \
    "$@"

if [[ -n "$DRY_RUN" ]]; then
    echo ""
    echo "This was a DRY RUN. Run with --go to actually push:"
    echo "  ./push_to_drive.sh --go"
fi
