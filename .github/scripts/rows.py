import csv
rows = [
("Low Poly Camping Assets","assets-3d-lowpoly","low-poly-camping-assets/low-poly-camping-assets.zip","3D 모델","camping,tent,prop,lowpoly,3d","Saraskau","https://opengameart.org/content/low-poly-camping-assets","CC0","optional: Saraskau (OpenGameArt)","2026-11-13","zip 1.4MB; 미리보기 preview.jpg"),
("Low-poly Retro PSX Skeleton","assets-3d-lowpoly","low-poly-retro-psx-skeleton/low-poly-retro-psx-skeleton.zip","3D 모델","skeleton,character,psx,retro,3d","LonesomeDucky","https://opengameart.org/content/low-poly-retro-psx-skeleton","CC-BY 4.0","required: LonesomeDucky (CC-BY 4.0)","2026-11-13","파일 1개(.blend); zip 약 903KB; 미리보기 preview.jpg"),
("Circular effect animations","assets-2d-pixel","circular-effect-animations/circular-effect-animations.zip","2D 이펙트","effect,magic,circle,spritesheet","Vircon32 (Carra)","https://opengameart.org/content/circular-effect-animations","CC-BY 4.0","required: Vircon32 (Carra) (CC-BY 4.0)","2026-11-13","zip 약 14KB; 원형 이펙트 스프라이트시트; 미리보기 preview.jpg"),
]
f = open("catalog.csv","a",newline="",encoding="utf-8")
csv.writer(f).writerows(rows)
f.close()
print("rows", sum(1 for _ in open("catalog.csv",encoding="utf-8")) - 1)
