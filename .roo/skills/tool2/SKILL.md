---
name: tool2
description: "Use when user asks about 불량, 수율, 검사결과, lot 추적, 품질 이상 추세 (MES quality domain)"
modeSlugs:
  - code
---

# Tool2 - MES Quality Query Skill

## Purpose
- 품질/검사/불량/수율 질문에 답한다.
- LOT 기반 추적과 품목별 불량 집계를 우선한다.

## Data Source
- SQLite path: d:\\data3\\Roo-Code\\dc_tools\\tool2\\tool2_sample.db
- Runtime config: d:\\data3\\Roo-Code\\dc_tools\\runtime-config.json
- Domain key: tool2

## MES Production Mapping
- qc results table (MES): qc_results
- lot table (MES): lots
- items table (MES): items
- lot key: lot_no
- item key: item_cd
- inspected qty column: inspected_qty
- defect qty column: defect_qty
- inspection timestamp: inspect_ts

## Query Rules
1. 날짜 조건이 없으면 최근 14일을 기본으로 사용한다.
2. 비율 계산 시 분모 0을 방어한다.
3. 품질 질문은 품목(item_cd)과 공정(work_center)을 함께 본다.

## Join Rules
- qc_results.lot_no = lots.lot_no
- qc_results.item_cd = items.item_cd

## Example SQL
```sql
SELECT q.item_cd, SUM(q.inspected_qty) AS inspected, SUM(q.defect_qty) AS defect,
       ROUND(CASE WHEN SUM(q.inspected_qty)=0 THEN 0
                  ELSE 100.0 * (SUM(q.inspected_qty)-SUM(q.defect_qty))/SUM(q.inspected_qty)
             END, 2) AS yield_pct
FROM qc_results q
GROUP BY q.item_cd
ORDER BY yield_pct ASC
LIMIT 20;
```

## Output Format
1. 핵심 이슈
2. 불량/수율 수치
3. 사용 SQL(핵심)
4. 추가 확인 포인트

## Safety
- UPDATE/DELETE/INSERT 금지
- 스키마 불일치 시 테이블/컬럼 확인 후 재시도

## Freshness Policy
- 스냅샷 주기는 Roo 내부 설정이 아니라 외부 배치에서 관리한다.
- 질문 답변 시 필요하면 "스냅샷 갱신 주기"를 runtime-config.json 기준으로 언급한다.
