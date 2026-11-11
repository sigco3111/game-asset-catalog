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
