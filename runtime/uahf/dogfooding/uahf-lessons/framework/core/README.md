# framework/core/ — Core Layer 경계 (자리)

이 디렉터리는 Core Layer의 경계다. AI 비의존·언어/툴체인 비의존 **계약·스키마 문서**만 담는다. 실행 코드를 담지 않는다 (structure.md §2·§4 C-2, 01 §3.2-E 규칙 1, 01 §3.3 INV-4).

## 설치 시 배치 안내

설치 시 spec 기준선(specs/)의 Core Contract 인스턴스 문서를 이 경계에 배치한다. 기준선 구성:

- `structure.md` — 디렉터리 구조 규격 (01 §3.2-E 인스턴스).
- `config-schema.md` — Config 스키마 (01 §3.2-B 인스턴스).

## 불변 규칙

- 이 경계의 어떤 문서 본문에도 특정 AI 이름·모델명·제품 기능명·프로그래밍 언어명·툴체인명·직렬화 형식명을 두지 않는다 (structure.md §5 C-3, 01 §3.3 INV-4). 이 규칙은 설치 검증 체크리스트 CK-6의 판정 대상이다 (12 §3.2-C).
- 환경 의존 실현이 필요한 자리에는 일반형 표기와 소관 포인터만 둔다 — 구체 인스턴스는 Adapter Binding 경계(`framework/adapters/<adapter>/`)가 소유한다.
- Core Contract의 정본은 specs/01-runtime.md §3이다. 이 경계의 문서는 그 계약의 인스턴스이며 계약을 재정의하지 않는다.

이 안내 파일 자체도 AI 비의존을 유지한다.
