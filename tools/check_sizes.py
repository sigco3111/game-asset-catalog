#!/usr/bin/env python3
"""에셋 저장소 5곳의 용량을 GitHub API로 읽어 docs/capacity-report.md를 만든다 (표준 라이브러리만 사용).

사용법: python3 tools/check_sizes.py
환경 변수 GITHUB_TOKEN이 있으면 인증 헤더로만 쓰고(요청 한도 완화), 파일에는 기록하지 않는다.
API 호출이 실패한 저장소는 '확인 실패'로 적고 종료 코드 0으로 끝낸다.
"""
import json, os, urllib.request
from datetime import datetime, timedelta, timezone

OWNER = "sigco3111"
REPOS = ["assets-2d-pixel", "assets-audio", "assets-3d-lowpoly", "assets-3d-lowpoly-2", "assets-ui-icons", "assets-2d-portraits"]
LIMIT_MB = 900
# (기준 MB 이상, 상태) — 큰 값부터
THRESHOLDS = [(900, "추가 중단"), (850, "분리 준비"), (700, "주의")]
OK = "양호"
FAIL = "확인 실패"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "capacity-report.md")


def fetch_kb(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{repo}", headers={"Accept": "application/vnd.github+json", "User-Agent": "capacity-check"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return int(json.load(r)["size"])
    except Exception as e:
        print(f"{repo}: {e}")
        return None


def status(mb):
    for limit, name in THRESHOLDS:
        if mb >= limit:
            return name
    return OK


def main():
    now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
    rows, ok_mb = [], []
    for repo in REPOS:
        kb = fetch_kb(repo)
        if kb is None:
            rows.append(f"| {repo} | {FAIL} | {FAIL} | {FAIL} |")
            continue
        mb = kb / 1024
        ok_mb.append(mb)
        rows.append(f"| {repo} | {mb:,.1f} | {status(mb)} | {max(0.0, LIMIT_MB - mb):,.1f} |")
    L = [
        "# 저장소 용량 점검 보고서",
        "",
        f"생성: {now} (`python3 tools/check_sizes.py`, 매주 월요일 자동 갱신)",
        "",
        "| 저장소 | 용량(MB) | 상태 | 900MB까지 남은 용량(MB) |",
        "| --- | ---: | --- | ---: |",
        *rows,
        "",
    ]
    if len(ok_mb) == len(REPOS):
        L += [f"5개 저장소 합계: {sum(ok_mb):,.1f}MB (저장소별로 판단하며 합계는 참고용입니다).", ""]
    L += [
        "## 판정 규칙",
        "",
        "- 양호: 700MB 미만",
        "- 주의: 700MB 이상",
        "- 분리 준비: 850MB 이상 (다음 저장소 `assets-<종류>-2` 준비)",
        "- 추가 중단: 900MB 이상 (그 저장소에는 새 팩을 올리지 않음)",
        "",
        "용량은 GitHub API의 `size`(KB)를 1024로 나눈 값입니다. 릴리스 첨부 파일은 포함되지 않습니다. 자세한 정책은 [capacity.md](capacity.md)를 참고하세요.",
        "",
    ]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    print("\n".join(rows))


if __name__ == "__main__":
    main()
