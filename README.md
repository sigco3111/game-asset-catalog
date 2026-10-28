# game-asset-catalog

재사용 가능한 게임 에셋 라이브러리의 중앙 카탈로그입니다.
실제 파일은 유형별 저장소에 두고, 여기에 모든 에셋의 출처·라이선스·작가·장르 태그를 기록합니다.

## 저장소 구성

| 저장소 | 내용 | 수록 |
| --- | --- | --- |
| [assets-2d-pixel](https://github.com/sigco3111/assets-2d-pixel) | 2D 픽셀 스프라이트, 타일셋, 텍스처 | 68팩 |
| [assets-3d-lowpoly](https://github.com/sigco3111/assets-3d-lowpoly) | 3D 로우폴리 모델·애니메이션 캐릭터 (GLB·OBJ) | 41팩 (릴리스 첨부) |
| [assets-ui-icons](https://github.com/sigco3111/assets-ui-icons) | UI 키트, 아이콘, 폰트 | 12팩 |
| [assets-audio](https://github.com/sigco3111/assets-audio) | 효과음, 배경음악, 음성 (OGG) | 9팩 |

각 저장소 README에 팩별 미리보기 이미지와 내용·형식·개수가 있습니다.

2026-10-28에 3D 저장소에 잘못 분류돼 있던 7팩(Brick Pack, Modular Characters, Prototype Textures, Racing Pack, Robot Pack, Toon Characters, Voxel Pack)을 실제 파일 내용(3D 모델 파일 없음)에 따라 2D 저장소로 옮겼습니다.

## 수집 원칙

- 원본 파일 재배포가 명시적으로 허용된 라이선스(CC0, CC-BY)만 수록합니다.
- CC-BY 팩은 귀속 문구를 카탈로그에 함께 기록합니다.
- CC-BY-SA·GPL·CC-BY-NC, 개별 조건이 확인되지 않은 자료는 수록하지 않습니다.
- Unity Asset Store·Epic(Fab) 등 스토어 구매 에셋은 원본 재배포가 금지되는 경우가 많아 올리지 않습니다.
- 각 zip 안에 제작자 배포 원본 License.txt를 그대로 포함합니다. 원본에 라이선스 파일이 없는 팩(Quaternius Animated Zombie·Cute Monsters)은 공식 배포 페이지의 라이선스 표기를 근거로 수집자가 작성한 LICENSE-SOURCE.txt를 동봉합니다.

## 출처 검증 상태

- Kenney 팩(108개): kenney.nl의 CC0 배포 팩입니다. 원본 배포 페이지의 라이선스 조건과 각 팩 동봉 License.txt를 확인했습니다. 파일 바이트는 공식 미러 github.com/ETdoFresh/kenney.nl 에서 확보했으며, 공식 사이트 원본과 바이트 대조는 하지 않았습니다(kenney.nl 직접 다운로드 차단).
- KayKit 팩(10개): Kay Lousberg의 공식 GitHub 저장소(KayKit-Game-Assets) 원본 바이트를 그대로 보존했고, 동봉 LICENSE.txt(CC0)를 확인했습니다.
- Quaternius 팩(12개): quaternius.com 공식 배포 Google Drive 원본 바이트를 보존했고, 각 팩 페이지의 CC0 조건을 확인했습니다(Animated Zombie·Cute Monsters는 라이선스 미동봉으로 LICENSE-SOURCE.txt에 근거 기록).
- 저장소에 올라간 파일은 업로드 후 원격 다운로드 SHA-256을 로컬과 대조해 일치를 확인했습니다.

## 카탈로그

전체 목록은 [catalog.csv](catalog.csv)를 참고하세요. 장르는 tags 열로 검색합니다 (fantasy, rpg, platformer, towerdefense, shooter, ui, audio 등).
에셋이 늘어나면 장르별 저장소로 다시 나눌 수 있습니다.
