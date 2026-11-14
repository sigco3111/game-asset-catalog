import csv, subprocess

CAND = [
    dict(name="Chibi Neko by cosmix", repo="assets-3d-lowpoly-2", file="chibi-neko/chibineko.zip", type="3D 캐릭터",
         tags="character,cat,chibi,lowpoly", author="zodiepupper",
         source_url="https://opengameart.org/content/chibi-neko-by-cosmix", license="CC0",
         attribution="optional: zodiepupper", added="2026-11-14",
         notes="zip 원본 포함; OGA 라이선스 CC0; 파일 무변경; 썸네일 previews/chibi-neko.png",
         preview="previews/chibi-neko.png"),
    dict(name="Bald Man - Rigged", repo="assets-3d-lowpoly-2", file="bald-man-rigged/baldman_painted_rigged.zip", type="3D 캐릭터",
         tags="character,human,rigged,lowpoly", author="EmoPreben",
         source_url="https://opengameart.org/content/bald-man-rigged", license="CC0",
         attribution="optional: EmoPreben", added="2026-11-14",
         notes="zip 원본 포함; OGA 라이선스 CC0; 리깅 포함; 파일 무변경; 썸네일 previews/bald-man-rigged.png",
         preview="previews/bald-man-rigged.png"),
    dict(name="Pocket Bleeps - 31 Retro 8-Bit SFX (Free Sampler, CC-BY)", repo="assets-audio",
         file="pocket-bleeps/pocket-bleeps-free-sampler-31-sfx-wav-cc-by.zip", type="효과음",
         tags="sfx,retro,8bit,ui", author="Pocket Bleeps",
         source_url="https://opengameart.org/content/pocket-bleeps-%E2%80%93-31-retro-8-bit-sfx-free-sampler-cc-by",
         license="CC-BY 4.0", attribution="required: Pocket Bleeps", added="2026-11-14",
         notes="WAV 효과음 샘플러 31개; zip 원본 포함; 사운드 팩이라 썸네일 없음",
         preview=""),
]

OLD = {
    "Low Poly Stalls": "previews/low-poly-stalls.png",
    "low_poly_swords": "previews/low-poly-swords.png",
    "3D Character Pack": "previews/3d-character-pack.png",
    "3D Human Parts Pack": "previews/3d-human-parts-pack.png",
}

with open("catalog.csv", newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    header = list(rdr.fieldnames)
    rows = [dict(r) for r in rdr]

print("header:", header, flush=True)
print("rows before:", len(rows), flush=True)
if "preview" not in header:
    header.append("preview")
for r in rows:
    if r.get("preview") is None:
        r["preview"] = ""

existing = set(r["name"] for r in rows)
added = []
for c in CAND:
    if c["name"] in existing:
        print("skip duplicate:", c["name"], flush=True)
        continue
    row = {k: "" for k in header}
    row.update(c)
    rows.append(row)
    added.append(c)
    print("add:", c["name"], flush=True)

for r in rows:
    if r["name"] in OLD and not r["preview"]:
        r["preview"] = OLD[r["name"]]

with open("catalog.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)

total = len(rows)
n3d = sum(1 for a in added if a["repo"] == "assets-3d-lowpoly-2")
naud = sum(1 for a in added if a["repo"] == "assets-audio")
print("rows after:", total, "added:", len(added), "3d:", n3d, "audio:", naud)

readme = open("README.md", encoding="utf-8").read()
tbl = "\n".join("| %s | %s |" % (a["name"], "CC0" if a["license"] == "CC0" else "CC-BY 4.0") for a in added)

import re as _re
m = _re.search(r"## (\d{4}-\d{2}-\d{2}) A89 추가 \(3팩, 총 1878팩\)", readme)
anchor = m.group(0) if m else "## 2026-11-14 A89 추가"
print("anchor:", anchor, flush=True)

section = ""
section += "## 2026-11-14 A90 추가 (%d팩, 총 %d팩)\n\n" % (len(added), total)
section += "A90 라운드에서 OpenGameArt의 3D %d팩과 효과음 %d팩을 수집했습니다. 중복은 카탈로그 코드 검사(catalog.csv 팩 이름)로 확인했고, 이미 수록된 Bird Bath·low poly iron ore는 제외했습니다.\n\n" % (n3d, naud)
section += "| 팩 | 라이선스 |\n| --- | --- |\n" + tbl + "\n\n"
section += "종류: 3D %d팩(assets-3d-lowpoly-2), 효과음 %d팩(assets-audio). AI 생성 명시 팩 없음. 팩당 1커밋(에셋: <팩 이름> 추가)과 썸네일 커밋(썸네일: <팩 이름> 추가). 썸네일은 previews/<슬러그>.png로 자산 저장소에 커밋하고 catalog.csv preview 열을 채웠습니다. 사운드 팩은 썸네일 대상이 아닙니다. 지난 A88·A89의 네 팩(Low Poly Stalls, low_poly_swords, 3D Character Pack, 3D Human Parts Pack)도 OGA 원본 페이지 미리보기 이미지로 썸네일을 채웠습니다. 색인은 rebuild-index.yml 수동 실행으로 갱신합니다.\n\n" % (n3d, naud)

readme = readme.replace(anchor, section + anchor, 1)
readme = readme.replace("(3팩, 총 1878팩)", "(3팩, 총 1875팩)", 1)
readme = readme.replace("## 2026-11-14 A88 추가 (1팩, 총 1875팩)", "## 2026-11-14 A88 추가 (1팩, 총 1872팩)", 1)
open("README.md", "w", encoding="utf-8").write(readme)
print("readme done", flush=True)

with open("docs/log.md", "a", encoding="utf-8") as f:
    f.write("\n## 2026-11-14 A90 (%d팩, 총 %d팩)\n\n" % (len(added), total))
    for a in added:
        f.write("- %s (%s, %s) -> %s\n" % (a["name"], a["author"], a["license"], a["repo"]))
    f.write("- 썸네일: 신규 3D 팩 + 지난 4팩 previews/<슬러그>.png 커밋, catalog.csv preview 열 갱신\n")
    f.write("- README 제목 숫자 정정: A88 1872, A89 1875, A90 %d\n" % total)
    f.write("- 중복 제외: Bird Bath, low poly iron ore (이미 수록)\n")

subprocess.run(["git", "add", "catalog.csv", "README.md", "docs/log.md"], check=True)
subprocess.run(["git", "commit", "-m", "카탈로그: A90 %d팩 추가" % len(added)], check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
print("DONE", total, len(added), flush=True)
