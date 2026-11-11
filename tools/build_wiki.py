#!/usr/bin/env python3
"""assets-index.json -> docs/wiki/*.md (+ llms.txt in the repo root).

Python 3 standard library only; deterministic (no timestamps, no network).
docs/wiki/usage-ledger.md is maintained by hand and is never written here.
Usage: python3 tools/build_wiki.py [--check]
  (default) generate, then validate links and row counts; --check only validates.
"""
import argparse, json, os, re, sys
from collections import Counter, OrderedDict

SITE = "https://sigco3111.github.io/game-asset-catalog/"
RAW = "https://raw.githubusercontent.com/sigco3111/game-asset-catalog/main/"
NOTE = "> 이 문서는 tools/build_wiki.py가 assets-index.json에서 자동 생성합니다. 직접 고치지 마세요."
MAX_ROWS = 400
RECENT_N = 100
MANUAL = {"usage-ledger.md"}          # 손으로 쓰는 문서: 생성기가 건드리지 않음
ALLOWED = ("cc0", "cc-by", "mit", "gpl")
FAMILY_KO = OrderedDict([("cc0", "CC0"), ("cc-by", "CC-BY"), ("mit", "MIT"), ("gpl", "GPL 2.0/3.0"), ("other", "기타(허용 목록 밖)")])

# app.js의 CAT_LABEL / FX 와 같은 이름 (분류 순서도 동일)
CATEGORY_KO = OrderedDict([
    ("effect", "이펙트"), ("sfx", "효과음"), ("music", "음악"), ("voice", "음성"),
    ("tileset-2d", "2D 타일셋"), ("sprite-2d", "2D 스프라이트"), ("background-2d", "2D 배경"), ("map-2d", "2D 맵"),
    ("ui", "UI"), ("icon", "아이콘"), ("portrait", "초상화"), ("font", "폰트"), ("texture", "텍스처"),
    ("model-3d", "3D 모델"), ("character-3d", "3D 캐릭터"), ("vehicle-3d", "3D 탈것"), ("building-3d", "3D 건물"),
    ("board", "보드게임"), ("puzzle", "퍼즐"), ("other", "기타")])
EFFECT_KO = OrderedDict([
    ("hit", "타격"), ("impact", "충격"), ("magic", "마법"), ("explosion", "폭발"), ("fire", "불"),
    ("ice", "얼음"), ("lightning", "번개"), ("wind", "바람"), ("heal", "치유"), ("laser", "레이저"),
    ("particle", "입자"), ("smoke", "연기"), ("aura", "오라"), ("projectile", "투사체"), ("slash", "베기")])

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "docs", "wiki")
HEAD = ["이름", "분류", "제작자", "라이선스", "표기 필요", "AI 생성", "파일", "추가일"]


# ---------- 문자열 처리 ----------
def esc(s):
    """표 셀·링크 텍스트용 이스케이프: 파이프·줄바꿈·마크다운 기호."""
    s = "" if s is None else str(s)
    s = re.sub(r"\s*[\r\n]+\s*", " ", s).strip()
    s = s.replace("\\", "\\\\")
    for ch in "|`*_[]":
        s = s.replace(ch, "\\" + ch)
    return s.replace("<", "&lt;").replace(">", "&gt;")


def url(u):
    return "".join({" ": "%20", "(": "%28", ")": "%29", "|": "%7C", "<": "%3C", ">": "%3E"}.get(c, c) for c in u)


def link(text, u):
    return "[%s](%s)" % (esc(text), url(u))


def oxs(b):
    return "O" if b else "X"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def sort_assets(items):
    items = sorted(items, key=lambda a: (a["name"].casefold(), a["name"], a["id"]))
    return sorted(items, key=lambda a: a["added"] or "", reverse=True)   # 안정 정렬: 추가일 내림차순, 같으면 이름순


def file_cell(a):
    if a.get("download_url"):
        return link("다운로드", a["download_url"])
    n = len(a.get("download_urls") or a.get("split_parts") or [])
    return "%d개 분할" % n if n else "-"


def row(a):
    return [link(a["name"], a["source_url"]) if a.get("source_url") else esc(a["name"]),
            "`%s`" % a["category"], esc(a["author"]) or "-", esc(a["license"]) or "-",
            oxs(a["attribution_required"]), oxs(a["ai_generated"]), file_cell(a), a["added"] or "-"]


