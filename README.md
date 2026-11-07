# game-asset-catalog

재사용 가능한 게임 에셋 라이브러리의 중앙 카탈로그입니다.
실제 파일은 유형별 저장소에 두고, 여기에 모든 에셋의 출처·라이선스·작가·장르 태그를 기록합니다.

## 저장소 구성

| 저장소 | 내용 | 수록 |
| --- | --- | --- |
| [assets-2d-pixel](https://github.com/sigco3111/assets-2d-pixel) | 2D 픽셀 스프라이트, 타일셋, 텍스처 | 551팩 |
| [assets-3d-lowpoly](https://github.com/sigco3111/assets-3d-lowpoly) | 3D 로우폴리 모델·애니메이션 캐릭터 (GLB·OBJ) | 439팩 (대부분 릴리스 첨부) |
| [assets-3d-quaternius](https://github.com/sigco3111/assets-3d-quaternius) | Quaternius의 CC0 로우폴리 3D 팩 모음 (A7부터 신규 Quaternius 팩 전용, 폴더별 zip 분할) | 0팩 (신규) |
| [assets-ui-icons](https://github.com/sigco3111/assets-ui-icons) | UI 키트, 아이콘, 폰트 | 220팩 |
| [assets-audio](https://github.com/sigco3111/assets-audio) | 효과음, 배경음악, 음성 (OGG) | 412팩 |
| [assets-2d-portraits](https://github.com/sigco3111/assets-2d-portraits) | 삼국지 수묵담채 초상화 (자체 제작, 조건 없이 사용 가능) | 3팩 |

각 저장소 README에 팩별 미리보기 이미지와 내용·형식·개수가 있습니다.

2026-10-28에 3D 저장소에 잘못 분류돼 있던 7팩(Brick Pack, Modular Characters, Prototype Textures, Racing Pack, Robot Pack, Toon Characters, Voxel Pack)을 실제 파일 내용(3D 모델 파일 없음)에 따라 2D 저장소로 옮겼습니다. 같은 날 Sci-Fi Essentials Kit 4K Textures도 실제 내용이 PNG 36종뿐이라 같은 원칙으로 2D 저장소(v6.0)로 옮겼습니다(3D v6.0 링크는 동일 바이트로 유지).

## 수집 원칙

- 원본 파일 재배포가 명시적으로 허용된 라이선스(CC0, CC-BY)만 수록합니다.
- CC-BY 팩은 귀속 문구를 카탈로그에 함께 기록합니다.
- CC-BY-SA·GPL·CC-BY-NC, 개별 조건이 확인되지 않은 자료는 수록하지 않습니다.
- Unity Asset Store·Epic(Fab) 등 스토어 구매 에셋은 원본 재배포가 금지되는 경우가 많아 올리지 않습니다.
- 각 zip 안에 제작자 배포 원본 License.txt를 그대로 포함합니다. 원본에 라이선스 파일이 없는 팩은 원본 배포 페이지의 라이선스 표기를 근거로 수집자가 작성한 LICENSE-SOURCE.txt를 동봉하며, 원본 라이선스 파일과 구분합니다.

## 출처 검증 상태

- Kenney 팩(108개): kenney.nl의 CC0 배포 팩입니다. 원본 배포 페이지의 라이선스 조건과 각 팩 동봉 License.txt를 확인했습니다. 파일 바이트는 공식 미러 github.com/ETdoFresh/kenney.nl 에서 확보했으며, 공식 사이트 원본과 바이트 대조는 하지 않았습니다(kenney.nl 직접 다운로드 차단).
- KayKit 팩(10개): Kay Lousberg의 공식 GitHub 저장소(KayKit-Game-Assets) 원본 바이트를 그대로 보존했고, 동봉 LICENSE.txt(CC0)를 확인했습니다.
- Quaternius 팩(12개): quaternius.com 공식 배포 Google Drive 원본 바이트를 보존했고, 각 팩 페이지의 CC0 조건을 확인했습니다(Animated Zombie·Cute Monsters는 라이선스 미동봉으로 LICENSE-SOURCE.txt에 근거 기록).
- 저장소에 올라간 파일은 업로드 후 원격 다운로드 SHA-256을 로컬과 대조해 일치를 확인했습니다.

## 추가 확장 (총 159팩)

- 3D 16팩 추가: 식재료, 작물, 주택 실내, 모듈식 던전·SF 환경·도로, 자연, 터렛, 무기, NPC, 물고기, 선박. 실제 OBJ 파일 860개 및 대응 FBX·BLEND를 확인했습니다(형식별 중복 합산 아님). Food·Crops 사이 Coconut_Half OBJ 1개는 원본 공통 파일입니다.
- 오디오 4팩 추가: 효과음 390종, 총 720개 형식별 오디오 파일 디코딩 검사 완료.
- UI 1팩 추가: Game-icons.net SVG 4,180개. CC BY 3.0 귀속 필수이며, 원본 license.txt에 CC0로 표시된 2명 제작자 폴더는 예외입니다.
- Quaternius 신규 16팩은 제작자의 OpenGameArt 배포 페이지에서 받았습니다. 기존 Drive 배포본과 바이트 대조를 했다는 뜻은 아닙니다. 동봉 원본 라이선스가 없는 팩은 출처 페이지의 CC0 표기를 근거로 수집자 LICENSE-SOURCE.txt를 추가했습니다.
- 새 파일 모두 원격 다운로드 SHA-256 확인. Low Poly Nature Pack은 .z01+.zip 2개 분할이며 원격 파일 재결합과 내용 일치 검사를 마쳤습니다. README의 재결합 명령을 따르세요.
- v6.0(2026-10-28): Quaternius 제작자 OpenGameArt 배포 7팩 추가 — Fantasy Props MegaKit(모델 94종), Medieval Village MegaKit(176종), Modular Sci-Fi MegaKit(191종), Stylized Nature MegaKit(68종), Sci-Fi Essentials Kit 모델(37종), Universal Animation Library 1·2. 모두 11MB 분할 zip이며 49개 파일 원격 SHA-256 일치 확인. Sci-Fi Essentials 4K 텍스처(PNG 36종)는 2D 저장소 v6.0에 수록.

## 2026-11-07 A1 추가 (6팩, 총 1535팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Weapon Pack](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/weapon-pack) | assets-3d-lowpoly | Kenney | CC0 | 무기 OBJ 38종 + 스프라이트 |
| [Medieval Town Base](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/medieval-town-base) | assets-3d-lowpoly | Kenney | CC0 | 중세 마을 OBJ 67종 |
| [Playing Card Assets (52-cards deck + Chips)](https://github.com/sigco3111/assets-2d-pixel/tree/main/poker-cards-chips-2d) | assets-2d-pixel | mehrasaur | CC0 | 포커 카드 52장 + 칩 |
| [Bridge-Sized Playing Card Deck](https://github.com/sigco3111/assets-2d-pixel/tree/main/bridge-sized-playing-cards) | assets-2d-pixel | Mesmedir | CC0 | 브리지 크기 카드 덱 PNG |
| [Hex Board Game Tiles](https://github.com/sigco3111/assets-2d-pixel/tree/main/hex-board-game-tiles) | assets-2d-pixel | qubodup | CC0 | 육각 보드게임 타일 SVG |
| [Medieval fair [Loop]](https://github.com/sigco3111/assets-audio/tree/main/medieval-fair-loop) | assets-audio | Woli34 | CC0 | 중세 장터 음악 루프 OGG |

## 2026-11-07 A2 추가 (6팩, 총 1541팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [RPG Fantasy Icon Set](https://github.com/sigco3111/assets-ui-icons/tree/main/rpg-fantasy-icon-set) | assets-ui-icons | DezrasDragons | CC0 | RPG 장비 아이콘 PNG 9종 |
| [Tile based strategy game sprites](https://github.com/sigco3111/assets-2d-pixel/tree/main/tile-based-strategy-game-sprites) | assets-2d-pixel | danthedev | CC0 | 격자 전략 게임 스프라이트시트 |
| [180+ Seamless Hex Tiles](https://github.com/sigco3111/assets-2d-pixel/tree/main/180-seamless-hex-tiles) | assets-2d-pixel | Screaming Brain Studios | CC0 | 이음새 없는 육각 타일 PNG·TSX (원본 License.txt) |
| [Playing Cards (Vector & PNG)](https://github.com/sigco3111/assets-2d-pixel/tree/main/playing-cards-vector-png) | assets-2d-pixel | Byron Knoll | CC0 | SVG·PNG 카드 덱 |
| [Rpg Loop 1](https://github.com/sigco3111/assets-audio/tree/main/rpg-loop-1) | assets-audio | Tozan | CC0 | RPG 현악 루프 OGG·MIDI |
| [Medieval: Battle](https://github.com/sigco3111/assets-audio/tree/main/medieval-battle) | assets-audio | RandomMind | CC0 | 중세 전투 음악 MP3 (WAV는 25MB 업로드 제한으로 제외) |

새 팩은 `팩이름/` 폴더(zip, pack.md, 미리보기)로 올립니다. 업로드 도구가 파일명을 소문자로 바꿔 PACK.md는 `pack.md`로 저장됩니다. OGA 팩은 원본에 라이선스 파일이 없어 수집자가 쓴 LICENSE-SOURCE.txt를 zip에 넣었습니다.

## 2026-11-07 A3 추가 (6팩, 총 1547팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [UI Sounds](https://github.com/sigco3111/assets-audio/tree/main/ui-sounds) | assets-audio | SIEMPRERETORNA | CC0 | UI 효과음 WAV 11개 (Error·Accept·Notification 등) |
| [8-Bit Victory Loop](https://github.com/sigco3111/assets-audio/tree/main/8bit-victory-loop) | assets-audio | josepharaoh99 | CC0 | 8비트 승리 루프 OGG + FamiTracker·NSF |
| [Full Dice Set](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/full-dice-set) | assets-3d-lowpoly | rehcub | CC0 | D4~D20 주사위 로우폴리 OBJ + 텍스처 |
| [Parchment Textures](https://github.com/sigco3111/assets-2d-pixel/tree/main/parchment-textures) | assets-2d-pixel | Charlie | CC0 | 양피지 텍스처 JPG 2장 |
| [Cybericons](https://github.com/sigco3111/assets-ui-icons/tree/main/cybericons) | assets-ui-icons | knekko | CC0 | 사이버펑크 32x32 아이콘 PNG 32종 |
| [Tiny Creatures](https://github.com/sigco3111/assets-2d-pixel/tree/main/tiny-creatures) | assets-2d-pixel | Clint Bellanger | CC0 | 16x16 몬스터·동물 180종 (원본 License.txt) |

종류: 효과음·음악·3D 보드게임 소품·텍스처·아이콘·픽셀 캐릭터. 텍스처는 기존 방식대로 assets-2d-pixel에 수록했습니다. 모두 OGA 페이지의 CC0 표기를 직접 확인했습니다.

실제 팩 수(catalog.csv 기준): 2D 529 · 3D 429 · UI/아이콘 197 · 오디오 390 · 기타 3.

## 2026-11-07 A4 추가 (8팩, 총 1555팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Hi-Tech Button Sound Pack I (Non Themed)](https://github.com/sigco3111/assets-audio/tree/main/hi-tech-button-sound-pack-i-non-themed) | assets-audio | Circlerun | CC0 | 하이테크 UI 버튼·창 효과음 15종 (WAV·MP3, 원본 RAR 그대로) |
| [Click UI Menu SFX (yes/no/select)](https://github.com/sigco3111/assets-audio/tree/main/click-ui-menu-sfx-yes-no-select) | assets-audio | qubodup | CC0 | 클릭·긍정·부정 UI 효과음 WAV 8개 (7z→zip 재압축) |
| [Accept/ Decline UI Menu](https://github.com/sigco3111/assets-audio/tree/main/accept-decline-ui-menu) | assets-audio | KarateStudios | CC0 | 수락/거절 UI 효과음 FLAC 2개 |
| [Menu Loop](https://github.com/sigco3111/assets-audio/tree/main/menu-loop) | assets-audio | Akikazer | CC0 | 메뉴 음악 루프 WAV (2.6MB) |
| [5 wood textures](https://github.com/sigco3111/assets-2d-pixel/tree/main/5-wood-textures) | assets-2d-pixel | Luke.RUSTLTD | CC0 | 타일형 나무 텍스처 PNG 5장 |
| [CC0 Book Icons](https://github.com/sigco3111/assets-ui-icons/tree/main/cc0-book-icons) | assets-ui-icons | AntumDeluge | CC0 | 32x32 책 아이콘 모음 (출처별 CC0) |
| [Deep Night - 8x8 Platformer Assets](https://github.com/sigco3111/assets-2d-pixel/tree/main/deep-night-8x8-platformer-assets) | assets-2d-pixel | VEXED | CC0 | 8x8 플랫포머 타일·적·플레이어 |
| [Paper Pixels - 8x8 Platformer Assets](https://github.com/sigco3111/assets-2d-pixel/tree/main/paper-pixels-8x8-platformer-assets) | assets-2d-pixel | VEXED | CC0 | 8x8 플랫포머 타일·적·플레이어 (3 팔레트) |

종류: UI·메뉴 효과음 4팩, 텍스처 1, 아이콘 1, 8x8 플랫포머 타일셋 2. 모두 OGA 페이지의 라이선스 항목(CC0)을 직접 확인했습니다. 대용량 팩은 이번에 추가하지 않았습니다. 새 저장소 없음(저장소 용량 모두 약 120MB 이하).

실제 팩 수(catalog.csv 기준): 2D 533 · 3D 439 · UI/아이콘 198 · 오디오 395 · 기타 3.

## 카탈로그

전체 목록은 [catalog.csv](catalog.csv)를 참고하세요. 장르는 tags 열로 검색합니다 (fantasy, rpg, platformer, towerdefense, shooter, ui, audio 등).
에셋이 늘어나면 장르별 저장소로 다시 나눌 수 있습니다.

## 에셋 도서관 사이트

https://sigco3111.github.io/game-asset-catalog/

이 저장소의 `catalog.csv`를 읽어 팩을 이미지로 둘러보고 검색하는 사이트입니다(현재 1625팩). 팩 단위 검색이 기본이며, 초상화 탭에서는 팩 안의 인물을 이름으로 검색할 수 있습니다: 확정 한국어명과 한자명으로 찾고, 한국어명이 확정되지 않은 204명은 '미정'으로 표시되어 '미정' 검색으로 모아볼 수 있습니다. 결과는 60명씩 표시되고 '더 보기'로 전체를 탐색하며, 인물별 썸네일 미리보기와 개별 원본 다운로드(릴리스 개별 에셋)를 제공합니다. 사이트 파일은 `index.html`, `style.css`, `app.js`입니다.

### 새 팩을 추가할 때

사이트는 `catalog.csv`에 기록된 팩만 보여줍니다. 새 팩을 올린 뒤 `catalog.csv`에 한 줄을 추가하면 저장소 변경 후 약 1분 안에 사이트에 반영됩니다(2026-10-28 측정).

| 열 | 용도 |
| --- | --- |
| name, repo, file, type, tags, author, source_url, license, attribution, added, notes | 기존 열 그대로 |
| preview | 미리보기 이미지 주소. 비어 있으면 사이트에 "확인 필요"로 표시됩니다(오디오 제외) |
| sample | 오디오 샘플(.ogg) 주소 |
| split | 분할 ZIP이면 `Y` |

`name`, `file`, `license`, `source_url`, `preview`가 비어 있으면 사이트가 해당 팩에 "확인 필요"를 표시합니다. 썸네일과 메타데이터는 자동 생성되지 않으므로 수집할 때 함께 기록해야 합니다.

## 2026-11-07 A5 추가 (6팩, 총 1561팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Cube World Kit (Aug 2023)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/cube-world-kit) | assets-3d-lowpoly | Quaternius | CC0 | 큐브풍 모델 108종, 25.8MB 단일 zip |
| [Zombie Apocalypse Kit (March 2024)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/zombie-apocalypse-kit) | assets-3d-lowpoly | Quaternius | CC0 | 모델 60종, 40.9MB를 zip 3개(part1~3)로 분할 |
| [Human Token](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/human-token) | assets-3d-lowpoly | Clint Bellanger | CC0 | 사람 모양 토큰 .blend |
| [Token Poker](https://github.com/sigco3111/assets-2d-pixel/tree/main/token-poker) | assets-2d-pixel | Guyome41 | CC0 | 포커 토큰 PNG·SVG |
| [Rpg Sound Effect Pack](https://github.com/sigco3111/assets-audio/tree/main/rpg-sound-effect-pack) | assets-audio | Delta12 Studio | CC0 | RPG 효과음 OGG 12개 |
| [FREE ASSET PACK - MISC 1](https://github.com/sigco3111/assets-2d-pixel/tree/main/free-asset-pack-misc-1) | assets-2d-pixel | CamTatz | CC0 | 2D 벡터·아이템 PNG 160개 |

Quaternius 두 팩은 공식 페이지의 Google Drive 폴더(전체 다운로드)에서 받은 원본이며, 팩 페이지의 CC0 표기를 직접 확인했습니다. OGA 4팩은 각 페이지의 라이선스 항목(CC0)을 다시 확인했습니다. CC-BY 팩은 없습니다. 새 저장소는 만들지 않았습니다(각 저장소 용량 700MB 미만).

## 2026-11-07 A6 추가 (7팩, 총 1568팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Ultimate Fantasy RTS (August 2022)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/ultimate-fantasy-rts) | assets-3d-lowpoly | Quaternius | CC0 | RTS용 건물(시대·단계별)·자연·자원 모델 128종, 84MB를 zip 5개로 분할 |
| [Cyberpunk Game Kit (July 2022)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/cyberpunk-game-kit) | assets-3d-lowpoly | Quaternius | CC0 | 캐릭터·적·플랫폼·터렛 등 71종, zip 2개 |
| [Ultimate Nature Pack (June 2019)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/ultimate-nature-pack) | assets-3d-lowpoly | Quaternius | CC0 | 자연 모델 150종, zip 2개 |
| [Ultimate Modular Ruins Pack (August 2021)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/ultimate-modular-ruins-pack) | assets-3d-lowpoly | Quaternius | CC0 | 모듈식 폐허·던전 90종, zip 2개 |
| [Ultimate Monsters (October 2022)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/ultimate-monsters) | assets-3d-lowpoly | Quaternius | CC0 | 애니메이션 몬스터 50종, zip 3개 |
| [Ultimate Modular Women Pack (February 2022)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/ultimate-modular-women-pack) | assets-3d-lowpoly | Quaternius | CC0 | 여성 캐릭터 10종(부품 조합·애니메이션 24종), zip 3개 |
| [Sushi Restaurant Kit (May 2023)](https://github.com/sigco3111/assets-3d-lowpoly/tree/main/sushi-restaurant-kit) | assets-3d-lowpoly | Quaternius | CC0 | 요리 게임용 식재료·캐릭터·실내 108종, zip 3개; 원본 라이선스 파일 없어 LICENSE-SOURCE.txt 동봉 |

Quaternius 7팩 모두 공식 팩 페이지의 License 항목(CC0)을 직접 확인했고, 공식 Google Drive 폴더 '전체 다운로드' 원본을 폴더 단위로 나눠 올렸습니다(웹 업로드 한도 때문에 zip당 24MB 이하, 내용 변경 없음; 같은 위치에 풀면 복원). 한 번에 커밋할 수 있는 용량 한계로 큰 팩은 커밋을 여러 번에 나눴습니다. Ultimate Fantasy RTS·Ultimate Monsters·Ultimate Modular Women의 원본 License.txt 머리글은 다른 팩 이름으로 되어 있으나 본문은 CC0 1.0이며 원본 그대로 보존했습니다. CC-BY 팩은 없습니다. 3D 저장소는 약 450MB로 700MB 미만이라 새 저장소는 만들지 않았습니다.

## 2026-11-07 A7 (저장소 정리)

- 새 저장소 [assets-3d-quaternius](https://github.com/sigco3111/assets-3d-quaternius)를 만들었습니다. A7부터 새 Quaternius CC0 팩은 이 저장소에 올리고, catalog.csv의 repo 열에 `assets-3d-quaternius`로 적습니다. A6까지의 Quaternius 팩은 assets-3d-lowpoly에 그대로 두며(이동·삭제 없음) 해당 저장소 README에도 같은 안내를 넣었습니다.
- 이번 실행에서는 Google Drive 배포본의 다운로드 할당량 초과로 신규 팩을 추가하지 못했습니다(총 팩 수 변동 없음).

## 2026-11-07 A8 추가 (10팩, 총 1578팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Short Loops Background Music Pack](https://github.com/sigco3111/assets-audio/tree/main/short-loops-background-music-pack) | assets-audio | hernandack | CC0 | OGG 완전 반복 BGM 4곡 |
| [7DaysofVGM Free Asset Pack](https://github.com/sigco3111/assets-audio/tree/main/7daysofvgm-free-asset-pack) | assets-audio | LemonheadVGM | CC0 | 타이틀·메뉴·전투·보스전 테마 OGG 4곡 |
| [Versatile 255-Tile Pixel Art Pack](https://github.com/sigco3111/assets-2d-pixel/tree/main/versatile-255-tile-pixel-art-pack) | assets-2d-pixel | wareya | CC0 | 16x16 타일 255종(탑다운·횡스크롤 겸용) |
| [Top Down Dungeon Pack](https://github.com/sigco3111/assets-2d-pixel/tree/main/top-down-dungeon-pack) | assets-2d-pixel | Screaming Brain Studios | CC0 | 64x64 탑다운 던전 타일 2,256종(마젠타 배경·오토타일 세트) |
| [Bountiful Bits 10x10 Top-Down RPG Tiles](https://github.com/sigco3111/assets-2d-pixel/tree/main/bountiful-bits-10x10-top-down-rpg-tiles) | assets-2d-pixel | VEXED | CC0 | 10x10 1비트 탑다운 RPG 타일(9색) |
| [Bit Bonanza 10x10 Top-Down RPG Tiles](https://github.com/sigco3111/assets-2d-pixel/tree/main/bit-bonanza-10x10-top-down-rpg-tiles) | assets-2d-pixel | VEXED | CC0 | 10x10 탑다운 RPG 타일 |
| [Chess pieces and a board](https://github.com/sigco3111/assets-2d-pixel/tree/main/chess-pieces-and-a-board) | assets-2d-pixel | Drummyfish | CC0 | 체스 판+말 3세트(52x52) |
| [Ultimate Particle Pack For Casual Fight Game](https://github.com/sigco3111/assets-2d-pixel/tree/main/ultimate-particle-pack-for-casual-fight-game) | assets-2d-pixel | RandomUser | CC0 | 격투 게임용 파티클·이펙트 스프라이트 |
| [Quick GUI Pack](https://github.com/sigco3111/assets-ui-icons/tree/main/quick-gui-pack) | assets-ui-icons | electronsandsuch | CC0 | GUI 요소 PNG(화살표·버튼 등)+Krita 원본 |
| [8x8 Icons and Symbols](https://github.com/sigco3111/assets-ui-icons/tree/main/8x8-icons-and-symbols) | assets-ui-icons | DezrasDragons | CC0 | 8x8 장비 아이콘·기호 스프라이트시트 PNG 2장 |

종류: BGM·음악 2팩, 탑다운·플랫포머 타일셋 4, 보드게임 1, 파티클 1, UI 1, 아이콘 1. Quaternius·Google Drive가 아닌 OpenGameArt.org의 CC0 팩만 받았고, 모든 팩의 OGA 페이지 라이선스 항목(CC0)을 직접 확인했습니다. Top Down Dungeon Pack은 제작자 원본 License.txt(CC0)가 있고, 나머지는 페이지의 라이선스 표기로 LICENSE-SOURCE.txt를 작성했습니다. CC-BY 팩은 없습니다. 대용량(25MB 초과) 팩과 3D 팩은 추가하지 않았고 새 저장소는 만들지 않았습니다.

## 2026-11-07 A9 추가 (7팩, 총 1585팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Free VFX asset pack](https://github.com/sigco3111/assets-2d-pixel/tree/main/free-vfx-asset-pack) | assets-2d-pixel | CodeManu | CC0 | 픽셀 이펙트 22종(30·60fps PNG·GIF·.smp, 파일 2,150개); 94.6MB를 zip 6개로 분할 |
| [Fantasy World Map](https://github.com/sigco3111/assets-2d-pixel/tree/main/fantasy-world-map) | assets-2d-pixel | Belohlavek | CC0 | 무작위 생성 판타지 월드맵 GIF(4000x2000) |
| [Level & Battle Theme (Loops) - MP3](https://github.com/sigco3111/assets-audio/tree/main/level-battle-theme-loops) | assets-audio | Trex0n | CC0 | 레트로 신스 레벨·보스전 테마 MP3 2개(WAV 제외) |
| [Glizzy Elf Forest [RPG MUSIC PACK]](https://github.com/sigco3111/assets-audio/tree/main/glizzy-elf-forest-rpg-music-pack) | assets-audio | Zane Little Music | CC0 | RPG 음악 WAV 5곡; zip 2개로 분할 |
| [Assets: UI Casual Free #5 [Buttons, Bars, Panels]](https://github.com/sigco3111/assets-ui-icons/tree/main/assets-ui-casual-free-5-buttons-bars-panels) | assets-ui-icons | Wenrexa | CC0 | 캐주얼 UI PNG(3색 각 239종) |
| [Nat's 8x8 UI Pack (Over 50 UI Elements)](https://github.com/sigco3111/assets-ui-icons/tree/main/nats-8x8-ui-pack-over-50-ui-elements) | assets-ui-icons | nateonus | CC0 | 8x8 픽셀 UI 요소 50여 종 |
| [Icons for fantasy game (units and skills)](https://github.com/sigco3111/assets-ui-icons/tree/main/icons-for-fantasy-game-units-and-skills) | assets-ui-icons | voltz3666 | CC0 | 64x64 판타지 아이콘(진영·도시·유닛·스킬) |

종류: 이펙트 1팩, 일러스트(맵) 1, 음악 2, UI 키트 2, 아이콘 1. OpenGameArt.org의 CC0 팩만 받았고, 각 팩 페이지의 라이선스 항목(CC0)과 제출자(Author) 표기를 직접 확인했습니다. 원본 License.txt가 있는 팩은 없어 모두 페이지의 라이선스 표기로 LICENSE-SOURCE.txt를 작성했습니다(Nat's 8x8은 zip 내 readme.txt에도 CC0 명시). CC-BY 팩은 없습니다. 25MB 초과 팩(Free VFX 94.6MB, Glizzy Elf Forest 44.4MB)은 파일 내용을 바꾸지 않고 zip을 나눠 여러 커밋으로 올렸습니다. Level & Battle Theme은 WAV(30.7MB)가 한도를 넘어 MP3만 수록했고, 작가가 크레딧(Cal McEachern)을 요청했으나 필수는 아닙니다. 'RPG UI Elements CC0'는 개별 에셋이 아니라 컬렉션 페이지(라이선스 항목 없음)라 제외했습니다. 새 저장소는 만들지 않았습니다.

실제 팩 수(catalog.csv 기준): 2D 541 · 3D 439 · UI/아이콘 203 · 오디오 399 · 기타 3.

## 2026-11-07 A10 추가 (10팩, 총 1595팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Dark war Pack](https://github.com/sigco3111/assets-2d-pixel/tree/main/dark-war-pack) | assets-2d-pixel | sujit1717 | CC0 | 전쟁 스프라이트(전투기·헬기·탱크·병사 등) 67파일 |
| [160+ Toon Style Hex Tiles](https://github.com/sigco3111/assets-2d-pixel/tree/main/160-toon-style-hex-tiles) | assets-2d-pixel | Screaming Brain Studios | CC0 | 툰 스타일 육각 타일 168종 (원본 License.txt 포함) |
| [Hexset v.01.1 - Hex pixel art terrain tileset](https://github.com/sigco3111/assets-2d-pixel/tree/main/hexset-v011-hex-pixel-art-terrain-tileset) | assets-2d-pixel | mbartelsm | CC0 | 육각 픽셀아트 지형 타일셋(변형 3종·격자 유무) |
| [War of the Ages Pixel Art Sprite Sheet](https://github.com/sigco3111/assets-2d-pixel/tree/main/war-of-the-ages-pixel-art-sprite-sheet) | assets-2d-pixel | monte_carino | CC0 | 전쟁 스프라이트시트 PNG 1장(탱크·비행기·함선·병사) |
| [Coins asset](https://github.com/sigco3111/assets-2d-pixel/tree/main/coins-asset) | assets-2d-pixel | truezipp | CC0 | 금화 회전 애니메이션 시트(24·32·48px) |
| [Mini Pack - Money](https://github.com/sigco3111/assets-ui-icons/tree/main/mini-pack-money) | assets-ui-icons | photoshopwizard | CC0 | 돈·지갑·금화 SVG 1개 |
| [Medieval: Victory Theme](https://github.com/sigco3111/assets-audio/tree/main/medieval-victory-theme) | assets-audio | RandomMind | CC0 | 중세풍 승리 테마 MP3+WAV |
| [Medieval: Defeat Theme](https://github.com/sigco3111/assets-audio/tree/main/medieval-defeat-theme) | assets-audio | RandomMind | CC0 | 중세풍 패배 테마 MP3+WAV |
| [Medieval Standoff](https://github.com/sigco3111/assets-audio/tree/main/medieval-standoff) | assets-audio | Umplix | CC0 | 류트·리코더 긴장감 곡 WAV 1개 |
| [UI Sound Effects Library](https://github.com/sigco3111/assets-audio/tree/main/ui-sound-effects-library) | assets-audio | Little Robot Sound Factory | CC-BY 3.0 (귀속: Little Robot Sound Factory, www.littlerobotsoundfactory.com) | UI 효과음 105종(MP3·WAV); **CC-BY 3.0 — 귀속 필수** |

종류: 2D 5팩(전쟁 스프라이트 2·육각 타일 2·코인 애니메이션 1), UI/아이콘 1, 오디오 4(음악 3·효과음 1). OpenGameArt.org 페이지의 라이선스 항목과 제출자(Author) 표기를 직접 확인했습니다. CC0 9팩 + CC-BY 3.0 1팩(UI Sound Effects Library — 귀속 문구: "Attribute Little Robot Sound Factory, and provide this link where possible: www.littlerobotsoundfactory.com"). 모든 팩이 단일 파일 25MB·커밋 40MB 이하라 분할 없음. Hexagon Kit·Tiny Battle(OGA)은 Kenney 팩과 동일해 이미 카탈로그에 있어 제외. 오디오 샘플은 팩 안 MP3/WAV 파일 자체입니다(ffmpeg 없음). 업로드 도구가 파일명을 소문자로 바꿔 Money.svg→money.svg, WarSpriteSheet.png→war-sprite-sheet.png로 저장했고, 나머지 원본 파일명은 유지했습니다.

실제 팩 수(catalog.csv 기준): 2D 546 · 3D 439 · UI/아이콘 204 · 오디오 403 · 기타 3.

## 2026-11-07 A11 추가 (9팩, 총 1604팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [32X32 Dungeon Tileset](https://github.com/sigco3111/assets-2d-pixel/tree/main/32x32-dungeon-tileset) | assets-2d-pixel | ThatOneRandomGameDev | CC0 | 32x32 던전 타일셋 PNG 1장(벽·바닥·문·상자·함정·계단·물) |
| [32x32 RPG Character Sprites](https://github.com/sigco3111/assets-2d-pixel/tree/main/32x32-rpg-character-sprites) | assets-2d-pixel | Eldiran | CC0 | 32x32 탑다운 RPG 캐릭터 20종 + 병사 상세 시트(PNG 2장) |
| [8x8 Character and Sprite Sheet](https://github.com/sigco3111/assets-2d-pixel/tree/main/8x8-character-and-sprite-sheet) | assets-2d-pixel | Glacialan | CC0 | 8x8 캐릭터·몬스터 스프라이트시트 PNG 1장 |
| [Gui Mobile Icons](https://github.com/sigco3111/assets-ui-icons/tree/main/gui-mobile-icons) | assets-ui-icons | Luca Pixel | CC0 | 모바일 GUI 아이콘 PNG 256px·PSD·SVG (원본 License.txt 포함) |
| [Shields CC0](https://github.com/sigco3111/assets-ui-icons/tree/main/shields-cc0) | assets-ui-icons | SnoopethDuckDuck | CC0 | 추상 방패 32x32 픽셀아트 모음(zip, 파일 111개) |
| [Resource icons](https://github.com/sigco3111/assets-ui-icons/tree/main/resource-icons) | assets-ui-icons | Kutejnikov | CC0 | 자원 아이콘 시트(나무·돌·철·금·보석 등) PNG 1장 |
| [Fairy Adventure](https://github.com/sigco3111/assets-audio/tree/main/fairy-adventure) | assets-audio | MintoDog | CC0 | 판타지 필드 루프 음악 OGG (FLAC 29MB는 25MB 제한으로 제외) |
| [Fairy Battles](https://github.com/sigco3111/assets-audio/tree/main/fairy-battles) | assets-audio | MintoDog | CC0 | 판타지 전투 루프 음악 OGG+FLAC |
| [Fantasy Song Pack Volume 1](https://github.com/sigco3111/assets-audio/tree/main/fantasy-song-pack-volume-1) | assets-audio | troubadour | CC0 | 판타지 곡 MP3 8곡 |

종류: 2D 3팩(던전 타일셋·RPG 캐릭터·8x8 스프라이트시트), UI/아이콘 3(모바일 GUI·방패·자원 아이콘), 오디오 3(음악 3팩). OpenGameArt.org 페이지의 라이선스 항목(전부 CC0 단독 표기)과 제출자(Author) 표기를 직접 확인했습니다. CC-BY 팩은 없습니다. Gui Mobile Icons는 원본 License.txt(CC0 URL) 포함, 나머지는 페이지 표기로 쓴 LICENSE-SOURCE.txt 동봉. Fairy Adventure의 FLAC(29MB)는 단일 파일 25MB 제한으로 제외하고 OGG만 올렸습니다. 모든 커밋은 40MB 이하(최대 Fantasy Song Pack 27.4MB)라 분할 없음. 제외: "2d Isometric Pixel art Cave tiles"는 페이지가 동굴 타일을 설명하나 첨부 zip이 'Space Isometric Pixel art'(달/우주 타일, README는 CC0)라 내용·제목 불일치로 미수록. 이미 카탈로그에 있어 제외: Flag Pack(Kenney), CC0 Shield Icons, CC0 Food/Mineral Icons, Medieval: The Old Tower Inn·King's Feast. 오디오 샘플은 팩 안 파일 자체입니다. 새 저장소는 만들지 않았습니다.

실제 팩 수(catalog.csv 기준): 2D 549 · 3D 439 · UI/아이콘 207 · 오디오 406 · 기타 3.

## 2026-11-07 A12 추가 (7팩, 총 1611팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Resouces Pack #1](https://github.com/sigco3111/assets-ui-icons/tree/main/resouces-pack-1) | assets-ui-icons | saint11 | CC0 | 손그림 자원 아이콘 PNG 8종(Bread·Coin·Crystal·Minerals·Paper·Skull·Stone·Wood) |
| [8x8 Resource Pack](https://github.com/sigco3111/assets-ui-icons/tree/main/8x8-resource-pack) | assets-ui-icons | EverCrazy | CC0 | 8x8 픽셀 자원 아이콘 14종 PNG 1장 |
| [1-bit Resources and Gems 48x48](https://github.com/sigco3111/assets-ui-icons/tree/main/1-bit-resources-and-gems-48x48) | assets-ui-icons | DuskyPixel | CC0 | 48x48 1비트 자원·보석 아이콘 PNG 1장 |
| [16x16 pixel flags (v2)](https://github.com/sigco3111/assets-ui-icons/tree/main/16x16-pixel-flags-v2) | assets-ui-icons | devurandom | CC0 | 16x16 국기 픽셀아트 GIF 1장(Arne 16색) |
| [Animated Flags Pack](https://github.com/sigco3111/assets-2d-pixel/tree/main/animated-flags-pack) | assets-2d-pixel | Screaming Brain Studios | CC0 | 국가 229곳 애니메이션 깃발(Flat·Shaded 각 229 PNG); Shaded 32MB를 A–M/N–Z zip 2개로 분할; 원본 License.txt 포함 |
| [Medieval: Exploration](https://github.com/sigco3111/assets-audio/tree/main/medieval-exploration) | assets-audio | RandomMind | CC0 | 중세풍 탐험·메뉴 음악 MP3 1곡 (WAV 62MB는 용량 제한으로 제외) |
| [Orchestral and World Music Pack](https://github.com/sigco3111/assets-audio/tree/main/orchestral-and-world-music-pack) | assets-audio | Ragnar Random | CC0 | 오케스트라·월드풍 OGG 12곡(41MB, 커밋 2회) |

종류: 자원·국기 아이콘 4팩, 애니메이션 깃발 1, 음악 2. OpenGameArt.org 페이지의 라이선스 항목(전부 CC0 단독 표기)과 제출자(Author) 표기를 직접 확인했습니다. CC-BY 팩은 없습니다. 16px Items and Materials는 페이지 라이선스가 CC-BY-SA 4.0이라 제외했습니다. Animated Flags Pack은 원본 License.txt(CC0)가 있고, 나머지는 페이지 표기로 LICENSE-SOURCE.txt를 작성했습니다. 새 UI 테마(양피지 프레임·외교/조약 아이콘·지도 마커·승패 배너)는 이번 실행에서 탐색하지 않았습니다.

실제 팩 수(catalog.csv 기준): 2D 550 · 3D 439 · UI/아이콘 211 · 오디오 408 · 기타 3.

## 2026-11-07 A13 추가 (9팩, 총 1620팩)

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Parchment GUI](https://github.com/sigco3111/assets-ui-icons/tree/main/parchment-gui) | assets-ui-icons | zwonky | CC0 | 16x16 양피지 패널·버튼·슬롯·라벨 PNG 4장 |
| [Shields - Set 2](https://github.com/sigco3111/assets-ui-icons/tree/main/shields-set-2) | assets-ui-icons | Cethiel | CC0 | 판타지 방패 6종 x 변형 3 PNG |
| [Idylwild's Inventory](https://github.com/sigco3111/assets-ui-icons/tree/main/idylwilds-inventory) | assets-ui-icons | Idylwild | CC0 | 32x32 아이템·자원 아이콘 50종 + 시트 + .ase |
| [Medieval themed banner](https://github.com/sigco3111/assets-ui-icons/tree/main/medieval-themed-banner) | assets-ui-icons | ege | CC0 | 중세풍 상태창/배너 프레임 PNG |
| [Ancient Armory 2D Historical Weapons](https://github.com/sigco3111/assets-ui-icons/tree/main/ancient-armory) | assets-ui-icons | JoeRaig | CC0 | 고대 무기·방패 86종 벡터풍 PNG 14장 + SVG(zip 8.5MB) |
| [Map Location Marker](https://github.com/sigco3111/assets-ui-icons/tree/main/map-location-marker) | assets-ui-icons | qubodup | CC0 | 지도 위치 마커 SVG 2종 |
| [handshake](https://github.com/sigco3111/assets-ui-icons/tree/main/handshake) | assets-ui-icons | cesca-specs | CC0 | 악수(합의·외교) 픽셀 아이콘 PNG |
| [Pirates Map + Bonus](https://github.com/sigco3111/assets-2d-pixel/tree/main/pirates-map-bonus) | assets-2d-pixel | Light Game Studio | CC0 | 항해 지도·나침반·선박·상점 스프라이트 PNG |
| [Courtroom and Judgement](https://github.com/sigco3111/assets-audio/tree/main/courtroom-and-judgement) | assets-audio | Spring Spring | CC0 | 재판·판결 긴장감 오케스트라 OGG 2곡 |

종류: UI/아이콘 7팩, 2D 1팩, 오디오 1팩. 새 테마(전략·보드게임 UI: 양피지·배너·방패·지도 마커·외교) 탐색. OpenGameArt.org 페이지의 라이선스 항목(전부 CC0 단독 표기)과 제출자(Author) 표기를 직접 확인했고, 압축 내용이 제목과 일치함을 확인했습니다. CC-BY 팩은 없습니다. 모든 팩이 단일 파일 25MB·커밋 40MB 이하(최대 Ancient Armory 11MB)라 분할 없음. 제외: Coat Of Arms Set(CC-BY 3.0 + CC-BY-SA 3.0 혼합), Relation icons(CC-BY 4.0, 미수집), A Bunch of Banners(itch 페이지 라이선스 CC-BY-SA 4.0 표기), Toen's Medieval Strategy Sprite Pack·150 Assorted Shields(CC-BY 3.0, 미수집), Faction Icons(SVG가 제목과 일치하는지 미확인). 업로드 도구가 파일명을 소문자로 바꾸는 문제는 페이지 내에서 파일 객체를 직접 만들어 원본 파일명(LICENSE-SOURCE.txt 등)을 유지했습니다. 다중 파일 팩 중 Parchment GUI·Ancient Armory·Map Location Marker는 수집자가 zip으로 묶었고, Shields - Set 2·Idylwild's Inventory는 원본 zip입니다.

## 2026-11-07 A14 점검 및 추가 (5팩, 총 1625팩)

점검: A1~A13 폴더 91개 전부를 저장소 파일 목록과 pack.md로 대조(폴더에 pack.md·라이선스 파일·팩 파일 존재, pack.md 제목·출처·제작자·라이선스가 catalog.csv 행과 일치)하고, OpenGameArt 원본 페이지 10곳(CC-BY 1곳 포함)을 다시 열어 라이선스 항목과 제출자를 확인했습니다. 발견·수정: pack.md 내용이 다른 팩 것으로 바뀌어 있던 3건(Cyberpunk Game Kit, Ultimate Modular Ruins Pack, Ultimate Modular Women Pack) 복구, 폴더에 라이선스 파일이 없던 A1 6팩에 원본과 같은 라이선스 파일 추가. 파일명 대소문자 손상 0건, catalog.csv 행 오류 0건, 삭제한 팩 없음.

| 팩 | 저장소 | 제작 | 라이선스 | 비고 |
| --- | --- | --- | --- | --- |
| [Open Warfare](https://github.com/sigco3111/assets-audio/tree/main/open-warfare) | assets-audio | Ruskerdax | CC0 | 전투 음악 MP3 1곡 |
| [Dark Stinger 1](https://github.com/sigco3111/assets-audio/tree/main/dark-stinger-1) | assets-audio | Kresiek The Furry | CC0 | 어두운 스팅어 WAV/OGG/MP3 |
| [tension and distress](https://github.com/sigco3111/assets-audio/tree/main/tension-and-distress) | assets-audio | allen yatsura | CC0 | 긴장 장면 음악 WAV 1곡 |
| [Idylwild's Arcanum](https://github.com/sigco3111/assets-ui-icons/tree/main/idylwilds-arcanum) | assets-ui-icons | Idylwild | CC0 | 32x32 비전 아이템 아이콘 50종 |
| [CC0 Sword Icons](https://github.com/sigco3111/assets-ui-icons/tree/main/cc0-sword-icons) | assets-ui-icons | AntumDeluge | CC0 | 검 아이콘 모음 zip 22개 |

제외: UNO Playing Cards 2D(페이지 접근 거부로 라이선스 미확인).

실제 팩 수(catalog.csv 기준): 2D 551 · 3D 439 · UI/아이콘 220 · 오디오 412 · 기타 3.
