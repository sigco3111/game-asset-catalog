#!/usr/bin/env python3
"""catalog.csv -> assets-index.json (+ .min.json if >1.5MB) + docs/index-report.md.

Python 3 standard library only; deterministic (no timestamps, no network).
Usage: python3 tools/build_index.py [--commit HASH] [--link-check FILE]
"""
import argparse, csv, json, os, re, subprocess, sys
from collections import Counter, OrderedDict
from urllib.parse import quote

OWNER = "sigco3111"
MIN_THRESHOLD = 1_500_000
MIN_ROWS = 100  # 데이터 행이 이보다 적으면 색인을 만들지 않음 (빈 색인이 커밋되는 것을 막음)
REQUIRED = ["name", "repo", "file", "type", "license", "source_url"]
LC_START, LC_END = "<!-- link-check:start -->", "<!-- link-check:end -->"

CATEGORY = {
    "효과음": "sfx", "음악": "music", "배경음악": "music", "음성": "voice",
    "이펙트": "effect", "2D 이펙트": "effect",
    "2D 타일셋": "tileset-2d", "2D 스프라이트": "sprite-2d", "2D 스프라이트·타일셋": "sprite-2d",
    "2D 캐릭터": "sprite-2d", "2D 배경": "background-2d", "2D 맵": "map-2d",
    "UI·아이콘": "ui", "2D UI": "ui", "UI 키트": "ui",
    "아이콘": "icon", "2D 아이콘": "icon", "폰트": "font", "2D 글자": "font",
    "2D 텍스처": "texture",
    "3D": "model-3d", "3D 모델": "model-3d", "3D 모듈 키트": "model-3d", "3D 모듈러": "model-3d",
    "3D 소품": "model-3d", "3D 환경": "model-3d", "3D 자연": "model-3d", "3D 무기": "model-3d",
    "3D 동물": "model-3d", "3D 애니메이션": "model-3d", "3D 타일셋": "model-3d",
    "3D 캐릭터 의상": "model-3d",
    "3D 캐릭터": "character-3d", "3D 탈것": "vehicle-3d", "3D 건물": "building-3d",
    "보드게임": "board", "2D 퍼즐": "puzzle",
}
CATEGORIES = ["effect", "sfx", "music", "voice", "tileset-2d", "sprite-2d", "background-2d", "map-2d",
              "ui", "icon", "portrait", "font", "texture", "model-3d", "character-3d", "vehicle-3d",
              "building-3d", "board", "puzzle", "other"]

EFFECT_KEYWORDS = OrderedDict([
    ("hit", r"hits?|타격"),
    ("impact", r"impacts?|충격"),
    ("magic", r"magic|magical|spells?|arcane|마법"),
    ("explosion", r"explosions?|explode[sd]?|booms?|blasts?|폭발"),
    ("lightning", r"lightning|thunder|electric|electricity|shock|번개|전기"),
    ("fire", r"fire|fireball|flames?|burn|burning|화염"),
    ("ice", r"ice|icy|icicles?|frost|frozen|freeze|얼음"),
    ("wind", r"wind|gust|tornado|바람"),
    ("heal", r"heal|heals|healing|치유|회복"),
    ("laser", r"lasers?|레이저"),
    ("particle", r"particles?|파티클"),
    ("smoke", r"smoke|연기"),
    ("aura", r"auras?|오라"),
    ("projectile", r"projectiles?|bullets?|missiles?|투사체"),
    ("slash", r"slash|slashes|slashing|참격"),
])
EFFECT_RE = {k: re.compile(r"(?<![a-z0-9])(?:%s)(?![a-z0-9])" % v) for k, v in EFFECT_KEYWORDS.items()}

AI_RE = re.compile(r"AI 생성(?!\s*(?:아님|여부))")
# 긍정 표현: 'AI-generated' / 'AI generated' / 'AI 생성물' (앞에 not/non/no 또는 뒤에 아님/여부가 오면 제외)
AI_TEXT_RE = re.compile(r"(?<![A-Za-z])(?<!not )(?<!non-)(?<!no )AI[- ]generated(?![A-Za-z])|AI 생성물(?!\s*(?:아님|이 아님|여부))", re.I)
NO_ATTR_RE = re.compile(r"(?:없음|none|n/a)", re.I)
LICENSE_BASE_RE = re.compile(r"(?:CC0|CC-BY(?:[ -][34]\.0)?|MIT|GPL [23]\.0)")

