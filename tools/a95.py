import csv, json, subprocess, urllib.request
from collections import Counter, defaultdict

def get(url):
    with urllib.request.urlopen(url, timeout=180) as r:
        return r.read().decode('utf-8')

out=[]
def p(s=''): out.append(str(s))

rows=list(csv.reader(open('catalog.csv', encoding='utf-8')))
hdr=rows[0]; rows=rows[1:]
p('TOTAL %d' % len(rows))
p('HDR ' + ','.join(hdr))
for r in rows[-6:]:
    p('ROW ' + json.dumps(r, ensure_ascii=False))
p('REPOS ' + json.dumps(Counter(r[1] for r in rows), ensure_ascii=False))

readme=open('README.md', encoding='utf-8').read().split('\n')
for i,l in enumerate(readme):
    if 'A94' in l:
        p('README A94 L%d' % i)
        for x in readme[max(0,i-5):i+10]:
            p('  ' + x)
p('README LINES %d' % len(readme))
for l in readme[:40]:
    if '팩' in l and ('개' in l or ',' in l):
        p('HEAD ' + l)

log=open('docs/log.md', encoding='utf-8').read().split('\n')
p('LOG TAIL')
for x in log[-25:]:
    p('  ' + x)

cat=json.loads(get('https://raw.githubusercontent.com/AgenticGameDevs/generated-assets/main/catalog.json'))
p('AGA TOTAL %d' % len(cat))
g=defaultdict(list)
for a in cat:
    g[(a.get('collection'), a.get('category'), a.get('kind'), a.get('license'))].append(a)
for k in sorted(g, key=lambda k: (str(k[0]), str(k[1]))):
    v=g[k]
    p('AGA %s | n=%d | bytes=%d' % ('|'.join(str(x) for x in k), len(v), sum((x.get('bytes') or 0) for x in v)))

open('a95-res.txt','w',encoding='utf-8').write('\n'.join(out))
subprocess.run(['git','config','user.name','sigco3111'])
subprocess.run(['git','config','user.email','sigco3111@users.noreply.github.com'])
subprocess.run(['git','add','a95-res.txt'])
subprocess.run(['git','commit','-m','A95: 조사 결과'])
subprocess.run(['git','push'])
print('\n'.join(out))
