#!/usr/bin/env bash
# 빌드 시점에 공개 저장소를 받아 지점 사이트를 생성한다.
# 이 프로젝트는 아직 Git 에 연결돼 있지 않아 배포마다 파일을 수동으로 올려야 한다.
# 산출물을 통째로 다시 올리는 대신 저장소를 받아 build.mjs 를 돌린다.
set -euo pipefail

SLUG="${1:?slug 인자가 필요하다}"
REPO="https://github.com/kajam0623-rgb/dongseong.git"
BRANCH="claude/ilsan-anitok-project-arpdi5"

rm -rf .src public
git clone --depth 1 --branch "$BRANCH" "$REPO" .src

( cd .src/anitok-campuses && node build.mjs "$SLUG" )

SRC=".src/anitok-campuses/sites/$SLUG"
test -f "$SRC/index.html"

cp -r "$SRC" public
# 배포 루트의 vercel.json 이 이미 적용되므로 사본은 지운다. 문서 파일도 공개하지 않는다.
rm -f public/vercel.json public/PHOTOS.md public/README.md

echo "---- 배포될 파일 ----"
find public -type f | sort
