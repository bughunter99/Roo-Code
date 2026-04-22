---
name: tool3
description: "Use when user asks about 재고, 입출고, 창고별 수량, 재고 회전, 부족 품목 (MES inventory domain)"
modeSlugs:
  - code
---

# Tool3 - MES Inventory Query Skill

## Purpose
- 재고/입출고/창고별 현황 질문에 답한다.
- 현재고와 최근 이동 이력을 함께 제시한다.

## Data Source
- SQLite path: d:\\data3\\Roo-Code\\dc_tools\\tool3\\tool3_sample.db
- Runtime config: d:\\data3\\Roo-Code\\dc_tools\\runtime-config.json
- Domain key: tool3

## MES Production Mapping
- onhand table (MES): stock_onhand
- move table (MES): stock_moves
- items table (MES): items
- item key: item_cd
- warehouse key: warehouse
- onhand qty column: onhand_qty
- safety stock column: safety_stock
- movement timestamp: move_ts

## Query Rules
1. 현재고는 stock_onhand를 기준으로 한다.
2. 이동 이력은 stock_moves에서 최근순으로 확인한다.
3. 부족 품목은 safety_stock 대비 부족량으로 계산한다.

## Join Rules
- stock_onhand.item_cd = items.item_cd
- stock_moves.item_cd = items.item_cd

## Example SQL
```sql
SELECT s.item_cd, i.item_nm, s.warehouse, s.onhand_qty, s.safety_stock,
       (s.onhand_qty - s.safety_stock) AS gap
FROM stock_onhand s
JOIN items i ON i.item_cd = s.item_cd
ORDER BY gap ASC
LIMIT 20;
```

## Output Format
1. 부족/과잉 핵심 요약
2. 창고별 수량
3. 사용 SQL(핵심)
4. 운영 액션 제안

## Safety
- UPDATE/DELETE/INSERT 금지
- 집계 전 단위(PCS/KG) 혼재 여부 확인

## Freshness Policy
- 스냅샷 주기는 Roo 내부 설정이 아니라 외부 배치에서 관리한다.
- 질문 답변 시 필요하면 "스냅샷 갱신 주기"를 runtime-config.json 기준으로 언급한다.
