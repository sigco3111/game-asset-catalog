# 용량 관리 정책

## 목적

에셋 저장소(`assets-2d-pixel`, `assets-audio`, `assets-3d-lowpoly`, `assets-ui-icons`, `assets-2d-portraits`)가 GitHub 권장 크기(저장소당 약 1GB)를 넘지 않도록 미리 점검하고, 커지기 전에 어떻게 나눌지 정해 둡니다. 이 카탈로그 저장소는 5개 저장소의 색인이며 용량 문제가 없습니다.

## 현재 현황

2026-11-11 18:22 KST 기준(GitHub API `size`): `assets-2d-pixel` 약 328MB, `assets-audio` 약 369MB, `assets-3d-lowpoly` 약 528MB, `assets-ui-icons` 약 56MB, `assets-2d-portraits` 약 51MB로 5개 합계 약 1.3GB이며, 저장소 하나도 700MB에 이르지 않아 모두 양호입니다. 최신 수치는 docs/capacity-report.md 참조.

## 기준

| 용량 | 상태 | 뜻 |
| --- | --- | --- |
| 700MB 미만 | 양호 | 평소대로 수집 |
| 700MB 이상 | 주의 | 소유자에게 알리고 큰 팩을 릴리스로 올리는 쪽을 우선 |
| 850MB 이상 | 분리 준비 | 다음 저장소를 만들고 새 팩은 그쪽으로 |
| 900MB 이상 | 추가 중단 | 그 저장소에는 새 팩을 올리지 않음 |

기준은 저장소 하나씩 따로 적용합니다. 용량은 GitHub API의 `size`(KB)를 1024로 나눈 MB이며 릴리스 첨부 파일은 포함되지 않습니다.

## 규칙

1. **큰 zip은 릴리스로**: 5MB를 넘는 zip 파일은 저장소 트리 대신 GitHub Releases에 올립니다. 카탈로그에는 이미 `releases/download/...` 경로를 쓰는 항목이 있으며, 같은 방식으로 `catalog.csv`의 `file`/`preview` 열에 적습니다. 릴리스 첨부는 저장소 용량에 들어가지 않습니다.
2. **저장소 분리**: 저장소가 분리 준비(850MB 이상)가 되면 다음 저장소를 `assets-<종류>-2`(예: `assets-audio-2`)라는 이름의 공개 저장소로 만들고, README 형식은 기존 에셋 저장소와 같게 합니다. 새 팩은 그 저장소에 올리고, `catalog.csv`의 `repo` 열에 실제 저장소 이름을 적어서 색인과 도서관 사이트가 그대로 동작하게 합니다. 용량 점검 대상 목록(`tools/check_sizes.py`의 `REPOS`)에도 새 저장소를 추가합니다.
3. **기록 보존**: 소유자의 명시적인 결정 없이는 용량을 줄이려고 히스토리를 다시 쓰거나(force push, 기록 정리) 팩을 지우지 않습니다.
4. **파일 한도**: 파일 하나 25MB, 커밋 하나 40MB 이하(지금까지 쓰던 한도 그대로). 넘으면 분할하거나 릴리스로 올립니다.

## 점검 방법

- 직접 실행: 저장소 루트에서 `python3 tools/check_sizes.py` (표준 라이브러리만 사용, `GITHUB_TOKEN` 환경 변수가 있으면 인증에 사용). 결과는 `docs/capacity-report.md`에 쓰입니다.
- 자동 실행: GitHub Actions의 `용량 점검`(`.github/workflows/capacity-check.yml`)이 매주 월요일 00:00 UTC(한국 09:00)에 실행되어 변경이 있으면 `운영: 용량 점검 갱신`으로 커밋합니다. Actions 탭에서 수동 실행도 가능합니다.
- 주간 보고서: [capacity-report.md](capacity-report.md)

## 상태별 조치

보고서에서 상태를 확인했을 때 수집 에이전트가 해당 저장소와 용량을 라운드 보고에 적어 소유자에게 알립니다.

- **주의**: 보고에 적고, 큰 zip은 릴리스로 올립니다(규칙 1).
- **분리 준비**: 보고에 적고, 소유자 확인 뒤 `assets-<종류>-2` 저장소를 만들어 새 팩을 그쪽에 올립니다(규칙 2).
- **추가 중단**: 그 저장소에는 팩을 더 올리지 않고 보고합니다. 새 팩은 `-2` 저장소로 가며, 기존 팩 삭제나 기록 정리는 소유자가 정합니다(규칙 3).

## 2026-11-14 A87 저장소 추가

assets-3d-lowpoly가 약 692MB로 700MB에 근접해, 2026-11-14 A87 라운드에서 3D 2호 저장소 assets-3d-lowpoly-2(공개, 기존 저장소와 같은 README 구성, 릴리스 태그 사용)를 만들었습니다. A87 이후 3D 팩은 assets-3d-lowpoly-2에 올리고 catalog.csv의 repo 열에 그 이름을 적습니다. 기존 저장소의 파일은 삭제·이동하지 않습니다. tools/check_sizes.py의 점검 대상에 새 저장소를 추가했습니다.
