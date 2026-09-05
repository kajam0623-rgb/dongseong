#!/usr/bin/env bash
#
# 지점별 저장소 7개를 만들고 각 사이트를 밀어 넣는다.
#
#   ./tools/create-repos.sh              # 전체
#   ./tools/create-repos.sh mokdong      # 특정 지점만
#   DRY_RUN=1 ./tools/create-repos.sh    # 무엇을 할지만 출력
#
# 사전 조건: gh CLI 로그인 (`gh auth login`)
#   gh auth status 로 확인. 저장소 생성 권한이 있는 개인 계정으로 로그인해야 한다.
#
# 이미 있는 저장소는 만들지 않고 푸시만 한다. 각 저장소는 해당 지점 사이트 폴더가
# 그대로 루트가 되므로, Vercel에서 저장소만 연결하면 추가 설정 없이 배포된다.

set -euo pipefail

OWNER="kajam0623-rgb"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITES="$HERE/sites"
DRY_RUN="${DRY_RUN:-}"

run() {
  if [[ -n "$DRY_RUN" ]]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI가 없습니다. https://cli.github.com 에서 설치한 뒤 'gh auth login' 하세요." >&2
  [[ -z "$DRY_RUN" ]] && exit 1
fi

if [[ -z "$DRY_RUN" ]] && ! gh auth status >/dev/null 2>&1; then
  echo "gh 로그인이 필요합니다: gh auth login" >&2
  exit 1
fi

# slug → 저장소 이름 · 설명
declare -A REPO=(
  [mokdong]="mokdong-anitok|애니톡 목동 본원 랜딩페이지 (정적 사이트)"
  [hongdae]="hongdae-anitok|홍대 애니톡 만화애니학원 랜딩페이지 (정적 사이트)"
  [gangdong]="gangdong-anitok|강동 애니톡 만화애니학원 랜딩페이지 (정적 사이트)"
  [bucheon]="bucheon-anitok|부천 애니톡 만화애니학원 랜딩페이지 (정적 사이트)"
  [gwanggyo]="gwanggyo-anitok|광교 애니톡 만화애니학원 랜딩페이지 (정적 사이트)"
  [gimpo]="gimpo-anitok|김포 애니톡 만화애니학원 랜딩페이지 (정적 사이트)"
  [academy]="academy-anitok|애니톡 웹툰게임 아카데미 랜딩페이지 (정적 사이트)"
)

SLUGS=("$@")
if [[ ${#SLUGS[@]} -eq 0 ]]; then
  SLUGS=(mokdong hongdae gangdong bucheon gwanggyo gimpo academy)
fi

for slug in "${SLUGS[@]}"; do
  entry="${REPO[$slug]:-}"
  if [[ -z "$entry" ]]; then
    echo "알 수 없는 지점: $slug" >&2
    exit 1
  fi
  name="${entry%%|*}"
  desc="${entry#*|}"
  src="$SITES/$slug"

  if [[ ! -d "$src" ]]; then
    echo "$src 가 없습니다. 먼저 'node build.mjs $slug' 를 실행하세요." >&2
    exit 1
  fi

  echo
  echo "== $OWNER/$name  ← sites/$slug"

  if [[ -n "$DRY_RUN" ]]; then
    echo "  [dry-run] gh repo create $OWNER/$name --public --description \"$desc\""
  elif gh repo view "$OWNER/$name" >/dev/null 2>&1; then
    echo "  저장소가 이미 있습니다. 푸시만 진행합니다."
  else
    gh repo create "$OWNER/$name" --public --description "$desc"
  fi

  # 사이트 폴더를 그대로 루트로 하는 임시 클론을 만들어 푸시한다.
  # 원본 sites/ 폴더에는 .git 을 남기지 않는다.
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  cp -R "$src/." "$tmp/"

  if [[ -n "$DRY_RUN" ]]; then
    echo "  [dry-run] $(cd "$tmp" && ls | tr '\n' ' ')를 $OWNER/$name 의 main 으로 푸시"
  else
    (
      cd "$tmp"
      git init -q -b main
      git add -A
      git -c user.name="${GIT_AUTHOR_NAME:-$(git config --global user.name || echo anitok)}" \
          -c user.email="${GIT_AUTHOR_EMAIL:-$(git config --global user.email || echo noreply@anitok.com)}" \
          commit -q -m "$desc"
      git remote add origin "https://github.com/$OWNER/$name.git"
      for i in 1 2 3 4; do
        if git push -u origin main; then break; fi
        echo "  푸시 실패, $((2 ** i))초 후 재시도"
        sleep $((2 ** i))
      done
    )
  fi

  rm -rf "$tmp"
  trap - EXIT
  echo "  완료 → https://github.com/$OWNER/$name"
done

echo
echo "다음 단계: Vercel에서 각 저장소를 Import 하세요."
echo "  프레임워크 프리셋 'Other', 빌드 명령 없음, 출력 디렉터리 기본값 그대로면 됩니다."
