# Roo Handoff Guide (정보 전달 + 주기 전달)

이 문서는 아래 2가지를 Roo Code에 전달하는 방법을 설명합니다.

1. 어떤 SQLite를 어떤 질문에 사용할지 (정보 전달)
2. 몇 초마다 스냅샷을 갱신할지 (주기 전달)

## 핵심 원칙

- Roo는 스케줄러가 아닙니다.
- `snapshotIntervalSeconds`는 Roo 설정이 아니라 외부 배치/스케줄러 설정입니다.
- Roo에는 스킬 지시문(SKILL.md)과 설정 파일 경로를 통해 "해석 규칙"을 전달합니다.

## 1) 정보 전달 방법

### A. 스킬 파일 설치

Roo가 자동 인식하는 경로:
- `.roo/skills/tool1/SKILL.md`
- `.roo/skills/tool2/SKILL.md`
- `.roo/skills/tool3/SKILL.md`

이미 준비된 설치 스크립트:
```powershell
powershell -ExecutionPolicy Bypass -File .\\dc_tools\\install_skills.ps1
```

### B. 스킬 내 필수 항목

각 SKILL.md에서 아래를 명시합니다.
- Data Source: SQLite 경로
- Join Rules: 조인 키
- Query Rules: 기간 기본값, 제한, 예외 규칙
- Output Format: 답변 형식
- MES Production Mapping: 실제 MES 컬럼명 매핑

## 2) 주기(초) 전달 방법

### A. 주기 설정 파일

`dc_tools/runtime-config.json`의 값을 기준으로 운영합니다.

```json
{
  "snapshotIntervalSeconds": 300
}
```

### B. 외부 스케줄러/루프 실행

샘플 루프 실행:
```powershell
powershell -ExecutionPolicy Bypass -File .\\dc_tools\\refresh-loop.ps1
```

이 루프는 `snapshotIntervalSeconds`를 읽어 주기적으로 스냅샷 갱신 명령을 실행합니다.

실운영에서는 `create_sample_dbs.py` 대신 MES ETL 명령으로 교체하세요.

예시:
```powershell
python .\\etl\\refresh_mes_snapshots.py
```

## 3) Roo에게 실제로 어떻게 말하면 되는가

아래처럼 작업 시작 시 1회 지시하면 됩니다.

예시 프롬프트:

- "tool1/tool2/tool3 스킬 규칙을 우선 적용해."
- "SQLite는 runtime-config.json에 명시된 경로를 사용해."
- "질문 도메인에 맞는 스킬을 선택해서 조회 SQL을 실행하고, 요약/근거/SQL 순서로 답해."

## 4) 권장 운영 순서

1. `runtime-config.json`에 실운영 DB 경로와 주기(초) 반영
2. 각 SKILL.md의 MES Production Mapping을 샘플명에서 실운영명으로 교체
  - tool1: `orders`, `production`, `items` 및 `order_id/item_cd/due_date` 계열
  - tool2: `qc_results`, `lots`, `items` 및 `lot_no/item_cd/inspect_ts` 계열
  - tool3: `stock_onhand`, `stock_moves`, `items` 및 `item_cd/warehouse/move_ts` 계열
3. `install_skills.ps1` 실행
4. 새 Roo 세션 시작
5. `refresh-loop.ps1` 또는 Task Scheduler로 주기 갱신 실행

## 5) 주의사항

- SQLite 파일 경로가 바뀌면 SKILL.md와 runtime-config.json을 함께 수정
- 질문 실패 시 우선 스키마 확인(`.tables`, `PRAGMA table_info`) 후 재시도
- 쓰기 SQL(INSERT/UPDATE/DELETE) 금지
