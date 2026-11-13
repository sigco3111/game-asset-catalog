import csv
rows = [
 ("Rocket Thruster Effect Animations","assets-2d-pixel","rocket-thruster-effect-animations/rocket-thruster-effect-animations.zip","2D 이펙트","effect,thruster,animation,spritesheet","Reactorcore","https://opengameart.org/content/rocket-thruster-effect-animations","CC0","optional: Reactorcore (OpenGameArt)","2026-11-13","zip 약 74KB; 미리보기 preview.jpg"),
]
f = open("catalog.csv","a",newline="",encoding="utf-8")
csv.writer(f).writerows(rows)
f.close()
print("rows", sum(1 for _ in open("catalog.csv",encoding="utf-8")) - 1)
