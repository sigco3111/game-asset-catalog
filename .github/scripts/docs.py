n = sum(1 for _ in open("catalog.csv",encoding="utf-8")) - 1
sec = "## 2026-11-13 A85 추가 (3팩, 총 %d팩)\n\n" % n
sec += "A85 라운드에서 OpenGameArt 3D 최신순의 3D 2팩 Tool Pack 1\u00b7Toolbox\u00b7Rocket Thruster" 
sec += "을 수집했습니다. 중복은 카탈로그 저장소 코드 검색으로 확인했습니다(Minigolf Kit\u00b7Plasma Electric Effect Animations\u00b7Gun Muzzle Flash Effects는 이미 수록되어 제외).\n\n"
sec += "| 팩 | 라이선스 |\n| --- | --- |\n| Tool Pack 1 | CC0 |\n| Toolbox | CC0 |\n| Rocket Thruster Effect Animations | CC0 |\n\n"
sec += "종류: 3D 2팩(assets-3d-lowpoly), 2D 이펙트 1팩(assets-2d-pixel). 라이선스: CC0 3팩. AI 생성 명시 팩 없음. 팩당 1커밋(에셋: <팩 이름> 추가, 임시 워크플로 ingest-pack.yml 수동 실행). 용량: assets-3d-lowpoly 약 657MB, assets-2d-pixel 약 383MB(700MB 미만, 새 저장소 생성 없음). 색인(assets-index*.json)\u00b7위키\u00b7llms.txt는 직접 손대지 않고 Actions 자동 갱신에 맡김. '\ucc9c\ud558\uc0bc\ubd84 \uac8c\uc784 \uc5d0\uc14b 56'\uc740 \uc218\uc9d1 \ub300\uc0c1\uc774 \uc544\ub2d8.\n"
rd = open("README.md",encoding="utf-8").read()
i = rd.find("## 2026-11-13 A84")
open("README.md","w",encoding="utf-8").write(rd[:i] + sec + rd[i:])
e = "- 2026-11-13 A85: Tool Pack 1 (LonesomeDucky, CC0), Toolbox (LonesomeDucky, CC0), Rocket Thruster Effect Animations (Reactorcore, CC0) (3팩, 총 %d팩; 3D 모델 2(assets-3d-lowpoly), 2D 이펙트 1(assets-2d-pixel)). 임시 ingest-pack.yml로 팩 업로드, catalog-append.yml로 catalog.csv 행 3개\u00b7README 절\u00b7docs/log.md 추가. 색인은 Actions 자동 갱신." % n
lg = open("docs/log.md",encoding="utf-8").read().rstrip("\n")
open("docs/log.md","w",encoding="utf-8").write(lg + "\n" + e + "\n")
print("total", n)
