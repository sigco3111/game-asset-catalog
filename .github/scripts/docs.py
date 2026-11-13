n = sum(1 for _ in open("catalog.csv",encoding="utf-8")) - 1
sec = "## 2026-11-13 A85 추가 (1팩, 총 %d팩)\n\n" % n
sec += "A85 라운드에서 OpenGameArt 2D 이펙트 1팩 Rocket Thruster Effect Animations(Reactorcore, CC0)를 수집했습니다. 중복은 카탈로그 저장소 코드 검색으로 확인했습니다.\n\n"
sec += "| 팩 | 라이선스 |\n| --- | --- |\n| Rocket Thruster Effect Animations | CC0 |\n\n"
sec += "종류: 2D 이펙트 1팩(assets-2d-pixel). 라이선스: CC0 1팩. AI 생성 명시 팩 없음. 팩당 1커밋(에셋: <팩 이름> 추가, 임시 워크플로 ingest-pack.yml 수동 실행). 용량: assets-3d-lowpoly 변경 없음, assets-2d-pixel 약 384MB(700MB 미만, 새 저장소 생성 없음). 색인(assets-index*.json)·위키·llms.txt는 직접 손대지 않고 Actions 자동 갱신에 맡김. '천하삼분 게임 에셋 56'은 수집 대상이 아님.\n"
rd = open("README.md",encoding="utf-8").read()
i = rd.find("## 2026-11-13 A84")
open("README.md","w",encoding="utf-8").write(rd[:i] + sec + rd[i:])
e = "- 2026-11-13 A85: Rocket Thruster Effect Animations (Reactorcore, CC0) (1팩, 총 %d팩; 2D 이펙트 1(assets-2d-pixel)). 임시 ingest-pack.yml로 팩 업로드, catalog-append.yml로 catalog.csv 행 1개·README 절·docs/log.md 추가. 색인은 Actions 자동 갱신." % n
lg = open("docs/log.md",encoding="utf-8").read().rstrip("\n")
open("docs/log.md","w",encoding="utf-8").write(lg + "\n" + e + "\n")
print("total", n)