# 2D 일반 type 세분화 키워드 (name/tags/정제한 notes에서 단어 단위 일치, 유일하게 일치할 때만 적용)
REFINE_KEYWORDS = OrderedDict([
    ("portrait", r"portraits?|avatars?|초상화?"),
    ("font", r"fonts?|typefaces?|glyphs?|폰트|글꼴"),
    ("texture", r"textures?|텍스처"),
    ("effect", r"effects?|fx|explosions?|particles?|lasers?|slash|spells?|auras?|smoke|이펙트"),
    ("ui", r"ui|gui|hud|user interfaces?|interfaces?|buttons?|menus?|dialogu?es?"),
    ("icon", r"icons?|아이콘"),
    ("background-2d", r"backgrounds?|parallax|parallex|배경"),
    ("map-2d", r"maps?|minimaps?|지도"),
    ("tileset-2d", r"tile ?sets?|tiles?|tilemaps?|타일"),
    ("sprite-2d", r"sprites?|sprite ?sheets?|spritesheets?|charsets?|characters?|heroe?s?|enemies|monsters?|creatures?|baddies|스프라이트"),
])
REFINE_RE = {k: re.compile(r"(?<![a-z0-9])(?:%s)(?![a-z0-9])" % v) for k, v in REFINE_KEYWORDS.items()}
# 둘 이상 일치할 때 허용하는 조합 (그 외 조합은 모호하므로 other 유지)
REFINE_COMBO = {frozenset(["tileset-2d", "sprite-2d"]): "sprite-2d",   # 기존 '2D 스프라이트·타일셋' 매핑과 동일
                frozenset(["tileset-2d", "map-2d"]): "tileset-2d"}     # 'map tiles'는 타일셋
BOILER_RE = re.compile(r"파일 \d+개 \([^)]*\)|수집자 LICENSE-SOURCE\.txt 동봉\([^)]*\)|SHA-256 검증 업로드")
PREVIEW_NOTE_RE = re.compile(r"previews/[^\s;,)]+|[\w./-]*preview[\w-]*\.(?:png|jpe?g|gif|webp)", re.I)
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/([^/]+)/[^/]+/(.+)$")


def slugify(s):
    s = re.sub(r"[^a-z0-9가-힣]+", "-", s.lower()).strip("-")
    return s or "untitled"


def license_family(lic):
    l = lic.strip().lower()
    if l.startswith("cc0"): return "cc0"
    if l.startswith("cc-by"): return "cc-by"
    if l.startswith("mit"): return "mit"
    if l.startswith("gpl"): return "gpl"
    return "other"


def allowed_status(lic):
    """exact | annotated | not_allowed (allowed list: CC0, CC-BY, MIT, GPL 2.0/3.0)."""
    l = lic.strip()
    if re.fullmatch(r"CC0|CC-BY(?: [34]\.0)?|MIT|GPL [23]\.0", l): return "exact"
    if re.match(r"(?:CC0|CC-BY|MIT|GPL [23]\.0)\b", l): return "annotated"
    return "not_allowed"


def rel_from_url(u, repo):
    """repo-relative path from a raw/github URL of the same repo, else None."""
    m = re.match(r"^https://raw\.githubusercontent\.com/%s/%s/[^/]+/(.+)$" % (OWNER, re.escape(repo)), u) or \
        re.match(r"^https://github\.com/%s/%s/(?:raw|blob)/[^/]+/(.+)$" % (OWNER, re.escape(repo)), u) or \
        re.match(r"^https://github\.com/%s/%s/(releases/download/.+)$" % (OWNER, re.escape(repo)), u)
    return m.group(1) if m else None


def norm_path(p):
    p = p.strip().replace("\\", "/")
    while p.startswith("./") or p.startswith("/"): p = p[2:] if p.startswith("./") else p[1:]
    return p


def malformed_reason(f):
    r = []
    if not f.strip(): return ["빈 값"]
    if f != f.strip(): r.append("앞뒤 공백")
    if f.startswith("/") or f.startswith("./"): r.append("선행 / 또는 ./")
    if "\\" in f: r.append("역슬래시")
    if ".." in f.split("/"): r.append("상위 경로(..)")
    if "//" in f: r.append("중복 슬래시")
    if re.search(r"\s", f.strip()): r.append("내부 공백")
    if re.search(r"[?#%]", f): r.append("URL 예약문자(?#%)")
    if f.startswith("releases/download/") and not re.fullmatch(r"releases/download/[^/]+/[^/]+", f): r.append("릴리스 경로 형식 불일치")
    if not re.search(r"\.[A-Za-z0-9]{1,6}$", f): r.append("확장자 없음")
    return r


