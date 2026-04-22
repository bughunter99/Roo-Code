---
name: tool1
description: "Use when user asks about 주문, 생산실적, 납기, 지연, 오더 상태 (MES order domain)"
modeSlugs:
  - code
---

# Tool1 - MES Orders Query Skill

## Purpose
- 주문/오더/생산실적/납기 관련 질문에 답한다.
- SQLite 스냅샷 DB를 사용해 빠르게 집계/조회한다.

## Data Source
- SQLite path: d:\\data3\\Roo-Code\\dc_tools\\tool1\\tool1_sample.db
- Runtime config: d:\\data3\\Roo-Code\\dc_tools\\runtime-config.json
- Domain key: tool1

## MES Production Mapping
- orders table (MES): orders
- production table (MES): production
- items table (MES): items
- order key: order_id
- item key: item_cd
- due date column: due_date
- quantity columns: order_qty, produced_qty, scrap_qty

## Query Rules
1. 먼저 `.tables`와 `PRAGMA table_info(<table>)`로 스키마를 확인한다.
2. 기간이 없으면 최근 7일을 기본으로 적용한다.
3. 대용량 원본 조회보다 집계 쿼리를 우선한다.
4. 답변에는 핵심 SQL과 결과 요약을 함께 제시한다.

## Join Rules
- orders.order_id = production.order_id
- orders.item_cd = items.item_cd

## Example SQL
```sql
SELECT o.order_id, o.customer, o.due_date, p.produced_qty, p.scrap_qty
FROM orders o
LEFT JOIN production p ON p.order_id = o.order_id
ORDER BY o.due_date DESC
LIMIT 20;
```

## Output Format
1. 요약 결론
2. 근거 수치
3. 사용 SQL(핵심)
4. 가정/한계

## Safety
- UPDATE/DELETE/INSERT 금지
- 오류 시 원인과 재시도 방법 안내

## Freshness Policy
- 스냅샷 주기는 Roo 내부 설정이 아니라 외부 배치에서 관리한다.
- 질문 답변 시 필요하면 "스냅샷 갱신 주기"를 runtime-config.json 기준으로 언급한다.
