> 이 문서는 tools/build_wiki.py가 assets-index.json에서 자동 생성합니다. 직접 고치지 마세요.

> generated from `catalog.csv@2a08dffa16d98707cdcf284dff795ef89350e26a`

# 게임 에셋 카탈로그 위키

게임 에셋 카탈로그(sigco3111/game-asset-catalog)의 **주제별 모음 위키**입니다. 사람과 AI 에이전트가 에셋을 빨리 찾고, 라이선스와 표기 의무를 확인하고, 쓴 기록을 남기도록 돕습니다.

## 이 위키는 어떻게 만들어지나

- `catalog.csv` → `python3 tools/build_index.py` → `assets-index.json` → `python3 tools/build_wiki.py` → `docs/wiki/*.md`, `llms.txt`.
- 이 위키의 자동 생성 문서는 직접 고치지 않습니다. 에셋이 바뀌면 두 스크립트를 다시 실행합니다(표준 라이브러리만 사용, 같은 입력이면 같은 출력).
- 에셋마다 쪽을 따로 만들지 않습니다. 표의 이름을 누르면 제작자의 출처 페이지로 갑니다.
- 손으로 쓰는 문서는 [사용 장부](usage-ledger.md) 하나뿐이며 생성기가 덮어쓰지 않습니다.
- 현재 색인: 에셋 **1887개** (`catalog.csv@2a08dffa16d98707cdcf284dff795ef89350e26a`).

## 링크

- 에셋 도서관(검색 사이트): https://sigco3111.github.io/game-asset-catalog/
- 색인: [assets-index.json](../../assets-index.json), [assets-index.min.json](../../assets-index.min.json) · 원본 표: [catalog.csv](../../catalog.csv) · 점검 보고서: [index-report.md](../index-report.md)
- 에이전트용 안내: [llms.txt](../../llms.txt)
- [라이선스 모음](licenses.md) · [최근 추가 100개](recent.md) · [사용 장부](usage-ledger.md)

## 라이선스 규칙

- 허용 라이선스: **CC0, CC-BY, MIT, GPL 2.0/3.0**만 수록합니다. 그 밖의 라이선스는 쓰기 전에 직접 확인합니다(자세한 목록은 [licenses.md](licenses.md)).
- 라이선스를 재해석하지 않습니다. 색인의 `license`, `license_note`, `attribution` 값을 그대로 따릅니다.
- GPL 에셋은 원본 GPL 조건(라이선스 고지, 소스 공개 등)을 유지합니다.

## 표기(attribution) 규칙

- 색인의 `attribution_required`가 참이면(153개: CC-BY·MIT·GPL) 에셋을 쓰는 프로젝트의 `CREDITS.md`에 제작자·출처·라이선스를 적습니다. 문구 예시는 색인의 `attribution` 값입니다.
- CC0는 표기가 필수가 아니며, 색인에는 선택 표기 문구만 있습니다.
- 쓴 에셋은 [사용 장부](usage-ledger.md)에도 한 줄 기록합니다.

## AI 생성 표시

- 색인의 `ai_generated`가 참인 에셋(22개)은 표에서 'AI 생성'이 **O**로 표시됩니다. 라이브러리에서는 `?ai=0`으로 제외할 수 있습니다.

## 분류별 개수

| 분류 | 이름 | 개수 | 목록 |
|---|---|---|---|
| `effect` | 이펙트 | 139 | [category-effect.md](category-effect.md) |
| `sfx` | 효과음 | 235 | [category-sfx.md](category-sfx.md) |
| `music` | 음악 | 230 | [category-music.md](category-music.md) |
| `voice` | 음성 | 2 | [category-voice.md](category-voice.md) |
| `tileset-2d` | 2D 타일셋 | 146 | [category-tileset-2d.md](category-tileset-2d.md) |
| `sprite-2d` | 2D 스프라이트 | 132 | [category-sprite-2d.md](category-sprite-2d.md) |
| `background-2d` | 2D 배경 | 27 | [category-background-2d.md](category-background-2d.md) |
| `map-2d` | 2D 맵 | 3 | [category-map-2d.md](category-map-2d.md) |
| `ui` | UI | 205 | [category-ui.md](category-ui.md) |
| `icon` | 아이콘 | 40 | [category-icon.md](category-icon.md) |
| `portrait` | 초상화 | 2 | [category-portrait.md](category-portrait.md) |
| `font` | 폰트 | 2 | [category-font.md](category-font.md) |
| `texture` | 텍스처 | 70 | [category-texture.md](category-texture.md) |
| `model-3d` | 3D 모델 | 453 | [category-model-3d.md](category-model-3d.md) |
| `character-3d` | 3D 캐릭터 | 32 | [category-character-3d.md](category-character-3d.md) |
| `vehicle-3d` | 3D 탈것 | 10 | [category-vehicle-3d.md](category-vehicle-3d.md) |
| `building-3d` | 3D 건물 | 23 | [category-building-3d.md](category-building-3d.md) |
| `board` | 보드게임 | 5 | [category-board.md](category-board.md) |
| `puzzle` | 퍼즐 | 2 | [category-puzzle.md](category-puzzle.md) |
| `other` | 기타 | 129 | [category-other.md](category-other.md) |

합계 1887개. 분류가 400행을 넘는 목록은 `-2` 쪽으로 이어집니다.

## 효과 종류별 개수

한 에셋이 여러 효과 종류를 가질 수 있어 합계가 에셋 수와 다를 수 있습니다.

| 효과 종류 | 이름 | 개수 | 목록 |
|---|---|---|---|
| `hit` | 타격 | 44 | [effects-hit.md](effects-hit.md) |
| `impact` | 충격 | 46 | [effects-impact.md](effects-impact.md) |
| `magic` | 마법 | 93 | [effects-magic.md](effects-magic.md) |
| `explosion` | 폭발 | 65 | [effects-explosion.md](effects-explosion.md) |
| `fire` | 불 | 53 | [effects-fire.md](effects-fire.md) |
| `ice` | 얼음 | 21 | [effects-ice.md](effects-ice.md) |
| `lightning` | 번개 | 26 | [effects-lightning.md](effects-lightning.md) |
| `wind` | 바람 | 9 | [effects-wind.md](effects-wind.md) |
| `heal` | 치유 | 16 | [effects-heal.md](effects-heal.md) |
| `laser` | 레이저 | 13 | [effects-laser.md](effects-laser.md) |
| `particle` | 입자 | 30 | [effects-particle.md](effects-particle.md) |
| `smoke` | 연기 | 12 | [effects-smoke.md](effects-smoke.md) |
| `aura` | 오라 | 7 | [effects-aura.md](effects-aura.md) |
| `projectile` | 투사체 | 27 | [effects-projectile.md](effects-projectile.md) |
| `slash` | 베기 | 9 | [effects-slash.md](effects-slash.md) |