def refine_category(name, tags, notes):
    """type '2D'(모호) 행만: 키워드가 한 범주에만 일치할 때 그 범주, 아니면 'other'."""
    text = " ".join([name, " ".join(tags), BOILER_RE.sub(" ", notes)]).lower()
    hit = frozenset(k for k, rx in REFINE_RE.items() if rx.search(text))
    if len(hit) == 1: return next(iter(hit))
    return REFINE_COMBO.get(hit, "other")


def license_note(lic):
    """허용 라이선스로 시작하지만 부가 설명이 붙은 표기의 부가 설명 (없으면 None)."""
    if allowed_status(lic) != "annotated": return None
    m = LICENSE_BASE_RE.match(lic.strip())
    rest = lic.strip()[m.end():].lstrip(" /·,;").strip()
    if rest.startswith("(") and rest.endswith(")") and rest.count("(") == 1: rest = rest[1:-1].strip()
    return rest or None


def effect_kinds(name, tags, notes):
    text = " ".join([name, " ".join(tags), notes]).lower()
    return [k for k, rx in EFFECT_RE.items() if rx.search(text)]


def tags_list(raw):
    out, seen = [], set()
    for t in raw.split(","):
        t = t.strip().lower()
        if t and t not in seen: seen.add(t); out.append(t)
    return out


def build_assets(rows):
    assets, used = [], set()
    for r in rows:
        repo, name = r["repo"].strip(), r["name"].strip()
        base = f"{repo}/{slugify(name)}"
        aid, n = base, 1
        while aid in used:
            n += 1
            aid = f"{base}-{n}"
        used.add(aid)
        tags, seen = [], set()
        for t in r["tags"].split(","):
            t = t.strip().lower()
            if t and t not in seen: seen.add(t); tags.append(t)
        notes = r["notes"]
        lic, attr = r["license"], r["attribution"]
        fam = license_family(lic)
        # preview: CSV preview column (raw URL -> repo-relative path), else notes
        preview = None
        pv = r.get("preview", "").strip()
        if pv: preview = rel_from_url(pv, repo) or pv
        else:
            m = PREVIEW_NOTE_RE.search(notes)
            if m: preview = m.group(0)
        sample = r.get("sample", "").strip() or None
        split_raw = r.get("split", "").strip()
        split = [s.strip() for s in split_raw.split(";") if s.strip() and s.strip().upper() != "Y"]  # "Y" = flag only (parts part1..N in notes)
        path = rel_from_url(r["file"].strip(), repo) or norm_path(r["file"])
        a = OrderedDict()
        a["id"] = aid; a["name"] = name; a["repo"] = repo; a["file"] = r["file"]
        a["type"] = r["type"]; a["category"] = CATEGORY.get(r["type"].strip(), "other")
        if r["type"].strip() == "2D": a["category"] = refine_category(name, tags_list(r["tags"]), r["notes"])
        a["tags"] = tags; a["effect_kind"] = effect_kinds(name, tags, notes)
        a["author"] = r["author"]; a["source_url"] = r["source_url"]
        a["license"] = lic; a["license_note"] = license_note(lic); a["license_family"] = fam; a["attribution"] = attr
        al = attr.strip().lower()
        a["attribution_required"] = not (fam == "cc0" or al.startswith("optional") or al.startswith("불요") or NO_ATTR_RE.fullmatch(al))
        a["ai_generated"] = bool(AI_RE.search(notes) or AI_TEXT_RE.search(notes) or AI_TEXT_RE.search(lic))
        a["added"] = r["added"]; a["notes"] = notes; a["preview"] = preview
        a["download_path"] = path
        # download_url: pattern verified on real examples (see docs/index-report.md); split rows have no single file
        def url_of(p):
            return f"https://github.com/{OWNER}/{repo}/" + (quote(p) if p.startswith("releases/download/") else "raw/main/" + quote(p))
        ok_path = path and not malformed_reason(path)
        if not ok_path:
            a["download_url"], a["download_urls"] = None, []
        elif split and path.startswith("releases/download/"):
            d = path.rsplit("/", 1)[0]
            a["download_url"], a["download_urls"] = None, [url_of(d + "/" + p) for p in split]
        elif split:
            d = path.rsplit("/", 1)[0] + "/" if "/" in path else ""
            a["download_url"], a["download_urls"] = None, [url_of(d + p) for p in split]
        else:
            a["download_url"] = url_of(path); a["download_urls"] = [a["download_url"]]
        a["sample"] = sample
        a["multipart"] = bool(split_raw)
        a["split_parts"] = split
        assets.append(a)
    return assets