def page(title, commit, body):
    L = [NOTE, "", "> generated from `catalog.csv@%s`" % commit, "", "# " + title, ""] + body
    while L and L[-1] == "":
        L.pop()
    return "\n".join(L) + "\n"


# ---------- 목록 쪽 ----------
def list_pages(slug, title, intro, items, commit):
    """slug.md, slug-2.md ... 을 만든다 (표가 MAX_ROWS 초과 시 분할). {파일명: 내용}."""
    items = sort_assets(items)
    chunks = [items[i:i + MAX_ROWS] for i in range(0, len(items), MAX_ROWS)] or [[]]
    names = [slug + ".md"] + ["%s-%d.md" % (slug, i) for i in range(2, len(chunks) + 1)]
    out = OrderedDict()
    for i, (name, chunk) in enumerate(zip(names, chunks)):
        body = list(intro)
        if len(chunks) > 1:
            body += ["이 목록은 %d쪽으로 나뉩니다(쪽당 최대 %d행): " % (len(chunks), MAX_ROWS)
                     + " · ".join(("**%d쪽**" % (j + 1)) if j == i else "[%d쪽](%s)" % (j + 1, n) for j, n in enumerate(names)), ""]
        body += ["현재 쪽: %d행 (전체 %d개). 정렬: 추가일 내림차순, 같으면 이름순." % (len(chunk), len(items)), ""]
        body += table(HEAD, [row(a) for a in chunk]) if chunk else ["(해당 에셋 없음)"]
        out[name] = page(title if i == 0 else "%s (%d쪽)" % (title, i + 1), commit, body)
    return out


def nav():
    return ["[위키 홈](README.md) · [라이선스](licenses.md) · [최근 추가](recent.md) · [사용 장부](usage-ledger.md)", ""]


COLS = ["표 열: 이름(출처 링크) · 분류 · 제작자 · 라이선스 · 표기 필요(O/X) · AI 생성(O/X) · 파일(내려받기 링크 또는 'N개 분할') · 추가일.",
        "'N개 분할'은 내려받기 주소가 여러 개인 에셋입니다. 모든 주소는 [assets-index.json](../../assets-index.json)의 `download_urls`에 있습니다.", ""]


# ---------- 문서 만들기 ----------
def build(doc):
    commit = doc["generated_from"].split("@", 1)[1] if "@" in doc["generated_from"] else "unknown"
    assets = doc["assets"]
    N = len(assets)
    by_cat = {k: [a for a in assets if a["category"] == k] for k in CATEGORY_KO}
    unknown_cat = sorted({a["category"] for a in assets} - set(CATEGORY_KO))
    if unknown_cat:
        sys.exit("unknown category: %s" % unknown_cat)
    by_fx = {k: [a for a in assets if k in a["effect_kind"]] for k in EFFECT_KO}
    unknown_fx = sorted({k for a in assets for k in a["effect_kind"]} - set(EFFECT_KO))
    if unknown_fx:
        sys.exit("unknown effect_kind: %s" % unknown_fx)
    out = OrderedDict()
    page_of = {}                                    # 분류/효과 -> 첫 쪽 파일명

    for k, ko in EFFECT_KO.items():
        intro = nav() + ["효과 종류 `%s`(%s)에 해당하는 에셋 **%d개**입니다. 에셋 하나가 여러 효과 종류를 가질 수 있어 다른 효과 쪽과 겹칠 수 있습니다." % (k, ko, len(by_fx[k])),
                         "라이브러리에서 보기: [?fx=%s](%s?fx=%s)" % (k, SITE, k)]
        if k in ("hit", "impact"):
            intro[-1] += " (라이브러리는 hit·impact를 '타격·충격' 하나로 묶어 보여줍니다.)"
        intro += [""] + COLS
        title = "타격·충격 이펙트 모음 — %s" % k if k in ("hit", "impact") else "%s 이펙트 모음" % ko
        out.update(list_pages("effects-" + k, title, intro, by_fx[k], commit))
        page_of[("fx", k)] = "effects-%s.md" % k

    for k, ko in CATEGORY_KO.items():
        intro = nav() + ["분류 `%s`(%s)에 해당하는 에셋 **%d개**입니다. 라이브러리에서 보기: [?cat=%s](%s?cat=%s)" % (k, ko, len(by_cat[k]), k, SITE, k), ""] + COLS
        out.update(list_pages("category-" + k, "%s 모음" % ko, intro, by_cat[k], commit))
        page_of[("cat", k)] = "category-%s.md" % k

    recent = sort_assets(assets)[:RECENT_N]
    out["recent.md"] = page("최근 추가된 에셋 (최신 %d개)" % RECENT_N, commit, nav() + [
        "추가일이 가장 최근인 에셋 %d개입니다(추가일 내림차순, 같으면 이름순). 가장 이른 추가일: %s." % (len(recent), recent[-1]["added"]), ""] + COLS
        + table(HEAD, [row(a) for a in recent]))

    out["licenses.md"] = licenses_page(assets, commit)
    out["README.md"] = home_page(assets, commit, page_of, by_cat, by_fx)
    return commit, out


