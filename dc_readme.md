# Roo-Code 분석 요약 (dc_readme)

## 1. 프로젝트 개요
- 프로젝트 경로: D:\data3\Roo-Code
- 자동 분류: Node.js/웹 애플리케이션
- 분석 시각: 2026-04-10 13:40:49
- 분석 방식: 정적 구조 분석(파일 트리, 확장자 분포, 빌드/설정 파일 탐지)

## 2. 소스 구성 분석
- 샘플링 파일 수(최대 5000): 2696
- 상위 확장자 분포: .ts(1343), .tsx(464), .json(405), .md(97), .png(97), .xml(32), .svg(27), .snap(27)
- 최상위 디렉터리: .changeset, .github, .husky, .roo, .vscode, apps, dc_code, dc_diagrams, locales, packages, releases, scripts
- 주요 엔트리/빌드 파일: README.md, readme.md, package.json

## 3. 기술 스택 추정
- 확장자 및 빌드 파일 기반으로 추정한 기술 스택은 위 구성 분석을 따르며,
  복수 언어/복수 빌드 시스템이 공존할 가능성이 있습니다.
- 대규모 저장소의 경우 샘플링 한계로 일부 하위 모듈은 통계에서 제외될 수 있습니다.

## 4. README.md 반영 권장 항목 (한국어)
- 프로젝트 목적/문제 정의
- 실행 방법(로컬 실행, 테스트, 빌드)
- 디렉터리 구조 설명(핵심 모듈 중심)
- 주요 의존성 및 버전 정책
- 배포/운영 가이드(있다면)
- 기여 가이드 및 코딩 규칙

## 5. 추가 개선 제안
- 아키텍처 다이어그램과 실제 코드 간 정합성 점검 자동화
- CI에서 린트/테스트/보안 스캔 파이프라인 표준화
- 모듈 경계와 데이터 흐름 문서 정기 갱신

---

## 6. Roo Code - SQLite DB 컨텍스트 설정 방법

매번 질문할 때 SQLite DB 경로를 언급하지 않아도, 미리 설정해두면 Roo Code가 자동으로 해당 DB를 참고해서 답변합니다.

### 방법 1: `.roorules` 파일 (가장 간단, 권장)

워크스페이스 루트에 `.roorules` 파일을 생성하고 아래처럼 작성합니다.

```
이 프로젝트의 데이터베이스는 C:\myproject\data.db (SQLite)입니다.
데이터 관련 질문에는 항상 이 DB를 sqlite3 명령으로 조회해서 답하세요.
```

- Roo Code가 **매 질문마다** 이 파일을 자동으로 시스템 프롬프트에 포함시킵니다.
- 워크스페이스별로 다른 DB를 지정할 수 있습니다.

### 방법 2: `.roo/rules-{모드명}/` 폴더 (모드별 적용)

특정 모드에서만 적용하고 싶을 때 사용합니다.

```
.roo/
  rules-code/
    db-context.md   ← 여기에 DB 경로 및 지시사항 작성
```

`db-context.md` 내용 예시:
```
이 프로젝트의 데이터베이스는 C:\myproject\data.db (SQLite)입니다.
데이터 관련 질문에는 sqlite3 명령으로 조회해서 답하세요.
```

### 방법 3: Roo Code 설정 → Custom Instructions (전역 적용)

VS Code 사이드바 → Roo Code 설정 → **"Custom Instructions"** 텍스트 박스에 직접 입력합니다.  
모든 워크스페이스, 모든 세션에 전역으로 적용됩니다.

### 동작 원리

Roo Code는 SQLite 파일을 직접 파싱하는 기능이 내장된 것이 아닙니다.  
AI가 `execute_command` 도구를 통해 터미널에서 `sqlite3` CLI를 실행하여 조회합니다.

```bash
sqlite3 C:\myproject\data.db ".tables"
sqlite3 C:\myproject\data.db "SELECT * FROM users LIMIT 10"
```

따라서 **시스템에 `sqlite3`가 설치되어 있어야** 합니다.

- 설치 확인: `sqlite3 --version`
- Windows 설치: `winget install SQLite.SQLite` 또는 https://www.sqlite.org/download.html

---

## 7. MES 질의응답용 Skill 설계안 (SQLite 스냅샷 기반)

목표:
- MES 원본 시스템의 방대한 테이블을 직접 매번 조회하지 않고,
- 질문 가능한 핵심 데이터를 주기적으로 SQLite 파일로 적재한 뒤,
- 질문 유형별 SKILL.md 지시문으로 Roo Code가 적절한 DB/쿼리 패턴을 선택하도록 운영

### 7.1 운영 가능 여부

가능함. 이 프로젝트의 Roo Code는 워크스페이스 `.roo/skills/*/SKILL.md`를 탐색하고,
현재 모드/설명(description) 기준으로 적용할 스킬을 선택해 로드하는 구조를 지원한다.

