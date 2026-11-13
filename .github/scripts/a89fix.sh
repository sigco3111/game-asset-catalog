#!/usr/bin/env bash
set -e
python3 - <<'PY'
import re
t = open('README.md', encoding='utf-8').read()
# 내가 뒤에 붙인 A89 블록 제거
lines = t.split('\n')
out = []
skip = False
for ln in lines:
    if ln.startswith('## A89 (2026-11-14)'):
        skip = True
        continue
    if skip:
        if ln.startswith('## '):
            skip = False
        else:
            continue
    out.append(ln)
t = '\n'.join(out)
sec = '## 2026-11-14 A89 추가 (3팩, 총 1878팩)\n\nA89 라운드에서 OpenGameArt의 3D 3팩 low_poly_swords(Q2DENJINDREW, CC0), 3D Character Pack(byzmod3d, CC0), 3D Human Parts Pack(byzmod3d, CC0)을 수집했습니다. 중복은 저장소 코드 검색으로 확인했습니다(세 팩 모두 0건).\n\n'
if 'A89 추가' not in t:
    i = t.find('## 2026-11-14 A88')
    t = t[:i] + sec + t[i:] if i >= 0 else t + '\n' + sec
open('README.md', 'w', encoding='utf-8').write(t)
print('ok')
PY