def licenses_page(assets, commit):
    N = len(assets)
    fam = Counter(a["license_family"] for a in assets)
    B = nav() + [
        "에셋 **%d개**의 라이선스 사실을 `assets-index.json`에서 그대로 옮긴 문서입니다. 라이선스를 해석하거나 바꿔 적지 않습니다. 의심스러우면 각 에셋의 출처 링크와 zip 안 원본 License 파일을 확인하세요." % N, "",
        "## 허용 라이선스", "",
        "이 카탈로그가 허용하는 라이선스는 **CC0, CC-BY, MIT, GPL 2.0/3.0**뿐입니다. 이 밖의 에셋은 아래 '허용 목록 밖' 절에 따로 표시합니다.", "",
        "## 라이선스 계열(license_family)별 개수", ""]
    rows = []
    for f, ko in FAMILY_KO.items():
        if fam.get(f):
            rows.append([f, ko, str(fam[f]), str(sum(1 for a in assets if a["license_family"] == f and a["attribution_required"])),
                         "예" if f in ALLOWED else "아니오"])
    B += table(["license_family", "이름", "개수", "표기 필요 개수", "허용 목록"], rows)
    B += ["", "## 라이선스 문구(license)별 개수", "", "문구는 색인의 `license` 값 그대로입니다.", ""]
    lc = Counter((a["license"], a["license_family"], a["attribution_required"]) for a in assets)
    B += table(["license", "license_family", "표기 필요", "개수"],
               [[esc(l), f, oxs(r), str(n)] for (l, f, r), n in sorted(lc.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))])
    B += ["", "## 표기가 필요한 에셋", "",
          "`attribution_required`가 참인 에셋 %d개입니다(CC-BY·MIT·GPL). '표기 문구'는 색인의 `attribution` 값 그대로입니다. CC0 에셋은 표기가 필수가 아닙니다." % sum(a["attribution_required"] for a in assets), ""]
    B += table(["이름", "제작자", "라이선스", "표기 문구", "추가일"],
               [[link(a["name"], a["source_url"]), esc(a["author"]), esc(a["license"]), esc(a["attribution"]) or "-", a["added"]]
                for a in sort_assets([a for a in assets if a["attribution_required"]])])
    notes = [a for a in assets if a["license_note"]]
    B += ["", "## 라이선스 비고(license_note)가 있는 에셋", "",
          "이중 표기 등으로 선택한 라이선스를 기록한 에셋 %d개입니다. 비고는 색인 값 그대로입니다." % len(notes), ""]
    B += table(["이름", "라이선스", "비고"], [[link(a["name"], a["source_url"]), esc(a["license"]), esc(a["license_note"])] for a in sort_assets(notes)])
    out = [a for a in assets if a["license_family"] not in ALLOWED]
    B += ["", "## 허용 목록 밖 에셋 (확인 없이 쓰지 마세요)", "",
          "license_family가 `cc0`·`cc-by`·`mit`·`gpl`이 아닌 에셋 %d개입니다. **do not use without checking** — 사용하기 전에 라이선스 문구와 출처를 직접 확인하세요." % len(out), ""]
    B += table(["이름", "license_family", "라이선스", "표기 필요", "AI 생성", "추가일"],
               [[link(a["name"], a["source_url"]), a["license_family"], esc(a["license"]), oxs(a["attribution_required"]), oxs(a["ai_generated"]), a["added"]] for a in sort_assets(out)])
    ai = [a for a in assets if a["ai_generated"]]
    B += ["", "## AI 생성 표시 에셋", "", "`ai_generated`가 참인 에셋 %d개입니다. 라이브러리에서는 `?ai=0`으로 제외할 수 있습니다." % len(ai), ""]
    B += table(["이름", "분류", "라이선스 계열", "추가일"], [[link(a["name"], a["source_url"]), "`%s`" % a["category"], a["license_family"], a["added"]] for a in sort_assets(ai)])
    return page("라이선스 모음", commit, B)


