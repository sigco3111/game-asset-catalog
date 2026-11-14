import csv, subprocess

AUDIO = dict(name="Pocket Bleeps - 31 Retro 8-Bit SFX (Free Sampler, CC-BY)", repo="assets-audio",
    file="pocket-bleeps/pocket-bleeps-free-sampler-31-sfx-wav-cc-by.zip", type="효과음",
    tags="sfx,retro,8bit,ui", author="Pocket Bleeps",
    source_url="https://opengameart.org/content/pocket-bleeps-%E2%80%93-31-retro-8-bit-sfx-free-sampler-cc-by",
    license="CC-BY 4.0", attribution="required: Pocket Bleeps", added="2026-11-14",
    notes="WAV 효과음 샘플러 31개; zip 원본 포함; 사운드 팩이라 썸네일 없음", preview="")

CAND_NAMES = ["Bird Bath", "low poly iron ore", "Chibi Neko by cosmix", "Bald Man - Rigged"]
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

print("rows before:", len(rows), flush=True)
for r in rows:
    if r.get("name") in CAND_NAMES:
        print("existing row:", r.get("name"), "|", r.get("repo"), "|", r.get("file"), "|", r.get("source_url"), flush=True)
    for k in list(r.keys()):
        if k is None:
            del r[k]
            print("dropped None-key column from row", r.get("name"), flush=True)

existing = set(r["name"] for r in rows)
added = []
if AUDIO["name"] in existing:
    print("audio already present", flush=True)
else:
    row = {k: "" for k in header}
    row.update({k: v for k, v in AUDIO.items() if k in header})
    rows.append(row)
    added.append(AUDIO)

for r in rows:
    if r.get("name") in OLD and not r.get("preview"):
        r["preview"] = OLD[r["name"]]

with open("catalog.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k) or "" for k in header})

total = len(rows)
print("rows after:", total, "added:", len(added), flush=True)

readme = open("README.md", encoding="utf-8").read()
anchor = "## 2026-11-14 A89 추가"
section = ""
section += "## 2026-11-14 A90 추가 (1팩, 총 %d팩)\n\n" % total
section += "A90 라운드에서 OpenGameArt의 효과음 1팩 Pocket Bleeps - 31 Retro 8-Bit SFX(Pocket Bleeps, CC-BY 4.0)를 수집했습니다. 3D 후보였던 Bird Bath, low poly iron ore, Chibi Neko by cosmix, Bald Man - Rigged은 카탈로그 코드 검사(catalog.csv 팩 이름)에서 이미 수록된 팩으로 확인되어 제외했습니다.\n\n"
section += "| 팩 | 라이선스 |\n| --- | --- |\n| Pocket Bleeps - 31 Retro 8-Bit SFX | CC-BY 4.0 |\n\n"
section += "종류: 효과음 1팩(assets-audio). 라이선스: CC-BY 4.0 1팩. AI 생성 명시 팩 없음. 팩 1커밋(에셋: <팩 이름> 추가). 사운드 팩은 썸네일 대상이 아닙니다. 지난 A88·A89의 네 팩(Low Poly Stalls, low_poly_swords, 3D Character Pack, 3D Human Parts Pack)은 OGA 원본 페이지 미리보기 이미지로 previews/<슬러그>.png 썸네일을 만들어 preview 열을 채웠습니다. 색인은 rebuild-index.yml 수동 실행으로 갱신합니다.\n\n"

readme = readme.replace(anchor, section + anchor, 1)
readme = readme.replace("## 2026-11-14 A89 추가 (3팩, 총 1878팩)", "## 2026-11-14 A89 추가 (3팩, 총 1875팩)", 1)
readme = readme.replace("## 2026-11-14 A88 추가 (1팩, 총 1875팩)", "## 2026-11-14 A88 추가 (1팩, 총 1872팩)", 1)
open("README.md", "w", encoding="utf-8").write(readme)
print("readme ok", flush=True)

with open("docs/log.md", "a", encoding="utf-8") as f:
    f.write("\n## 2026-11-14 A90 (1팩, 총 %d팩)\n\n" % total)
    f.write("- Pocket Bleeps - 31 Retro 8-Bit SFX (Pocket Bleeps, CC-BY 4.0) -> assets-audio\n")
    f.write("- 3D 후보 4종(Bird Bath, low poly iron ore, Chibi Neko by cosmix, Bald Man - Rigged)은 이미 수록되어 제외\n")
    f.write("- 썸네일: 지난 4팩 previews/<슬러그>.png 커밋, catalog.csv preview 열 갱신\n")
    f.write("- README 제목 숫자 정정: A88 1872, A89 1875, A90 %d\n" % total)

subprocess.run(["git", "add", "catalog.csv", "README.md", "docs/log.md"], check=True)
subprocess.run(["git", "commit", "-m", "카탈로그: A90 1팩 추가"], check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
print("DONE", total, flush=True)