### 7.2 권장 디렉터리 구조

```text
.roo/
  skills/
    mes-orders/
      SKILL.md
      docs/
        schema.md
        query-playbook.md
    mes-quality/
      SKILL.md
      docs/
        schema.md
        query-playbook.md
    mes-inventory/
      SKILL.md
      docs/
        schema.md
        query-playbook.md
```

선택 사항(모드 제한):
- `SKILL.md` frontmatter에 `modeSlugs`를 넣어 특정 모드에서만 활성화

### 7.3 Skill 분할 기준

스킬은 "도메인 + 질문 의도" 단위로 분리하는 것이 좋다.

- `mes-orders`: 수주/생산실적/납기/지연 원인
- `mes-quality`: 불량/수율/검사이력/LOT 추적
- `mes-inventory`: 재고/입출고/창고별 수량/회전율

규칙:
- 한 스킬이 너무 많은 질문군을 포함하지 않기
- description에 트리거 키워드를 구체적으로 넣기
- 중복 키워드가 많은 경우 우선순위 규칙을 SKILL.md에 명시

### 7.4 SKILL.md 템플릿 (권장)

```md
---
name: mes-quality
description: "Use when user asks about 불량, 수율, 검사결과, lot 추적, 품질 추세"
modeSlugs:
  - code
---

# MES Quality Assistant

## Scope
- 품질/검사/불량/수율 질문만 처리한다.
- 범위를 벗어나면 mes-orders 또는 mes-inventory 스킬 사용을 우선 검토한다.

## Data Sources
- SQLite path: D:\mes-snapshots\quality_snapshot.db
- 주요 테이블:
  - qc_result(qc_id, lot_no, item_cd, wc_cd, defect_qty, inspect_ts)
  - prod_lot(lot_no, wo_no, item_cd, start_ts, end_ts)
  - item_master(item_cd, item_nm, spec)

## Join Keys
- qc_result.lot_no = prod_lot.lot_no
- qc_result.item_cd = item_master.item_cd

## Query Strategy
1. 먼저 `.tables`와 `PRAGMA table_info(<table>)`로 스키마 확인
2. 질문 기간이 없으면 최근 7일 기본 적용
3. 대용량 조회 시 LIMIT/집계 우선
4. 합계/비율(수율)은 분모 0 예외 처리

## SQL Patterns
- 불량 상위 품목:
  SELECT item_cd, SUM(defect_qty) AS defect_sum
  FROM qc_result
  WHERE inspect_ts >= datetime('now', '-7 day')
  GROUP BY item_cd
  ORDER BY defect_sum DESC
  LIMIT 20;

## Output Format
- 답변은 다음 순서로 제공:
  1) 요약 결론
  2) 근거 수치
  3) 사용 SQL(핵심만)
  4) 데이터 한계/가정

## Safety Rules
- UPDATE/DELETE/INSERT 금지
- 경로가 없거나 sqlite3 오류면 원인과 재시도 방법 안내
```

### 7.5 스냅샷 DB 설계 원칙

- 원본 MES 전체를 복사하지 말고 질문 빈도가 높은 컬럼만 추출
- 날짜 파티션(일/주) 단위로 파일 분리 고려
- 코드성 컬럼(item_cd, wc_cd)은 반드시 마스터 테이블과 함께 제공
- 조인 키/인덱스를 스냅샷 단계에서 보장

권장 인덱스 예시:
- `CREATE INDEX idx_qc_result_inspect_ts ON qc_result(inspect_ts);`
- `CREATE INDEX idx_qc_result_lot_no ON qc_result(lot_no);`
- `CREATE INDEX idx_prod_lot_lot_no ON prod_lot(lot_no);`

### 7.6 질문 라우팅 전략

스킬 선택 정확도를 높이려면 각 스킬 description에 아래를 포함:
- 대표 질문 문구
- 핵심 키워드(불량, 수율, 재고, 납기 등)
- 비적용 범위(예: 재고 질문은 mes-inventory로)

### 7.7 운영 체크리스트

- sqlite3 설치 확인 (`sqlite3 --version`)
- 각 스킬의 DB 경로 유효성 확인
- 스키마 변경 시 `docs/schema.md` 동기화
- SQL 패턴 테스트(표본 질문 10~20개)
- 월 1회 스킬 description/키워드 튜닝

### 7.8 한계 및 대안

- SKILL.md는 "지시문"이며, 자동 ETL 스케줄링 기능은 아님
- DB 스냅샷 생성/갱신은 외부 배치 작업(예: Python, Airflow, Windows Task Scheduler)로 운영 필요
- 필요 시 MCP 서버를 붙여 SQL 실행/권한 제어를 더 엄격히 관리 가능
