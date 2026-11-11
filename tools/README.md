# tools

## build_index.py

`catalog.csv`에서 기계 판독용 검색 색인과 점검 보고서를 만듭니다. Python 3 표준 라이브러리만 사용하며 결과는 결정적입니다(같은 입력이면 같은 출력).

### 재생성

저장소 루트에서:

```
python3 tools/build_index.py
```

- 입력: `catalog.csv` (CSV 파서 사용, 쉼표가 든 따옴표 필드 처리)
- 출력: `assets-index.json`, `docs/index-report.md`, 그리고 `assets-index.json`이 1.5MB를 넘으면 `assets-index.min.json`(같은 데이터, 공백 없음)
- `generated_from`의 커밋 해시는 `git log -1 -- catalog.csv`로 정함. 직접 지정하려면 `--commit <해시>`.
- 보고서 4장(샘플 링크 점검)은 네트워크를 쓰지 않아 스크립트가 만들지 않습니다. 기존 `docs/index-report.md`의 해당 구간(`link-check` 표식)을 그대로 유지하며, 새 결과를 넣으려면 `--link-check <마크다운 파일>`을 사용하세요.
- `catalog.csv`와 다른 기존 파일은 수정하지 않습니다.

### 자동 재생성 워크플로 (`.github/workflows/rebuild-index.yml`)

- 실행 시점: `catalog.csv`·`tools/build_index.py`·`tools/build_wiki.py` push, 6시간마다 예약 실행(`schedule`), 수동 실행(`workflow_dispatch`). 예약·수동 실행은 push 때 건너뛰었거나 실패한 갱신을 나중에 맞춰 줍니다.
- `catalog.csv`가 없으면(삭제 후 이름 변경하는 짧은 순간 등) `catalog.csv가 없어 이번 실행은 건너뜁니다`를 출력하고 빌드 없이 성공으로 끝납니다.
- 변경이 없으면 `nothing to commit`만 출력하고 커밋하지 않습니다. 변경이 있으면 커밋 후 push하며, push가 경합으로 실패하면 `git pull --rebase` 후 최대 3번 시도합니다.
- `build_index.py`는 `catalog.csv`가 없거나 데이터 행이 100개 미만이면 한국어 오류 메시지를 출력하고 종료 코드 2로 끝납니다(빈 색인 커밋 방지). 이때 출력 파일은 바뀌지 않습니다.
