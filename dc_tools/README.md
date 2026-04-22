# dc_tools 샘플 구성

이 폴더는 MES 질의응답 운영을 위한 샘플입니다.

- tool1: 주문/생산/납기 도메인
- tool2: 품질/불량/수율 도메인
- tool3: 재고/입출고 도메인

각 폴더에는 아래가 포함됩니다.
- SKILL.md: Roo Code가 질문 유형에 맞춰 로드할 지시문
- *_sample.db: 샘플 SQLite 스냅샷 데이터

추가 운영 파일:
- runtime-config.json: DB 경로/도메인/갱신 주기(초)
- refresh-loop.ps1: 주기 기반 샘플 갱신 루프
- ROO_HANDOFF.md: Roo에 정보/주기 전달 절차 문서

## Roo Code에 넘기는 방법

Roo Code가 자동으로 인식하는 위치는 `.roo/skills/<skill-name>/SKILL.md` 입니다.
`dc_tools`는 샘플 보관소이므로, 실제 사용 시 아래 중 하나를 수행합니다.

1. 복사 방식 (권장)
- `.roo/skills/tool1/SKILL.md`
- `.roo/skills/tool2/SKILL.md`
- `.roo/skills/tool3/SKILL.md`

2. 심볼릭 링크 방식
- `.roo/skills/tool1` -> `dc_tools/tool1`
- `.roo/skills/tool2` -> `dc_tools/tool2`
- `.roo/skills/tool3` -> `dc_tools/tool3`

## 운영 팁
- SKILL.md description에 트리거 키워드를 구체적으로 적을수록 라우팅 정확도가 올라갑니다.
- SQLite 스냅샷은 배치로 주기 갱신하세요 (예: 1시간/1일).
- 스키마 변경 시 SKILL.md의 Join Rules와 Example SQL을 함께 업데이트하세요.

## 주기(초) 설정 예시

`runtime-config.json`의 `snapshotIntervalSeconds` 값을 조정합니다.

```json
{
	"snapshotIntervalSeconds": 300
}
```

샘플 루프 실행:

```powershell
powershell -ExecutionPolicy Bypass -File .\\dc_tools\\refresh-loop.ps1
```