def md_table(headers, rows):
    esc = lambda x: str(x).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def counts_table(title_cols, counter, order=None, limit=None):
    items = ([(k, counter[k]) for k in order if k in counter] if order
             else sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))))
    if limit: items = items[:limit]
    return md_table(title_cols, items)


def examples(lst, n=10):
    return lst[:n]


def build_report(rows, header, assets, commit, link_check, existing_lc, size_info):
    N = len(assets)
    L = []
    w = L.append
    w("# 색인 점검 보고서\n")
    w("> `tools/build_index.py`가 자동 생성합니다. 수정하지 말고 스크립트를 다시 실행하세요.\n")
    w("## 1. 개요\n")
    w(f"- 원본: `catalog.csv@{commit}`")
    w(f"- 데이터 행 수: **{N}**")
    w(f"- CSV 헤더({len(header)}열): `{','.join(header)}`")
    extra = [h for h in header if h not in ("name,repo,file,type,tags,author,source_url,license,attribution,added,notes".split(","))]
    if extra: w(f"- 참고: 기본 11열 외 추가 열 {extra} 이 있어 색인에 반영함 (`preview`는 상대경로로 변환, `sample`, `split_parts` 추가).")
    w(f"- 파일 크기: " + ", ".join(f"`{k}` {v:,} bytes" for k, v in size_info.items()) if size_info else "- 파일 크기: (생성 후 산출)")
    w("")
    w("## 2. 집계\n")
    w("### 저장소(repo)별\n"); w(counts_table(["repo", "개수"], Counter(a["repo"] for a in assets))); w("")
    w("### 카테고리(category)별\n"); w(counts_table(["category", "개수"], Counter(a["category"] for a in assets))); w("")
    tcount = Counter((a["type"], a["category"]) for a in assets)
    w("### 원본 type → category 매핑\n")
    w(md_table(["type(원본)", "category", "개수"], sorted(((t, c, n) for (t, c), n in tcount.items()), key=lambda x: (-x[2], x[0])))); w("")
    two = [a for a in assets if a["type"].strip() == "2D"]
    w(f"### 원본 type `2D` 세분화 (정제 2차): 전 {len(two)}행 모두 other → 후\n")
    w("name/tags/notes(수집 boilerplate 제외)의 키워드가 한 범주에만 명확히 일치할 때만 지정하고, 일치가 없거나 둘 이상이면 other로 둠(예외: tileset+sprite → sprite-2d, tileset+map → tileset-2d). 원본 `type`은 바꾸지 않음. 키워드는 스크립트 `REFINE_KEYWORDS` 참고.\n")
    cb = Counter(a["category"] for a in two)
    w(md_table(["category", "전", "후"], [(c, len(two) if c == "other" else 0, cb.get(c, 0)) for c in CATEGORIES if cb.get(c) or c == "other"])); w("")
    w("### license_family별\n"); w(counts_table(["license_family", "개수"], Counter(a["license_family"] for a in assets))); w("")
    w("### 라이선스 문자열(license)별\n"); w(counts_table(["license", "개수"], Counter(a["license"] for a in assets))); w("")
    w("### 추가일(added) 일자별\n"); w(counts_table(["added", "개수"], Counter(a["added"] for a in assets), order=sorted(set(a["added"] for a in assets)))); w("")
    tags = Counter(t for a in assets for t in a["tags"])
    w("### 상위 태그 30\n"); w(counts_table(["tag", "개수"], tags, limit=30)); w("")
    ek = Counter(k for a in assets for k in a["effect_kind"])
    w("### effect_kind별 (키워드 일치 기준, 하나의 에셋이 여러 종류에 속할 수 있음)\n")
    w(md_table(["effect_kind", "개수"], [(k, ek.get(k, 0)) for k in EFFECT_KEYWORDS]))
    w(f"\n- effect_kind가 하나 이상인 에셋: {sum(1 for a in assets if a['effect_kind'])} / {N}\n")
    w(f"- attribution_required=true: {sum(a['attribution_required'] for a in assets)}, ai_generated=true: {sum(a['ai_generated'] for a in assets)}, preview 있음: {sum(1 for a in assets if a['preview'])}, 분할(split) 행: {sum(1 for a in assets if a['split_parts'])}\n")

    # ---- quality
    w("## 3. 품질 점검 (catalog.csv는 수정하지 않음)\n")
    # empty required
    emp = [(i + 2, f, r.get("name", "")) for i, r in enumerate(rows) for f in REQUIRED if not r.get(f, "").strip()]
    w(f"### 3.1 필수 필드가 빈 행: {len(emp)}건\n")
    if emp: w(md_table(["CSV 줄", "빈 필드", "name"], examples(emp, 30)))
    w("")
    # dup source_url
    su = {}
    for i, r in enumerate(rows):
        if r["source_url"].strip(): su.setdefault(r["source_url"].strip(), []).append(i)
    dsu = {u: v for u, v in su.items() if len(v) > 1}
    w(f"### 3.2 source_url 중복: {len(dsu)}개 URL에 걸쳐 {sum(len(v) for v in dsu.values())}행 (한 페이지에서 여러 팩을 만든 경우 포함)\n")
    if dsu:
        w(md_table(["source_url", "행 수", "id 예시"], [(u, len(v), ", ".join(assets[i]["id"] for i in v[:3])) for u, v in sorted(dsu.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:15]]))
    w("")
    nr = {}
    for i, r in enumerate(rows): nr.setdefault((r["name"].strip(), r["repo"].strip()), []).append(i)
    dnr = {k: v for k, v in nr.items() if len(v) > 1}
    w(f"### 3.3 (name, repo) 중복: {len(dnr)}쌍, {sum(len(v) for v in dnr.values())}행\n")
    if dnr: w(md_table(["name", "repo", "행 수", "file"], [(k[0], k[1], len(v), "; ".join(rows[i]["file"] for i in v[:3])) for k, v in sorted(dnr.items())[:15]]))
    w("")
    # licences
    st = {"exact": Counter(), "annotated": Counter(), "not_allowed": Counter()}
    for a in assets: st[allowed_status(a["license"])][a["license"]] += 1
    w("### 3.4 허용 목록(CC0, CC-BY, MIT, GPL 2.0/3.0) 밖의 라이선스 표기 — 값은 수정하지 않음\n")
    w(f"- 허용 목록과 정확히 일치: {sum(st['exact'].values())}행")
    w(f"- 허용 라이선스로 시작하지만 부가 설명이 붙은 표기: {sum(st['annotated'].values())}행 ({len(st['annotated'])}종)")
    w(f"- 허용 목록에 해당하지 않음: **{sum(st['not_allowed'].values())}행** ({len(st['not_allowed'])}종)\n")
    if st["annotated"]: w(md_table(["부가 설명이 붙은 license", "행 수"], sorted(st["annotated"].items(), key=lambda kv: (-kv[1], kv[0])))); w("")
    if st["not_allowed"]:
        w(md_table(["허용 목록 밖 license", "행 수", "id"], [(l, n, ", ".join(a["id"] for a in assets if a["license"] == l)) for l, n in sorted(st["not_allowed"].items())])); w("")
    # attribution
    need_empty = [a for a in assets if a["attribution_required"] and not a["attribution"].strip()]
    w(f"### 3.5 표기가 필요한데 attribution이 빈 행: {len(need_empty)}건\n")
    if need_empty: w(md_table(["id", "license"], [(a["id"], a["license"]) for a in need_empty[:30]]))
    w("")
    fam_opt = [a for a in assets if a["license_family"] in ("cc-by", "mit", "gpl") and a["attribution"].strip().lower().startswith("optional")]
    w(f"- 참고: license_family가 cc-by/mit/gpl인데 attribution이 `optional`로 시작하는 행: {len(fam_opt)}건 (규칙상 attribution_required=false 처리됨; 확인 필요)")
    if fam_opt: w("  - " + ", ".join(a["id"] for a in fam_opt[:10]) + (" …" if len(fam_opt) > 10 else ""))
    nonopt_cc0 = [a for a in assets if a["license_family"] == "cc0" and not a["attribution"].strip().lower().startswith("optional")]
    w(f"- 참고: license_family=cc0인데 attribution이 `optional`로 시작하지 않는 행: {len(nonopt_cc0)}건")
    fuyo = [a for a in assets if a["attribution"].strip().startswith("불요")]
    w(f"- 참고: attribution이 `불요`로 시작하거나 `없음`/`none`/`n/a`인 행: {sum(1 for a in assets if a['attribution'].strip().startswith('불요') or NO_ATTR_RE.fullmatch(a['attribution'].strip()))}건 — attribution_required=false 처리 (정제 2차 변경; 이전에는 `불요` 2행이 true였음: {', '.join(a['id'] for a in fuyo)})")
    ar_true_nonreq = [a for a in assets if a["attribution_required"] and a["license_family"] == "cc0"]
    w(f"- 참고: attribution_required=true인 행 {sum(a['attribution_required'] for a in assets)}건 (cc0인데 true: {len(ar_true_nonreq)}건)\n")
    # malformed file
    mal = [(i + 2, r["file"], ", ".join(malformed_reason(r["file"]))) for i, r in enumerate(rows) if malformed_reason(r["file"])]
    full_url = [a for a in assets if a["file"].startswith("http")]
    w(f"### 3.6 file 열 경로 형식 이상: {len(mal)}건\n")
    if mal: w(md_table(["CSV 줄", "file", "사유"], examples(mal, 30)))
    if full_url: w(f"- file 열이 저장소 상대경로가 아니라 전체 URL인 행 {len(full_url)}건: 색인의 download_path는 같은 저장소의 상대경로로 환산({', '.join(a['download_path'] for a in full_url[:3])}), 원본 file 값은 `file`에 그대로 유지.")
    rel = sum(1 for r in rows if r["file"].startswith("releases/download/"))
    w(f"- file 열 구성: 릴리스 자산 경로(`releases/download/<태그>/<파일>`) {rel}행, 저장소 트리 경로 {len(rows) - rel}행")
    spl = [a for a in assets if a["split_parts"]]
    flagY = [a for a in assets if a["multipart"] and not a["split_parts"]]
    w(f"- split 열 값이 `Y`(파트 파일명 미나열, 폴더 내 part1~N zip)인 행: {len(flagY)}건 — `multipart=true`, download_url은 file 열(part1) 기준.")
    w(f"- 파트 파일명이 나열된 분할 업로드(split 열) {len(spl)}행: file 열의 단일 파일명은 릴리스에 존재하지 않을 수 있고 실제 파일은 `split_parts`임 (예: `{spl[0]['id'] if spl else '-'}`). 이 행들의 `download_url`은 null, 대신 `download_urls`에 분할 파일 URL 목록을 둠.")
    nz = Counter(os.path.splitext(a["download_path"])[1].lower() for a in assets)
    w(f"- file 확장자 분포: " + ", ".join(f"{k or '(없음)'} {v}" for k, v in sorted(nz.items(), key=lambda kv: (-kv[1], kv[0]))) + "\n")
    # other
    cat_other = [a for a in assets if a["category"] == "other"]
    w(f"### 3.7 기타 관찰\n")
    w(f"- category가 `other`인 행: {len(cat_other)} (원본 type 분포: " + ", ".join(f"{t} {n}" for t, n in Counter(a['type'] for a in cat_other).most_common()) + ") — 원본 type이 `2D`처럼 모호하면 추측하지 않고 other로 둠.")
    neg = sum(1 for r in rows if "AI 생성" in r["notes"])
    ai_true = [(i + 2, a) for i, a in enumerate(assets) if a["ai_generated"]]
    ai_neg_true = [a["id"] for a in assets if re.search(r"AI 생성\s*(?:아님|여부)", a["notes"]) and not AI_RE.search(a["notes"]) and a["ai_generated"]]
    w(f"- notes에 `AI 생성` 문자열이 있는 행 {neg}건 중 `AI 생성 아님`/`AI 생성 여부 …` 형태의 부정·불명 표현을 제외한 행 {sum(1 for a in assets if AI_RE.search(a['notes']))}건, 그리고 license/notes에 `AI-generated`/`AI generated`/`AI 생성물`이 긍정 의미로 있는 행을 ai_generated=true로 판정: 총 {len(ai_true)}건.")
    w(f"- `AI 생성 아님`/`AI 생성 여부` 표기만 있는 행 중 true가 된 행: {len(ai_neg_true)}건")
    w("")
    w(md_table(["CSV 줄", "name", "repo", "근거"], [(ln, a["name"], a["repo"], ("notes `AI 생성`" if AI_RE.search(a["notes"]) else "license/notes `AI-generated`")) for ln, a in ai_true]))
    w("")
    ai_other = [a for a in assets if not a["ai_generated"] and re.search(r"\bAI\b|인공지능", a["notes"]) and not re.search(r"AI 생성", a["notes"])]
    w(f"- notes에 `AI`가 있으나 `AI 생성` 문구가 없어 false로 둔 행: {len(ai_other)}건" + (" (" + ", ".join(a['id'] for a in ai_other[:5]) + ")" if ai_other else ""))
    pv_missing = sum(1 for a in assets if a["preview"] is None)
    w(f"- preview가 없는 행: {pv_missing}건\n")

    # ---- link check
    w("## 4. 샘플 링크 점검 (전수 점검 아님, 표본)\n")
    if link_check:
        w(LC_START); w(link_check.strip()); w(LC_END)
    elif existing_lc:
        w(LC_START); w(existing_lc.strip()); w(LC_END)
    else:
        w(LC_START); w("미실행. `python3 tools/build_index.py --link-check <결과 JSON>` 으로 포함."); w(LC_END)
    w("")
    w("## 5. 색인 필드 규칙 메모\n")
    w("- `id`: `<repo>/<name 슬러그>`, 충돌 시 `-2`, `-3` 추가. 슬러그는 소문자 영숫자·한글 외 문자를 `-`로 치환.")
    w("- `category`: 원본 type(한국어) 표 기반 매핑(위 2장), 미지정은 other. `3D`는 model-3d로 매핑. `2D`는 아래 규칙으로 세분화.")
    w("- `tags`: 쉼표 분리, 소문자, 공백 제거, 한 에셋 내 중복 제거.")
    w("- `effect_kind`: name/tags/notes에 대한 단어 단위 키워드 일치만 사용(의미 추론 없음). 키워드 목록은 스크립트 `EFFECT_KEYWORDS` 참고.")
    w("- `license_family`: license 문자열의 접두사(cc0 / cc-by / mit / gpl / 그 외 other). 재해석하지 않음. license 값은 CSV 그대로.")
    w("- `attribution_required`: license_family=cc0 이거나 attribution이 `optional` 또는 `불요`로 시작하거나 `없음`/`none`/`n/a`와 같으면 false, 아니면 true.")
    w("- `ai_generated`: notes에 `AI 생성`이 있고 바로 뒤가 `아님`/`여부`가 아니거나, license/notes에 `AI-generated`/`AI generated`/`AI 생성물`이 긍정 의미로 있으면 true.")
    w("- `license_note`: license가 허용 라이선스(CC0, CC-BY, MIT, GPL 2.0/3.0)로 시작하지만 부가 설명이 붙은 경우 그 부가 설명(맨 앞 허용 라이선스 토큰 뒤 문자열, 전체가 괄호이면 괄호 제거), 그 외 null. `license` 값은 CSV 그대로.")
    w("- `category`(type `2D`만): 위 `2D` 세분화 규칙, 그 외 type은 매핑 표 그대로. 새 범주 `portrait` 추가.")
    w("- `preview`: CSV `preview` 열의 raw URL을 저장소 상대경로로 변환, 열이 비면 notes의 `previews/…`·`…preview….png` 경로, 없으면 null.")
    w("- `download_path`: file 열 정규화(선행 `/`, `./` 제거). `download_url`: 릴리스 경로는 `https://github.com/sigco3111/<repo>/releases/download/<태그>/<파일>`, 그 외는 `https://github.com/sigco3111/<repo>/raw/main/<경로>` (4장에서 실제 예시로 검증). 분할 행은 null이며 `download_urls`에 파트별 URL 목록(분할이 아닌 행은 `download_url` 1개짜리 목록). file 열이 같은 저장소의 전체 URL이면 상대경로로 환산(3.6 참고).")
    w("")
    w("## 6. 알려진 한계와 후속 정리\n")
    w("catalog.csv·license 값은 수정하지 않았습니다. 아래는 소유자의 후속 정리를 위한 목록입니다. CSV 줄 번호는 헤더를 1줄로 센 파일 줄 번호입니다.\n")
    w(f"### (a) 중복 행 (삭제하지 않음)\n")
    w(f"- (name, repo)가 같은 쌍 {len(dnr)}쌍({sum(len(v) for v in dnr.values())}행):\n")
    w(md_table(["name", "repo", "CSV 줄", "file"], [(k[0], k[1], ", ".join(str(i + 2) for i in v), "; ".join(rows[i]["file"] for i in v)) for k, v in sorted(dnr.items())])); w("")
    w(f"- source_url이 같은 값 {len(dsu)}개({sum(len(v) for v in dsu.values())}행):\n")
    w(md_table(["source_url", "CSV 줄", "name"], [(u, ", ".join(str(i + 2) for i in v), "; ".join(rows[i]["name"] for i in v)) for u, v in sorted(dsu.items())])); w("")
    w("### (b) file 값이 전체 URL인 행\n")
    w(md_table(["CSV 줄", "name", "file(원본)", "download_path(환산)"], [(i + 2, a["name"], a["file"], a["download_path"]) for i, a in enumerate(assets) if a["file"].startswith("http")])); w("")
    w("### (c) 허용 목록 밖의 자체 제작 라이선스 표기 (값 유지, 소유자 확인용)\n")
    na = [(i + 2, a) for i, a in enumerate(assets) if allowed_status(a["license"]) == "not_allowed"]
    w(f"license가 허용 목록(CC0, CC-BY, MIT, GPL 2.0/3.0) 밖의 맞춤 문구(`own work, AI-generated …`)인 행 {len(na)}건. 값은 그대로 두었고 `license_family`는 other, `ai_generated`는 true입니다.\n")
    w(md_table(["CSV 줄", "name", "repo", "attribution"], [(ln, a["name"], a["repo"], a["attribution"]) for ln, a in na])); w("")
    w("### (d) 분할 업로드 행 정책\n")
    sp = [a for a in assets if a["split_parts"]]
    w(f"- split 열에 파트 파일명이 나열된 행 {len(sp)}건: file 열의 단일 파일은 실제로 없을 수 있어 `download_url`은 null로 두고 `download_urls`에 파트별 URL을 둠(`multipart=true`, `split_parts` 포함). 사용자는 `download_url`이 null이면 `download_urls`를 사용해야 함.")
    sy = [a for a in assets if a["multipart"] and not a["split_parts"]]
    w(f"- split 열이 `Y`뿐인 행 {len(sy)}건: 파트 파일명 목록이 없어 `download_urls`는 file 열 기준 1개짜리 목록이며 `multipart=true`로만 표시(나머지 part2~N은 notes 참고).")
    w("- 분할이 아닌 행: `download_url` 1개 + `download_urls` 1개짜리 목록.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="catalog.csv")
    ap.add_argument("--commit", default=None, help="catalog.csv 원본 커밋 해시 (기본: git log -1 -- catalog.csv)")
    ap.add_argument("--link-check", default=None, help="샘플 링크 점검 결과 마크다운 파일 (4장에 삽입)")
    args = ap.parse_args()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(root, args.csv)
    commit = args.commit
    if not commit:
        try:
            commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", "catalog.csv"], cwd=root, capture_output=True, text=True, check=True).stdout.strip() or "unknown"
        except Exception:
            commit = "unknown"
    if not os.path.isfile(csv_path):
        print(f"오류: {args.csv} 파일이 없어 색인을 만들 수 없습니다. 기존 출력 파일은 변경하지 않았습니다.", file=sys.stderr)
        sys.exit(2)
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f)
        header = next(rd, [])
        rows = []
        for rec in rd:
            if not rec: continue
            rec = (rec + [""] * len(header))[:len(header)]
            rows.append(dict(zip(header, rec)))
    if len(rows) < MIN_ROWS:
        print(f"오류: {args.csv}의 데이터 행이 {len(rows)}개뿐입니다(최소 {MIN_ROWS}개 필요). 빈 색인을 만들지 않도록 중단합니다. 기존 출력 파일은 변경하지 않았습니다.", file=sys.stderr)
        sys.exit(2)
    for k in ("name,repo,file,type,tags,author,source_url,license,attribution,added,notes".split(",")):
        if k not in header: sys.exit(f"missing column: {k}")
    assets = build_assets(rows)
    doc = OrderedDict([("schema", 1), ("generated_from", f"catalog.csv@{commit}"), ("count", len(assets)), ("assets", assets)])
    pretty = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    out_json = os.path.join(root, "assets-index.json")
    with open(out_json, "w", encoding="utf-8", newline="\n") as f: f.write(pretty)
    size_info = OrderedDict([("assets-index.json", len(pretty.encode("utf-8")))])
    min_path = os.path.join(root, "assets-index.min.json")
    if size_info["assets-index.json"] > MIN_THRESHOLD:
        mini = json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n"
        with open(min_path, "w", encoding="utf-8", newline="\n") as f: f.write(mini)
        size_info["assets-index.min.json"] = len(mini.encode("utf-8"))
    elif os.path.exists(min_path):
        os.remove(min_path)
    lc = open(args.link_check, encoding="utf-8").read() if args.link_check else None
    rep_path = os.path.join(root, "docs", "index-report.md")
    existing = None
    if lc is None and os.path.exists(rep_path):
        t = open(rep_path, encoding="utf-8").read()
        if LC_START in t and LC_END in t: existing = t.split(LC_START, 1)[1].split(LC_END, 1)[0]
    os.makedirs(os.path.dirname(rep_path), exist_ok=True)
    with open(rep_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_report(rows, header, assets, commit, lc, existing, size_info))
    print(f"rows={len(rows)} assets={len(assets)} commit={commit} sizes={dict(size_info)}")


if __name__ == "__main__":
    main()
