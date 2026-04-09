# 무신사 발매 수집

무신사 발매판에서 브랜드별 신상품 발매 정보를 수집하고 엑셀로 저장합니다.
발매 예정 상품의 D-Day 계산, 발매 상태 분류, 커버낫 적용 인사이트를 포함합니다.

## 사용법
`/musinsa-release [옵션]` — 옵션을 생략하면 탭/성별/정렬을 물어봅니다.

## 절차

1. `system/skills/data/musinsa-release.md` 스킬 파일을 읽어 실행 절차 확인
2. **AskUserQuestion으로 필터 선택** (발매 탭, 성별, 정렬)
3. 사용자 선택을 파라미터로 변환하여 `system/scripts/musinsa-release-crawler/crawler.py` 실행
4. 수집 결과 보고 + 커버낫 관점 인사이트 제공

## 발매 탭
- **NOW** — 현재 발매 중인 상품
- **예정** — 발매 예정 상품 (D-Day 계산)
- **인기 재발매** — 재발매 요청이 많은 상품
- **무신사 단독** — 무신사 플랫폼 단독 발매
- **스니커즈 캘린더** — 스니커즈 특화 발매 일정

## 출력
- 엑셀(.xlsx): 이미지(셀 삽입), 브랜드, 상품명, 발매일시, D-Day, 발매상태, 가격, 품절, URL
- 저장 위치: `workspace/musinsa-release/release_YYYYMMDD/`

## 인사이트
- 시장 변화 분석 (브랜드 동향, 가격대 변화, 발매 패턴)
- 신규 유형 분석 (카테고리 신유형, IP 콜라보, 발매 방식)
- 커버낫 적용 제안 (BTA 프레임워크 기반)

## 예시
```
/musinsa-release                    → 필터 선택 → 수집
/musinsa-release 발매 예정 여성       → 예정 탭, 여성 필터 수집
/musinsa-release 무신사 단독 확인해줘 → 무신사 단독 탭 수집
```

## 인수
$ARGUMENTS
