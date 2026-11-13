#!/usr/bin/env bash
set -e
python3 - <<'PY'
import csv, io, re

# 1) catalog.csv 한 줄 추가
row = ['Low Poly Stalls','assets-3d-lowpoly-2','lightdreamerlabs-3d-stalls.zip','3D 소품',
       'stall,shop,food,prop','lightdreamerlabs','https://opengameart.org/content/low-poly-stalls',
       'CC0','','2026-11-14','zip 1개 703.1KB(출처 페이지 zip 그대로); A88 라운드 수집; AI 생성 언급 없음']
with open('catalog.csv','a',newline='',encoding='utf-8') as f:
    csv.writer(f).writerow(row)

# 2) README
r = open('README.md',encoding='utf-8').read()
anchor = '## 2026-11-14 A87 추가'
sec = '''## 2026-11-14 A88 추가 (1팩, 총 1872팩)

A88 라운드에서 OpenGameArt의 3D 1팩 Low Poly Stalls(lightdreamerlabs, CC0)를 수집했습니다. 중복은 카탈로그 저장소 코드 검색으로 확인했습니다(Low Poly Stalls 0건). 이번 라운드는 시간 제한으로 1팩만 수집했습니다.

| 팩 | 라이선스 |
| --- | --- |
| Low Poly Stalls | CC0 |

종류: 3D 1팩(assets-3d-lowpoly-2). 라이선스: CC0 1팩. AI 생성 명시 팩 없음. 팩당 1커밋(에셋: Low Poly Stalls 추가, 임시 워크플로 a88-ingest.yml). 용량: zip 703.1KB로 저장소 트리에 직접 포함. 색인은 rebuild-index.yml 수동 실행으로 갱신.

'''
if anchor in r and 'A88 추가' not in r:
    i = r.index(anchor)
    r = r[:i] + sec + r[i:]
# 3) 저장소 표에 assets-3d-lowpoly-2 행 추가
old = '| [assets-3d-lowpoly](https://github.com/sigco3111/assets-3d-lowpoly) | 3D 로우폴리 모델 (GLB·OBJ) | 2팩 (릴리스 첨부) |'
new = old + '\n| [assets-3d-lowpoly-2](https://github.com/sigco3111/assets-3d-lowpoly-2) | 3D 로우폴리 모델 2호 (700MB 분할 대응) | 2팩 |'
if 'assets-3d-lowpoly-2)' not in r and old in r:
    r = r.replace(old, new)
# 4) A86 총계 정정
r = r.replace('## 2026-11-14 A86 추가 (4팩, 총 1871팩)','## 2026-11-14 A86 추가 (4팩, 총 1868팩)')
open('README.md','w',encoding='utf-8').write(r)

# 5) docs/log.md
with open('docs/log.md','a',encoding='utf-8') as f:
    f.write('\n- 2026-11-14 A88: Low Poly Stalls(3D, CC0, assets-3d-lowpoly-2) 추가. 카탈로그 1872팩. README에 A88 절·assets-3d-lowpoly-2 행 추가, A86 총계 1868로 정정.\n')
print('ok')
PY
