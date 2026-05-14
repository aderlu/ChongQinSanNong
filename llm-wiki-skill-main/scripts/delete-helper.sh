#!/bin/bash
# llm-wiki 删除辅助脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/shared-config.sh"

usage() {
  cat <<'EOF'
用法：
  bash scripts/delete-helper.sh scan-refs <wiki_root> <素材文件名>
EOF
}

scan_refs() {
  local wiki_root="$1"
  local needle="$2"
  local wiki_dir="$wiki_root/wiki"

  [ -n "$needle" ] || {
    echo "素材文件名不能为空" >&2
    exit 1
  }

  [ -d "$wiki_dir" ] || {
    echo "知识库目录不存在：$wiki_dir" >&2
    exit 1
  }

  {
    grep -rlF --include='*.md' -- "$needle" "$wiki_dir" 2>/dev/null || true
  } | while IFS= read -r path; do
    [ -n "$path" ] || continue
    case "$path" in
      "$wiki_root"/*) printf '%s\n' "${path#"$wiki_root"/}" ;;
      *) printf '%s\n' "$path" ;;
    esac
  done | sort -u
}

command_name="${1:-}"

case "$command_name" in
  scan-refs)
    [ "$#" -eq 3 ] || { usage; exit 1; }
    scan_refs "$2" "$3"
    ;;
  *)
    usage
    exit 1
    ;;
esac