def home_page(assets, commit, page_of, by_cat, by_fx):
    N = len(assets)
    nattr = sum(a["attribution_required"] for a in assets)
    nai = sum(a["ai_generated"] for a in assets)
    B = [
        "게임 에셋 카탈로그(sigco3111/game-asset-catalog)의 **주제별 모음 위키**입니다. 사람과 AI 에이전트가 에셋을 빨리 찾고, 라이선스와 표기 의무를 확인하고, 쓴 기록을 남기도록 돕습니다.",
        "", "## 이 위키는 어떻게 만들어지나", "",
        "- `catalog.csv` → `python3 tools/build_index.py` → `assets-index.json` → `python3 tools/build_wiki.py` → `docs/wiki/*.md`, `llms.txt`.",
        "- 이 위키의 자동 생성 문서는 직접 고치지 않습니다. 에셋이 바뀌면 두 스크립트를 다시 실행합니다(표준 라이브러리만 사용, 같은 입력이면 같은 출력).",
        "- 에셋마다 쪽을 따로 만들지 않습니다. 표의 이름을 누르면 제작자의 출처 페이지로 갑니다.",
        "- 손으로 쓰는 문서는 [사용 장부](usage-ledger.md) 하나뿐이며 생성기가 덮어쓰지 않습니다.",
        "- 현재 색인: 에셋 **%d개** (`catalog.csv@%s`)." % (N, commit), "",
        "## 링크", "",
        "- 에셋 도서관(검색 사이트): %s" % SITE,
        "- 색인: [assets-index.json](../../assets-index.json), [assets-index.min.json](../../assets-index.min.json) · 원본 표: [catalog.csv](../../catalog.csv) · 점검 보고서: [index-report.md](../index-report.md)",
        "- 에이전트용 안내: [llms.txt](../../llms.txt)",
        "- [라이선스 모음](licenses.md) · [최근 추가 %d개](recent.md) · [사용 장부](usage-ledger.md)" % RECENT_N, "",
        "## 라이선스 규칙", "",
        "- 허용 라이선스: **CC0, CC-BY, MIT, GPL 2.0/3.0**만 수록합니다. 그 밖의 라이선스는 쓰기 전에 직접 확인합니다(자세한 목록은 [licenses.md](licenses.md)).",
        "- 라이선스를 재해석하지 않습니다. 색인의 `license`, `license_note`, `attribution` 값을 그대로 따릅니다.",
        "- GPL 에셋은 원본 GPL 조건(라이선스 고지, 소스 공개 등)을 유지합니다.", "",
        "## 표기(attribution) 규칙", "",
        "- 색인의 `attribution_required`가 참이면(%d개: CC-BY·MIT·GPL) 에셋을 쓰는 프로젝트의 `CREDITS.md`에 제작자·출처·라이선스를 적습니다. 문구 예시는 색인의 `attribution` 값입니다." % nattr,
        "- CC0는 표기가 필수가 아니며, 색인에는 선택 표기 문구만 있습니다.",
        "- 쓴 에셋은 [사용 장부](usage-ledger.md)에도 한 줄 기록합니다.", "",
        "## AI 생성 표시", "",
        "- 색인의 `ai_generated`가 참인 에셋(%d개)은 표에서 'AI 생성'이 **O**로 표시됩니다. 라이브러리에서는 `?ai=0`으로 제외할 수 있습니다." % nai, "",
        "## 분류별 개수", ""]
    B += table(["분류", "이름", "개수", "목록"], [["`%s`" % k, CATEGORY_KO[k], str(len(by_cat[k])), "[%s](%s)" % (page_of[("cat", k)], page_of[("cat", k)])] for k in CATEGORY_KO])
    B += ["", "합계 %d개. 분류가 400행을 넘는 목록은 `-2` 쪽으로 이어집니다." % sum(len(v) for v in by_cat.values()), "",
          "## 효과 종류별 개수", "", "한 에셋이 여러 효과 종류를 가질 수 있어 합계가 에셋 수와 다를 수 있습니다.", ""]
    B += table(["효과 종류", "이름", "개수", "목록"], [["`%s`" % k, EFFECT_KO[k], str(len(by_fx[k])), "[%s](%s)" % (page_of[("fx", k)], page_of[("fx", k)])] for k in EFFECT_KO])
    return page("게임 에셋 카탈로그 위키", commit, B)


