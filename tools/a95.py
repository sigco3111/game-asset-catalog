import os, csv, io, json, zipfile, hashlib, subprocess, urllib.request, shutil

MODE = os.environ.get('MODE', 'probe')
DATE = '2026-11-14'
AGA = 'https://github.com/AgenticGameDevs/generated-assets'
AGAB = 'https://raw.githubusercontent.com/AgenticGameDevs/generated-assets/main/'
CATCSV = 'https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/catalog.csv'
RAWB = 'https://raw.githubusercontent.com/sigco3111/%s/main/'
LIC = 'CC BY 4.0'

PACKS = [
 {'slug': 'fjordfall-boats-and-vehicles', 'name': 'Fjordfall Boats & Vehicles', 'collection': 'fjordfall', 'category': 'Boats & vehicles', 'repo': 'assets-3d-lowpoly-2', 'type': '3D', 'tags': '3d,lowpoly,vehicles,boats,fjordfall,ai-generated', 'mode': '3d'},
 {'slug': 'fjordfall-buildings', 'name': 'Fjordfall Buildings', 'collection': 'fjordfall', 'category': 'Buildings', 'repo': 'assets-3d-lowpoly-2', 'type': '3D', 'tags': '3d,lowpoly,buildings,fjordfall,ai-generated', 'mode': '3d'},
 {'slug': 'fjordfall-characters', 'name': 'Fjordfall Characters', 'collection': 'fjordfall', 'category': 'Characters', 'repo': 'assets-3d-lowpoly-2', 'type': '3D', 'tags': '3d,lowpoly,characters,fjordfall,ai-generated', 'mode': '3d'},
 {'slug': 'skybound-synthesized-sfx', 'name': 'Skybound Six Synthesized SFX', 'collection': 'skybound', 'category': 'Sound effects', 'repo': 'assets-audio', 'type': 'sfx', 'tags': 'sfx,effect,impact,explosion,laser,ai-generated', 'mode': 'audio'}
]

def gb(url):
    with urllib.request.urlopen(url, timeout=300) as r:
        return r.read()

def gt(url):
    return gb(url).decode('utf-8')

def sh(*a, **kw):
    return subprocess.run(list(a), check=True, **kw)

def commit(msg):
    sh('git', 'config', 'user.name', 'sigco3111')
    sh('git', 'config', 'user.email', 'sigco3111@users.noreply.github.com')
    sh('git', 'add', '-A')
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode == 0:
        print('no changes:', msg)
        return
    sh('git', 'commit', '-m', msg)
    sh('git', 'push')

def existing():
    rows = list(csv.reader(io.StringIO(gt(CATCSV))))
    names, urls = set(), set()
    for r in rows[1:]:
        if r:
            names.add((r[0] or '').strip().lower())
            urls.add((r[6] or '').strip().lower().rstrip('/'))
    return names, urls

def mb(n):
    return '%.1fMB' % (n / 1048576.0)

