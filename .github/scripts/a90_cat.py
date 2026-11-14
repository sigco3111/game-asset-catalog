import csv, os, subprocess

NEW = [
    dict(name="Bird Bath", repo="assets-3d-lowpoly-2", file="bird-bath/birdbath_0.zip", type="3D 모델",
         tags="nature,garden,prop,lowpoly", author="JeremyWoods",
         source_url="https://opengameart.org/content/bird-bath", license="CC0",
         attribution="optional: JeremyWoods", added="2026-11-14",
         notes="zip 원본 포함; OGA 라이선스 CC0; 파일 무변경; 썸네일 previews/bird-bath.png",
         preview="previews/bird-bath.png"),
    dict(name="low poly iron ore", repo="assets-3d-lowpoly-2", file="low-poly-iron-ore/stone_1.zip", type="3D 모델",
         tags="rock,ore,prop,lowpoly", author="musher3004",
         source_url="https://opengameart.org/content/low-poly-iron-ore", license="CC0",
         attribution="optional: musher3004", added="2026-11-14",
         notes="zip 원본 포함; OGA 라이선스 CC0; 파일 무변경; 썸네일 previews/low-poly-iron-ore.png",
         preview="previews/low-poly-iron-ore.png"),
    dict(name="Chibi Neko by cosmix", repo="assets-3d-lowpoly-2", file="chibi-neko/chibineko.zip", type="3D 캐릭터",
         tags="character,cat,chibi,lowpoly", author="zodiepupper",
         source_url="https://opengameart.org/content/chibi-neko-by-cosmix", license="CC0",
         attribution="optional: zodiepupper", added="2026-11-14",
         notes="zip 원본 포함; OGA 라이선스 CC0; 파일 무변경; 썸네일 previews/chibi-neko.png",
         preview="previews/chibi-neko.png"),
    dict(name="Pocket Bleeps - 31 Retro 8-Bit SFX (Free Sampler, CC-BY)", repo="assets-audio",
         file="pocket-bleeps/pocket-bleeps-free-sampler-31-sfx-wav-cc-by.zip", type="효과음",
         tags="sfx,retro,8bit,ui", author="Pocket Bleeps",
         source_url="https://opengameart.org/content/pocket-bleeps-%E2%80%93-31-retro-8-bit-sfx-free-sampler-cc-by",
         license="CC-BY 4.0", attribution="required: Pocket Bleeps", added="2026-11-14",
         notes="WAV 효과음 31개 샘플러; zip 원본 포함; 사운드 팩이라 썸네일 없음",
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
        r.setdefault("preview", "")

existing = set(r["name"] for r in rows)
for n in NEW:
    if n["name"] in existing:
        raise SystemExit("duplicate: " + n["name"])

for n in NEW:
    row = {k: "" for k in header}
    row.update(n)
    rows.append(row)

for r in rows:
    if r["name"] in OLD and not r.get("preview"):
        r["preview"] = OLD[r["name"]]

with open("catalog.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)

total = len(rows)
print("rows after:", total, flush=True)

readme = open("README.md", encoding="utf-8").read()
a89 = "## 2026-11-14 A89 추가 (3팩, 총 1878팩)"
a88 = "## 2026-11-14 A88 추가 (1팩, 총 1875팩)"
print("a89 found:", a89 in readme, "a88 found:", a88 in readme, flush=True)
readme = readme.replace(a89, "## 2026-11-14 A89 추가 (3팩, 총 1875팩)")
readme = readme.replace(a88, "## 2026-11-14 A88 추가 (1팩, 총 1872팩)")

section = """## 2026-11-14 A90 추가 (4팩, 총 %d팩)

A90 라운드에서 OpenGameArt의 3D 3팩 Bird Bath(JeremyWoods, CC0), low poly iron ore(musher3004, CC0), Chibi Neko by cosmix(zodiepupper, CC0)와 효과음 1팩 Pocket Bleeps - 31 Retro 8-Bit SFX(Pocket Bleeps, CC-BY 4.0)를 수집했습니다. 중복은 카탈로그 저장소 코드 검색(catalog.csv 팩 이름 검사)으로 확인했습니다.

| 팩 | 라이선스 |
| --- | --- |
| Bird Bath | CC0 |
| low poly iron ore | CC0 |
| Chibi Neko by cosmix | CC0 |
| Pocket Bleeps - 31 Retro 8-Bit SFX | CC-BY 4.0 |

종류: 3D 3팩(assets-3d-lowpoly-2), 효과음 1팩(assets-audio). 라이선스: CC0 3팩, CC-BY 4.0 1팩. AI 생성 명시 팩 없음. 팩당 1커밋(에셋: <팩 이름> 추가)에 썸네일 커밋(썸네일: <팩 이름> 추가)을 더했습니다. 썸네일은 previews/<슬러그>.png로 각 자산 저장소에 커밋하고 catalog.csv preview 열을 채웠습니다. 사운드 팩은 썸네일 대상이 아닙니다. 지난 A88·A89의 네 팩(Low Poly Stalls, low_poly_swords, 3D Character Pack, 3D Human Parts Pack)도 OGA 원본 페이지 미리보기 이미지로 썸네일을 채웠습니다. 색인은 rebuild-index.yml 수동 실행으로 갱신합니다.

""" % total

readme = readme.replace("## 2026-11-14 A89 추가", section + "## 2026-11-14 A89 추가", 1)
open("README.md", "w", encoding="utf-8").write(readme)

with open("docs/log.md", "a", encoding="utf-8") as f:
    f.write("\n## 2026-11-14 A90 (4팩, 총 %d팩)\n\n" % total)
    f.write("- OpenGameArt 3D 3팩: Bird Bath(JeremyWoods, CC0), low poly iron ore(musher3004, CC0), Chibi Neko by cosmix(zodiepupper, CC0) -> assets-3d-lowpoly-2\n")
    f.write("- OpenGameArt 효과음 1팩: Pocket Bleeps - 31 Retro 8-Bit SFX(Pocket Bleeps, CC-BY 4.0) -> assets-audio\n")
    f.write("- 썸네일: 신규 3D 3팩 + 지난 4팩(Low Poly Stalls, low_poly_swords, 3D Character Pack, 3D Human Parts Pack) previews/<슬러그>.png\n")
    f.write("- README 제목 숫자 정정: A88 1872, A89 1875, A90 %d\n" % total)
    f.write("- 임시 워크플로 a90-ingest.yml / a90-run*.yml 과 스크립트 a90*.py는 수집 후 삭제\n")

subprocess.run(["git", "add", "catalog.csv", "README.md", "docs/log.md"], check=True)
subprocess.run(["git", "commit", "-m", "카탈로그: A90 4팩 추가"], check=True)
subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
print("DONE", total, flush=True)