def llms_text(doc, commit):
    assets = doc["assets"]
    N = len(assets)
    cat = Counter(a["category"] for a in assets)
    fam = Counter(a["license_family"] for a in assets)
    fx = Counter(k for a in assets for k in a["effect_kind"])
    nattr = sum(a["attribution_required"] for a in assets)
    nai = sum(a["ai_generated"] for a in assets)
    j = lambda c, keys: ", ".join("%s %d" % (k, c[k]) for k in keys if c.get(k))
    return """# game-asset-catalog

> generated from `catalog.csv@%(c)s` by tools/build_wiki.py (do not edit by hand)

Catalog of %(n)d free game asset packs (2D sprites and tilesets, 3D models, UI and icons, sound effects, music, VFX) with source, author, licence and attribution data. Only redistributable licences are listed. The packs themselves live in sibling repos (assets-2d-pixel, assets-3d-lowpoly, assets-ui-icons, assets-audio, assets-2d-portraits); this repo holds the index, the search site and a wiki.

## Machine-readable data
- Library site (search UI): %(site)s
- Index, full fields: %(raw)sassets-index.json
- Index, minified (same content, ~2 MB): %(raw)sassets-index.min.json
- Source table: %(raw)scatalog.csv (`catalog.csv` is the source of truth; the index is generated from it)
- Index report: %(raw)sdocs/index-report.md
- Wiki home: %(raw)sdocs/wiki/README.md (topic pages: effects-<kind>.md, category-<category>.md, licenses.md, recent.md)
- Usage ledger (which project uses which asset): %(raw)sdocs/wiki/usage-ledger.md

## How to search
Load assets-index.json (`{schema, generated_from, count, assets[]}`) and filter `assets` by field:
- `category`: effect, sfx, music, voice, tileset-2d, sprite-2d, background-2d, map-2d, ui, icon, portrait, font, texture, model-3d, character-3d, vehicle-3d, building-3d, board, puzzle, other
- `effect_kind` (list): hit, impact, magic, explosion, fire, ice, lightning, wind, heal, laser, particle, smoke, aura, projectile, slash
- `license_family`: cc0, cc-by, mit, gpl, other; `attribution_required`: bool; `ai_generated`: bool
- other fields: id, name, repo, type, tags[], author, source_url, license, license_note, attribution, added, notes, preview, download_url, download_urls[] (several URLs = split archive, download all parts), multipart.
Library URL query parameters (confirmed in app.js): `q` search words; `cat` category; `repo` 2d|3d|ui|audio|portrait; `lic` cc0|cc-by|mit|gpl|other; `fx` comma list (hit covers hit+impact); `sort` name|type (default newest); `ai=0` hides AI-generated; `noattr=1` only assets needing no attribution; `author` exact author name.
Example: %(site)s?cat=sfx&fx=explosion&lic=cc0&sort=name

## Licence rules
- Allowed: CC0, CC-BY, MIT, GPL 2.0/3.0 only. Anything else (`license_family` = other) must be checked by a human before use.
- Never reinterpret a licence: copy `license`, `license_note` and `attribution` from the index; follow the original licence file inside each zip.
- If `attribution_required` is true (CC-BY, MIT, GPL), credit author, source_url and licence in the using project's CREDITS.md. CC0 needs no credit. GPL assets keep GPL conditions when redistributed.
- Respect `ai_generated`; mark such assets as AI-generated in your project.

## Using an asset and recording it
1. Find the asset in the index; check licence fields. 2. Download via `download_url` (or every URL in `download_urls`). 3. Add credits to the project's CREDITS.md when attribution is required. 4. Add one row per asset per project to docs/wiki/usage-ledger.md (columns: 프로젝트 | 에셋 이름 | 제작자 | 출처 URL | 라이선스 | 표기 위치 | 기록일).

## Regenerate
`python3 tools/build_index.py` (catalog.csv -> assets-index.json, assets-index.min.json, docs/index-report.md) then `python3 tools/build_wiki.py` (-> docs/wiki/*.md and this file). Python 3 stdlib only; output is deterministic. `python3 tools/build_wiki.py --check` validates links and counts.

## Counts snapshot (catalog.csv@%(c)s)
- Assets: %(n)d; attribution required: %(na)d; AI-generated: %(nai)d
- By licence family: %(fam)s
- By category: %(cat)s
- By effect_kind: %(fx)s
""" % dict(c=commit, n=N, site=SITE, raw=RAW, na=nattr, nai=nai, fam=j(fam, FAMILY_KO), cat=j(cat, CATEGORY_KO), fx=j(fx, EFFECT_KO))