def build_pack(p):
    names, urls = existing()
    if p['name'].strip().lower() in names:
        print('SKIP duplicate name', p['name'])
        return False
    cat = json.loads(gt(AGAB + 'catalog.json'))
    assets = [a for a in cat if a['collection'] == p['collection'] and a['category'] == p['category']]
    if not assets:
        raise SystemExit('no assets for ' + p['name'])
    slug = p['slug']
    shutil.rmtree(slug, ignore_errors=True)
    os.makedirs(slug)
    tmp = '/tmp/a95files'
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    files = []
    for a in assets:
        b = gb(AGAB + a['file'])
        h = hashlib.sha256(b).hexdigest()
        if a.get('sha256') and h != a['sha256']:
            raise SystemExit('checksum mismatch ' + a['id'])
        nm = os.path.basename(a['file'])
        open(os.path.join(tmp, nm), 'wb').write(b)
        files.append((a, nm, len(b)))
    total = sum(f[2] for f in files)
    creators = sorted({(a.get('creator') or {}).get('name', '') for a, _, _ in files} - {''})
    gens = sorted({(a.get('source') or {}).get('generator', '') for a, _, _ in files} - {''})
    sub = 'models/' if p['mode'] == '3d' else 'sfx/'
    zipname = slug + '.zip'
    zpath = os.path.join(slug, zipname)
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for a, nm, sz in files:
            z.write(os.path.join(tmp, nm), sub + nm)
    zsize = os.path.getsize(zpath)
    L = []
    L.append('# ' + p['name'])
    L.append('')
    L.append('- 출처: ' + AGA + ' (' + p['collection'] + ' / ' + p['category'] + ')')
    L.append('- 원본 컬렉션: ' + p['collection'] + ' (AI 생성·AI 보조 에셋 라이브러리)')
    L.append('- 라이선스: ' + LIC + ' (https://creativecommons.org/licenses/by/4.0/)')
    L.append('- 제작자: ' + ', '.join(creators))
    L.append('- 구성: ' + str(len(files)) + '개 파일, ' + mb(total))
    L.append('- 파일: ' + zipname + ' (' + mb(zsize) + ') — ' + ('저장소 내 포함' if zsize <= 5 * 1048576 else '릴리스 첨부'))
    L.append('- AI 생성: 예 — 출처 저장소가 AI 생성·AI 보조 작업물임을 명시')
    L.append('- 생성 도구: ' + ', '.join(gens))
    L.append('- 출처가 밝힌 조건: 저작자 표기, 라이선스 링크, 변경 여부 명시 필수. 수집 시 원본 파일 바이트 그대로 보관하고(zip 재압축만) 파일 내용은 바꾸지 않음')
    L.append('- 수집일: ' + DATE)
    L.append('- 태그: ' + p['tags'])
    L.append('')
    L.append('## 구성 파일')
    L.append('')
    L.append('| 에셋 | 파일 | 생성 도구 | 바이트 |')
    L.append('| --- | --- | --- | --- |')
    for a, nm, sz in files:
        L.append('| ' + a['name'].replace('|', '/') + ' | ' + nm + ' | ' + ((a.get('source') or {}).get('generator', '') or '') + ' | ' + str(sz) + ' |')
    L.append('')
    L.append('## 에셋별 표기')
    L.append('')
    for a, nm, sz in files:
        L.append('- ' + a['name'] + ': ' + (a.get('attribution') or ''))
    open(os.path.join(slug, 'pack.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    S = []
    S.append(p['name'])
    S.append('')
    S.append('출처 URL: ' + AGA)
    S.append('원본 경로: assets/' + p['collection'] + '/' + p['category'].lower().replace(' & ', '-') + '/')
    S.append('표기 라이선스: ' + LIC)
    S.append('라이선스 원문: https://creativecommons.org/licenses/by/4.0/')
    S.append('제작자: ' + ', '.join(creators))
    S.append('AI 생성: 예 (생성 도구: ' + ', '.join(gens) + ')')
    S.append('')
    S.append('이 파일은 수집자가 출처의 라이선스 표기를 기록한 것입니다.')
    S.append('원본 배포물에 라이선스 파일이 포함되어 있지 않기 때문에 이 파일이 그 역할을 합니다.')
    S.append('재배포·사용 시 저작자 표기, 라이선스 링크, 변경 여부를 함께 밝혀 주세요.')
    open(os.path.join(slug, 'LICENSE-SOURCE.txt'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    C = [p['name'], '']
    C.append('CC BY 4.0 - 사용 시 아래 표기를 남겨 주세요.')
    C.append('')
    for a, nm, sz in files:
        C.append(a['name'])
        C.append('  ' + (a.get('attribution') or ''))
        C.append('')
    open(os.path.join(slug, 'CREDITS.txt'), 'w', encoding='utf-8').write('\n'.join(C) + '\n')
    commit('에셋: ' + p['name'] + ' 추가')
    cand = [a for a in assets if a.get('preview')]
    if cand and p['mode'] == '3d':
        a = cand[0]
        src = '/tmp/a95prev.png'
        open(src, 'wb').write(gb(AGAB + a['preview']))
        out = os.path.join(slug, 'preview.jpg')
        for q, w in ((82, 480), (72, 440), (65, 400), (60, 360)):
            sh('convert', src, '-resize', '%dx%d>' % (w, w), '-background', 'white', '-alpha', 'remove', '-alpha', 'off', '-strip', '-quality', str(q), out)
            if os.path.getsize(out) <= 200 * 1024:
                break
        os.makedirs('previews', exist_ok=True)
        shutil.copy(out, os.path.join('previews', slug + '.jpg'))
        commit('썸네일: ' + p['name'] + ' 추가')
    return True

def run_build(mode):
    done = []
    for p in PACKS:
        if p['mode'] != mode:
            continue
        if build_pack(p):
            done.append(p['name'])
    print('ADDED:', done)
    return done

def catalog():
    rows = list(csv.reader(io.StringIO(gt(CATCSV))))
    hdr, data = rows[0], [r for r in rows[1:] if r]
    names = {(r[0] or '').strip().lower() for r in data}
    urls = {(r[6] or '').strip().lower().rstrip('/') for r in data}
    from collections import Counter
    atypes = Counter(r[3] for r in data if r[1] == 'assets-audio')
    atype = atypes.most_common(1)[0][0] if atypes else 'sfx'
    new = []
    for p in PACKS:
        if p['name'].strip().lower() in names or AGA.lower() in urls:
            print('DUP skip', p['name'])
            continue
        b = gb(RAWB % p['repo'] + p['slug'] + '/' + p['slug'] + '.zip')
        zs = len(b)
        md = gt(RAWB % p['repo'] + p['slug'] + '/pack.md')
        gen = ''
        for ln in md.split('\n'):
            if ln.startswith('- 생성 도구:'):
                gen = ln.split(':', 1)[1].strip()
            if ln.startswith('- 제작자:'):
                cre = ln.split(':', 1)[1].strip()
        typ = p['type'] if p['mode'] == '3d' else atype
        if p['mode'] == '3d':
            prev = RAWB % p['repo'] + 'previews/' + p['slug'] + '.jpg'
            notes = '3D 팩; AI 생성(AgenticGameDevs/generated-assets; 생성 도구 ' + gen + '); 라이선스 CC BY 4.0 표기 파일(pack.md·CREDITS.txt·LICENSE-SOURCE.txt) 포함; 썸네일 480px 이하 JPEG; ' + ('저장소 내 포함' if zs <= 5 * 1048576 else '릴리스 첨부')
        else:
            prev = ''
            notes = '효과음 팩; AI 생성(AgenticGameDevs/generated-assets; 생성 도구 ' + gen + '); 라이선스 CC BY 4.0 표기 파일 포함; ' + ('저장소 내 포함' if zs <= 5 * 1048576 else '릴리스 첨부')
        new.append([p['name'], p['repo'], p['slug'] + '/' + p['slug'] + '.zip', typ, p['tags'], cre, AGA, 'CC-BY', 'required: ' + cre + ' (CC BY 4.0)', DATE, notes, prev, '', ''])
    if not new:
        print('nothing to add')
        return
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(hdr)
    for r in data:
        w.writerow(r)
    for r in new:
        w.writerow(r)
    open('catalog.csv', 'w', encoding='utf-8').write(buf.getvalue())
    total = len(data) + len(new)
    n3 = sum(1 for r in new if r[1] == 'assets-3d-lowpoly-2')
    nfx = sum(1 for r in new if r[1] == 'assets-audio')
    rl = open('README.md', encoding='utf-8').read()
    sec = []
    sec.append('## 2026-11-14 A95 추가 (' + str(len(new)) + '팩, 총 ' + str(total) + '팩)')
    sec.append('')
    sec.append('A95 라운드: GitHub의 AgenticGameDevs/generated-assets(AI 생성 에셋 라이브러리; 미디어 CC BY 4.0·CC0, 코드 MIT)에서 Fjordfall 컬렉션의 3D 모델과 Skybound 효과음을 팩 단위로 모았습니다. 후보는 러너 안에서 전체 catalog.csv(csv.reader, name+source URL)와 대조해 걸러냈고, 팩마다 원본 파일 바이트와 sha256을 확인했습니다.')
    sec.append('')
    sec.append('| 팩 | 라이선스 |')
    sec.append('| --- | --- |')
    for r in new:
        sec.append('| ' + r[0] + ' | CC BY 4.0 |')
    sec.append('')
    th = []
    for r in new:
        th.append(r[0] + '=' + ('있음' if r[11] else '해당 없음(오디오)'))
    sec.append('종류: 3D ' + str(n3) + '팩, 효과음 ' + str(nfx) + '팩. AI 생성 표기는 각 팩 pack.md에 있고, 생성 도구와 출처 조건도 함께 적었습니다. 썸네일: ' + ', '.join(th) + '. 색인은 rebuild-index.yml 수동 실행으로 갱신합니다.')
    sec.append('')
    marker = '## 2026-11-14 A94 추가'
    if marker in rl:
        rl = rl.replace(marker, '\n'.join(sec) + '\n' + marker, 1)
    else:
        rl = rl + '\n' + '\n'.join(sec)
    open('README.md', 'w', encoding='utf-8').write(rl)
    logline = '- ' + DATE + ' A95: ' + ', '.join(r[0] for r in new) + ' (' + str(len(new)) + '팩, 총 ' + str(total) + '팩; 3D ' + str(n3) + '팩은 assets-3d-lowpoly-2, 효과음 ' + str(nfx) + '팩은 assets-audio; 출처 AgenticGameDevs/generated-assets, AI 생성 표기·생성 도구·CC BY 4.0 조건 기록; 이름·출처 URL 전체 catalog.csv 대조로 중복 제거).'
    lg = open('docs/log.md', encoding='utf-8').read()
    open('docs/log.md', 'w', encoding='utf-8').write(lg.rstrip('\n') + '\n\n' + logline + '\n')
    commit('카탈로그: A95 ' + str(len(new)) + '팩 추가')
    print('CATALOG ADDED', len(new), 'TOTAL', total)

def cleanup94():
    for f in ['.github/workflows/a94-go.yml', '.github/workflows/a94b-go.yml', 'a94-res.txt']:
        if os.path.exists(f):
            sh('git', 'rm', '-q', f)
    d = 'mico-font-2d-handwritten-display-font'
    if os.path.isdir(d):
        sh('git', 'rm', '-r', '-q', d)
    commit('A94: 임시 파일 삭제')
    print('cleanup94 done')

def cleanup():
    for f in ['tools/a95.py', 'a95-res.txt', '.github/workflows/a95-cat.yml']:
        if os.path.exists(f):
            sh('git', 'rm', '-q', f)
    commit('정리: A95 임시 파일 삭제')
    print('cleanup done')

if MODE == 'build3d':
    run_build('3d')
elif MODE == 'buildaudio':
    run_build('audio')
elif MODE == 'catalog':
    catalog()
elif MODE == 'cleanup94':
    cleanup94()
elif MODE == 'cleanup':
    cleanup()
else:
    print('unknown mode', MODE)
