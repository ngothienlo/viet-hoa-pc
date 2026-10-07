# Nhánh không được commit hoặc push thẳng. Mọi thay đổi vào đây qua PR trên GitHub.
# Hook khác nạp file này bằng `. "$(dirname "$0")/protected-branches.sh"`.
PROTECTED_BRANCHES="main master staging"

is_protected() {
  for name in $PROTECTED_BRANCHES; do
    [ "$1" = "$name" ] && return 0
  done
  return 1
}

refuse() {
  echo "" >&2
  echo "Chặn: $1" >&2
  echo "Tạo nhánh feature/, fix/ hoặc docs/ từ main rồi mở PR. Xem docs/technical/git-hooks.md." >&2
  echo "" >&2
  exit 1
}