# ---------- 검증 ----------
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def check(doc, expected_names):
    errs = []
    assets = doc["assets"]
    files = sorted(f for f in os.listdir(WIKI) if f.endswith(".md"))
    for rel in sorted(expected_names | MANUAL):
        if rel not in files:
            errs.append("missing file: " + rel)
    for f in files:
        text = open(os.path.join(WIKI, f), encoding="utf-8").read()
        if f not in MANUAL and not text.startswith(NOTE + "\n"):
            errs.append("%s: missing header note" % f)
        if len(text.encode("utf-8")) > 300_000:
            errs.append("%s: larger than 300 KB" % f)
        for m in LINK_RE.finditer(text):
            u = m.group(1)
            if re.match(r"[a-z][a-z0-9+.-]*:", u) or u.startswith("#"):
                continue
            path = os.path.normpath(os.path.join(WIKI, u.split("#")[0]))
            if not os.path.exists(path):
                errs.append("%s: broken link %s" % (f, u))

    def rows_in(prefix_names):
        n = 0
        for f in prefix_names:
            for line in open(os.path.join(WIKI, f), encoding="utf-8").read().splitlines():
                if line.startswith("| ") and not line.startswith("| " + HEAD[0]):
                    n += 1
        return n

    report = []
    for kind, keys, getter in (("effects", EFFECT_KO, lambda a, k: k in a["effect_kind"]),
                               ("category", CATEGORY_KO, lambda a, k: a["category"] == k)):
        for k in keys:
            names = [f for f in files if f == "%s-%s.md" % (kind, k) or re.fullmatch(r"%s-%s-\d+\.md" % (kind, re.escape(k)), f)]
            want = sum(1 for a in assets if getter(a, k))
            got = rows_in(names)
            report.append("%s %s: pages=%d rows=%d index=%d %s" % (kind, k, len(names), got, want, "OK" if got == want else "MISMATCH"))
            if got != want:
                errs.append("count mismatch %s %s: rows=%d index=%d" % (kind, k, got, want))
    rc = rows_in(["recent.md"])
    if rc != min(RECENT_N, len(assets)):
        errs.append("recent rows %d" % rc)
    return errs, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="생성하지 않고 링크·개수만 검증")
    args = ap.parse_args()
    with open(os.path.join(ROOT, "assets-index.json"), encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("count") != len(doc["assets"]):
        sys.exit("count field does not match assets length")
    commit, pages = build(doc)
    if not args.check:
        os.makedirs(WIKI, exist_ok=True)
        for name in os.listdir(WIKI):                               # 오래된 생성 쪽만 정리 (손글씨 문서는 건드리지 않음)
            if name not in pages and name not in MANUAL and re.fullmatch(r"(effects|category)-.*\.md|recent\.md|licenses\.md|README\.md", name):
                os.remove(os.path.join(WIKI, name))
        for name, text in pages.items():
            with open(os.path.join(WIKI, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(llms_text(doc, commit))
    errs, report = check(doc, set(pages))
    sizes = sorted(((len(t.encode("utf-8")), n) for n, t in pages.items()), reverse=True)
    print("pages=%d (+%d manual) assets=%d commit=%s biggest=%s" % (len(pages), len(MANUAL), len(doc["assets"]), commit, sizes[:3]))
    if args.check:
        print("\n".join(report))
    for e in errs:
        print("ERROR:", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
