#!/usr/bin/env bash
set -e
python3 - <<'PY'
import csv, io
rows = [
 ['low_poly_swords','assets-3d-lowpoly-2','swords_obj.zip','3D 모델','sword,weapon,lowpoly,obj','Q2DENJINDREW','https://opengameart.org/content/lowpolyswords','CC0','optional: none','2026-11-14','OBJ 로우폴리 검 모음; zip 원본 그대로','','',''],
 ['3D Character Pack','assets-3d-lowpoly-2','bravos_game_br_2024.zip','3D 캐릭터','character,humanoid,lowpoly,3d','byzmod3d','https://opengameart.org/content/3d-character-pack','CC0','optional: none','2026-11-14','zip 원본 그대로','','',''],
 ['3D Human Parts Pack','assets-3d-lowpoly-2','3d_human_parts_pack.zip','3D 모델','human,body,parts,lowpoly,3d','byzmod3d','https://opengameart.org/content/3d-human-parts-pack','CC0','optional: none','2026-11-14','zip 원본 그대로','','',''],
]
txt = open('catalog.csv', encoding='utf-8').read()
for r in rows:
    if r[6] in txt:
        continue
    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerow(r)
    if not txt.endswith('\n'):
        txt += '\n'
    txt += buf.getvalue()
open('catalog.csv', 'w', encoding='utf-8').write(txt)
rd = open('README.md', encoding='utf-8').read()
rd = rd.replace('1,872', '1,875').replace('1872팩', '1875팩')
sec = '\n## A89 (2026-11-14)\n- low_poly_swords (Q2DENJINDREW, CC0) - assets-3d-lowpoly-2\n- 3D Character Pack (byzmod3d, CC0) - assets-3d-lowpoly-2\n- 3D Human Parts Pack (byzmod3d, CC0) - assets-3d-lowpoly-2\n- 3팩 추가, 총 1,875팩 (3D 3)\n'
if 'A89 (2026-11-14)' not in rd:
    rd += sec
open('README.md', 'w', encoding='utf-8').write(rd)
log = '- 2026-11-14 A89: low_poly_swords (Q2DENJINDREW, CC0), 3D Character Pack (byzmod3d, CC0), 3D Human Parts Pack (byzmod3d, CC0) (3팩, 총 1875팩; 3D 3, assets-3d-lowpoly-2). OGA 최신 3D 목록과 코드 검색으로 중복 확인 후 수집, 팩마다 커밋.\n'
if 'A89:' not in open('docs/log.md', encoding='utf-8').read():
    open('docs/log.md', 'a', encoding='utf-8').write(log)
print('done')
PY
