import csv
rows = [
 ("Tool Pack 1","assets-3d-lowpoly","tool-pack-1/tool-pack-1.zip","3D 모델","tool,prop,lowpoly,3d","LonesomeDucky","https://opengameart.org/content/tool-pack-1","CC0","optional: LonesomeDucky (OpenGameArt)","2026-11-13","zip 17.8MB; 미리보기 preview.jpg"),
 ("Toolbox","assets-3d-lowpoly","toolbox/toolbox.zip","3D 모델","tool,prop,lowpoly,3d","LonesomeDucky","https://opengameart.org/content/toolbox-0","CC0","optional: LonesomeDucky (OpenGameArt)","2026-11-13","파일 1개(.blend); zip 약 13MB; 미리보기 preview.jpg"),
 ("Rocket Thruster Effect Animations","assets-2d-pixel","rocket-thruster-effect-animations/rocket-thruster-effect-animations.zip","2D 이펙트","effect,thruster,animation,spritesheet","Reactorcore","https://opengameart.org/content/rocket-thruster-effect-animations","CC0","optional: Reactorcore (OpenGameArt)","2026-11-13","zip 약 74KB; 미리보기 preview.jpg"),
]
f = open("catalog.csv","a",newline="",encoding="utf-8")
csv.writer(f).writerows(rows)
f.close()
print("rows", sum(1 for _ in open("catalog.csv",encoding="utf-8")) - 1)
