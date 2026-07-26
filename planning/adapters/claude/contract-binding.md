# planning/adapters/claude/contract-binding — Claude Code Project Contract Adapter 바인딩

상태: v1.2 Baseline · 2026-07-07 · 상위 규약: AGENT.md
근거 정본(§ 포인터만·재정의 0): `planning/specs/03-project-contract.md` §3.1·§3.2-A~D·§3.3·§3.4·§3.5·§3.6(PC-INV 1~12)·§4.1(바인딩 대상 표 4행)·§4.2(이식 교체 지점) — 본 문서가 물리 실현으로 바인딩하는 계약의 정본. 자매 선례·경계 근거: `uahf/framework/adapters/claude/memory-binding.md`·`scaffold-binding.md` §4(골격·"Markdown 본문 + front-matter" 관례·"지원 구조 = 시연 시 생성" L-07) · `uahf/framework/core/structure.md` §2·§5(C-3 — Adapter 경계는 격리 보유로 비적용)·§7(C-1) · 루트 `ARCHITECTURE.md` §7·§7.1·§8(UAF-INV ①②③) · `entry/specs/01-entry.md` §4.1 불릿 2·§3.2-C·EN-INV 2(contract-presence 탐지의 경로 관례·직렬화·존재 판정 수단을 Adapter 소관으로 위임) · `uahf/specs/12-scaffold.md` §3.2-A · `uahf/specs/00-glossary.md`(용어 신설 0 — `형태 A/B`는 structure.md §4 서술 라벨 인용).

거버넌스: 이 문서는 `planning/adapters/claude/` 소속 **Adapter Binding 문서**다. 이 경계는 Core·UAF 계약을 특정 실행 환경·직렬화 형식·물리 경로에 바인딩한 산출물을 **격리**하는 지점이며(structure.md §2·§5), 구체 직렬화 형식·물리 경로·환경 토큰의 사용이 **허용**된다(여기가 격리 지점이다 — C-3 비적용, 자매 memory-binding.md §0·scaffold-binding.md §0과 동형). 단 UAF·UAHF 정본을 **재정의하지 않는다** — 계약(필드 그룹·코어 필드·버저닝·불변)은 § 포인터로만 인용한다. 개정은 Advisor 승인으로만 이뤄진다.

---

## §0. 이 문서의 위치와 정본 경계

- **정본은 planning/specs/03 §3·§4다.** 이 문서는 그 계약의 **환경 실현 매핑**이며 계약 요소(필드 그룹 9종·필수 코어 필드·Dimension 매핑·버저닝 규율·인스턴스 거버넌스·UAHF Interface·PC-INV 1~12)를 **재정의·확장하지 않는다**. 본 문서가 확정하는 것은 03 §4.1이 "Adapter 소관"으로 미룬 **넷**뿐이다 — ① 직렬화 형식(§3) ② 저장 위치(§4) ③ 버전 표기(§5) ④ Provenance 컨테이너 외형·must-ignore 경계(§6). Provenance 내부 형식은 discovery-binding.md에, contract-presence 존재 판정 실행은 entry-binding.md에 포인터로 위임한다(추측·선취 금지).
- **격리 지점의 방향 반전(C-3 비적용).** Core 경계와 UAF 정본 본문은 특정 AI·언어·툴체인·직렬화 형식 토큰이 0건이다(structure.md §5·03 §3 도입·PC-INV 12). 이 문서는 그 **반대편**이며 구체 직렬화 형식·물리 경로·파일 확장자 사용이 허용된다. 단 **UAF 정본이 명명하지 않은 것을 UAF 정본 문면인 것처럼 서술하지 않는다** — 물리 확정은 전부 본 문서 소유임을 명시한다.
- **하네스 Bootstrap 전제(형태 A, D-v1.2-1)·문면만 소유(L-07).** 바인딩은 **실행 코드 0**이므로 매핑은 (i) 물리 실재 표면, (ii) 규약으로 확정된 정본 문면(형태 A — 경로·형식·표기 규격), (iii) 실행 코드 도입 시 로딩될 지점(형태 B — 컴파일러·tolerant reader 파서)을 정직하게 구분한다. 본 문서가 확정하는 물리 경로의 데이터 자산 자체는 생성하지 않고 경로·구조·형식의 **정본 문면만** 소유한다(memory-binding.md §7 "지원 구조 — 시연 시 생성" 선례 동형·물리 위치는 2차 산출물 디커플링 트랙 확정).
- **네임스페이스·용어.** 03이 소유하는 스키마 용어(`schemaVersion`·`instanceVersion`·`supersedes`·tolerant reader·opaque annex 등)는 03 정의를 § 포인터로 참조하고 재정의하지 않는다. 새 UAHF 용어·새 계약 요소(필드·연산·불변·kind)를 신설하지 않는다.

---

## §1. 목적

planning/specs/03 "### 4.1 바인딩 대상" 표 4행을 이 환경 위에 **v1.2 시점의 구체 물리 실현**으로 매핑한다. Contract는 UAF↔UAHF 유일 접점·Stable Contract(Public API, 03 §3.1-A)이므로 여기서 확정하는 물리 인터페이스는 후속 작업의 **선행 확정 인터페이스**다. 책임은 (i) §4.1 표 4행의 물리 실현(§2), (ii) 직렬화(§3)·저장 위치(§4)·버전 표기(§5)·Provenance 외형(§6) 확정, (iii) 03 §4.2 이식 교체 지점 대응(§8)이다. 03 §3·§4·UAHF 정본의 어떤 계약 요소도 재정의·확장하지 않으며(§0), 형태 A → 형태 B 전환에도 03 §3 계약 변경은 0이다(structure.md §7 C-1 동형).

---

## §2. 03 §4.1 바인딩 표 4행 물리 실현

"03 §4.1 바인딩 지점" 열은 정본 표현을 그대로 인용하고, "물리 실현" 열이 본 문서가 확정하는 형식·경로·표기를, "실현 형태" 열이 Bootstrap 상태에서의 **규약 실현(형태 A) / 형태 B**를 구분한다.

| # | 03 §3 계약 요소 (정본 §) | 03 §4.1 바인딩 지점 (정본 인용) | 물리 실현 (claude 환경) | 실현 형태 |
|---|---|---|---|---|
| 1 | Contract 직렬화·물리 포맷 (§3.1·§3.2) | 논리 스키마를 실제 문서·레코드로 표현하는 직렬화 형식. | **Markdown 본문 + YAML front-matter 단일 문서.** front-matter가 9그룹·필수 코어 필드 10의 자기서술 구조를, 본문이 인간 가독 렌더링을 담는다. Provenance는 분리 네임스페이스 컨테이너. 상세 §3. | 형식 확정(정본, 형태 A). 컴파일러·파서는 형태 B. |
| 2 | Contract 저장 위치 (§3.2) | Contract 인스턴스가 프로젝트에 배치·보관되는 물리 위치·경로 관례. | **이원화 확정**: 일반 관례 = 소비 프로젝트 내 `.claude/project-contract/`; 본 UAF 저장소 인스턴스(Brownfield dogfooding) = `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`(격리). 상세 §4. 01-entry §4.1이 Adapter 소관으로 미룬 contract-presence 탐지 경로의 실현(§3.2-C는 Evidence 관측 정의·유/무 도메인만 소유). | 경로 관례 확정(정본, 형태 A). 물리 위치는 2차 산출물 디커플링 트랙에서 확정. |
| 3 | `schemaVersion`·`instanceVersion` 표기 형식 (§3.3·§3.4) | 버전 값의 물리 표기·직렬화. | front-matter 스칼라 — `schemaVersion` = SemVer 점표기 문자열(예 형태 `"1.0"`), `instanceVersion` = 단조 증가 정수, `supersedes` = 이전 인스턴스 참조. 상세 §5. | 표기 형식 확정(정본, 형태 A). |
| 4 | Provenance 부속 물리 형식 (§3.2-D) | 불투명 부속의 물리 저장 형식 — Discovery 측·Adapter 측 소관(내부 구조 비정의). | front-matter 내 **분리 네임스페이스 `provenance` 컨테이너**(불투명 블록) — 외형·must-ignore 경계만 본 문서가 확정. 내부 형식은 후속 discovery-binding.md 소관. 상세 §6. | 컨테이너 외형·경계 확정(정본, 형태 A). 내부 형식은 후속 바인딩 소관. |

주: 위 4행은 03 "### 4.1 바인딩 대상" 표의 전 행이며, 각 "물리 실현"은 정본 표현을 이 환경의 구체 형식·경로로 좁힌 것으로 **새 바인딩 계약을 창설하지 않는다**(§0). 특정 AI·모델·제품 기능·방법론은 여기서도 명명하지 않는다(03 §4.1 말미 동형). 03 §4.1 표에 없는 계약 요소(§3.1 지위·§3.2-A~C·§3.3·§3.4·§3.5·§3.6)는 **이식 시에도 유지되는 것**이며 본 문서가 바인딩하지 않는다(§8 "유지되는 것" 열) — 진위 판정 기준은 03 §3이다.

---

## §3. Contract 직렬화 포맷 확정

03 §4.1 행 1의 물리 실현을 확정한다. 계약(03 §3.2 논리 스키마)은 § 포인터로만 인용하고 물리 직렬화만 확정한다.

### §3.1 확정 — Markdown 본문 + YAML front-matter 단일 문서

**Contract 인스턴스 1건 = Markdown 본문 + YAML front-matter 단일 문서 파일 1개**로 직렬화한다.

- **YAML front-matter** — 9 필드 그룹(03 §3.2-A)과 필수 코어 필드(03 §3.2-B)의 **기계 파싱 가능한 자기서술 구조**를 담는다. tolerant reader가 소비하는 표면이다.
- **Markdown 본문** — 같은 정의의 **인간 가독 렌더링**을 담는다. Advisor Consult 정독(03 §3.5-B (a))이 읽는 프로젝트 정의 정본 문서의 본문이다.

### §3.2 확정 근거 (rationale)

Contract는 03 §3.5-B에서 (a) Advisor가 착수 전 정독하는 Consult 대상 문서, (b) Scaffold가 프로젝트에 배치하는 정본 문서(uahf/specs/12-scaffold.md §3.2-A)로 소비된다. 사람이 정독하는 정의 문서이므로 **인간 가독 문서형(Markdown)이 자연 정합**이며, 기계 소비를 위한 구조화 표면(front-matter)을 겸비한다. 자매 선례 = scaffold-binding.md §4 Install Manifest("Markdown 본문 + front-matter" 프로젝트 배치 문서). 이 구체 직렬화 형식의 명명은 Adapter 경계에서 허용되며(C-3 비적용·§0) 이식 시 대상 환경 포맷으로 교체된다(§8).

### §3.3 03 §3.2 논리 스키마의 표현 요건 충족

- **ⓐ 9그룹·필수 코어 필드 10 표현.** front-matter 중첩 key로 9 필드 그룹(03 §3.2-A)과 필수 코어 필드 10(03 §3.2-B)을 담는다. 각 필드의 충족 의미(03 §3.2-B)는 물리 표현에서 보존된다 — 상세 의미는 03 §3.2-B 소유이며 여기서 재유도하지 않는다(§3.4 예시의 주석이 그 표현 자리를 보인다).
- **ⓑ tolerant reader 정합(03 §3.3-C).** YAML front-matter는 미지 key를 오류 없이 무시 가능한 자기서술 구조다. tolerant reader는 필수 코어 필드 key에만 의존하고 미지 필드·부속 네임스페이스(`provenance` 포함)는 must-ignore한다(PC-INV 5).
- **ⓒ Provenance 분리 불투명 컨테이너.** front-matter 내 분리 네임스페이스 `provenance` key로 표현되며 코어 필드와 물리적으로 구분된다(§6·03 §3.2-D). 내부 구조는 본 문서가 정의하지 않는다.
- **ⓓ append-only 인스턴스 거버넌스(03 §3.4).** 인스턴스 갱신은 **새 `instanceVersion` 문서 파일 추가**로 표현된다 — 기존 인스턴스 파일은 재작성하지 않고(PC-INV 9) 새 파일의 `meta.supersedes`가 이전 인스턴스를 참조한다(§5). memory-binding.md의 append-only 관례와 동형이다.

### §3.4 논리 골격 예시 (물리 front-matter 형태)

아래는 03 §8 예1(Ready Contract 논리 골격)의 물리 front-matter 렌더링 예시다. **9 그룹·필수 코어 필드만** 표현하며 새 계약 요소를 창설하지 않는다.

```
---
meta:
  id: <인스턴스 논리 식별자>
  schemaVersion: "1.0"        # SemVer 점표기 문자열 (§5)
  instanceVersion: 1          # 단조 증가 정수 (§5)
  supersedes: null            # 이전 인스턴스 참조 (없으면 null)
intent: <프로젝트 의도 — 비어 있을 수 없음>
requirements:
  functional: [ ... ]         # 최소 기능 요구 포함
  quality: [ ... ]
constraints: [ ... ]          # 명시적 공집합(빈 목록)도 충족
risks: [ ... ]                # 명시적 공집합(빈 목록)도 충족
architectureDirection:
  decisions: [ ... ]
  open: [ ... ]               # 미결의 명시도 충족
assumptionLedger: [ ]         # Ready에서 빈 원장 허용
readiness:
  completeness: <필수 코어 필드 전건 충족 판정>
  confidenceVector: <종단 판정 산출 기록>      # 03 §3.2-A 경계 — 산출 기록(결과), Discovery 내부 개념 아님
  openQuestions: [ ]          # 미해결 질문 목록 — Contract가 남기는 미해결 사항(산출 기록)
  userApproval: <사용자 승인 기록>
provenance: <불투명 컨테이너 — UAHF must-ignore; 내부 형식은 discovery-binding.md 소관, §6>
---

# Project Contract — <프로젝트명>
(위 front-matter 필드의 인간 가독 렌더링 — Advisor Consult 정독 대상, 03 §3.5-B (a))
```

- **경계 문면(중요).** 위 `readiness`의 `confidenceVector`·`openQuestions`는 03 §3.2-A "Readiness 구성의 경계 문면"이 규정한 종단 판정의 **산출 기록**이며 Discovery의 **내부 개념**(질문 선택·전략·예산·Strategy·Capability)이 **아니다**. 특히 `openQuestions`의 '질문'은 Contract가 남기는 미해결 사항이며 Discovery 내부의 질문 선택 기계와 다르다. 따라서 PC-INV 2 역참조 금지의 대상이 아니다(§7).
- 이 예시는 03 §8 논리 골격의 물리 렌더링일 뿐이며, 물리 직렬화·저장 위치를 확정하는 것은 본 문서다.

---

## §4. 저장 위치 관례 확정

03 §4.1 행 2의 물리 실현을 **이원화**로 확정한다. 두 경로 모두 본 문서가 정본으로 확정한다. 이는 01-entry §4.1(불릿 2)이 "contract-presence 탐지의 경로 관례·직렬화 형식·존재 판정 수단은 Adapter 소관"으로 미룬 지점의 물리 실현이기도 하다.

### §4.1 일반 관례 — 소비 프로젝트 내 배치

- **경로.** 소비 프로젝트 내 `.claude/project-contract/` 디렉터리에 인스턴스 문서를 배치한다.
- **파일명.** 인스턴스 1건 = 파일 1개, `project-contract.v<N>.md`(N = `instanceVersion` 정수, §5). 현재 인스턴스 = 후행 인스턴스에 의해 supersede되지 않은 최고 `instanceVersion` 파일. 인스턴스 갱신은 새 `v<N+1>` 파일 추가로 표현된다(append-only, §3.3 ⓓ).
- **근거.** Contract는 프로젝트 정의 정본 문서로서 (a) Advisor Consult 정독·(b) Scaffold 배치 대상이다(03 §3.5-B). 이 환경에서 하네스 규약·정의 문서의 관례 홈은 `.claude/`이며(scaffold-binding.md §6), Scaffold(uahf/specs/12-scaffold.md §3.2-A)가 관리하는 경계다. Contract를 그 아래 전용 하위 디렉터리에 두어 Advisor가 규약 문서와 함께 정독하고 Scaffold가 함께 배치하도록 정합시킨다. Entry의 contract-presence 관측(01-entry §3.2-C·EN-INV 2)은 이 well-known 경로의 인스턴스 파일 유무로 유/무를 판정한다 — 그중 **존재 판정 수단(탐지 실행)의 상세는 후속 entry-binding.md 소관**이고, 본 문서는 03 §4.1 행 2가 소유하는 **저장 경로 관례**를 확정한다(추측·선취 금지).

### §4.2 본 UAF 저장소 인스턴스 — 격리 배치 (Brownfield dogfooding)

- **경로.** 본 UAF 저장소 자신을 대상 프로젝트로 발견하는 dogfooding 인스턴스는 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`에 격리 배치한다(물리 위치는 2차 산출물 디커플링 트랙에서 확정). 파일명 관례는 §4.1과 동일(`project-contract.v<N>.md`).
- **근거(UAF-INV ① 안전).** dogfood Contract를 라이브 `.claude/` 규약 표면이나 Core 경계에 섞으면 하네스 규약과 발견 산출 데이터가 혼입된다. Adapter 경계 이하 `discovery-data/`로 격리하면 데이터 자산이 격리 지점 뒤에 놓여 접점 원칙(UAF-INV ①)과 정합한다 — 자매 `memory-data/`·`loop-data/` 선례(memory-binding.md §0·§2)와 동형이다.
- **지원 구조.** 이 경로·구조는 본 문서가 확정한 정본 문면이며 본 문서는 물리 데이터 자산을 생성하지 않는다(memory-binding.md §2 "지원 구조 — 시연 시 생성" 선례·L-07).

---

## §5. schemaVersion · instanceVersion 표기 형식 확정

03 §4.1 행 3의 물리 실현을 확정한다. 버저닝 규율(03 §3.3)·인스턴스 거버넌스(03 §3.4)는 § 포인터로만 인용하고 물리 표기만 확정한다.

### §5.1 표기 형식

| 값 | 소속 그룹 (03 §3.2-A) | 물리 표기 (이 Adapter 확정) | 근거 계약 |
|---|---|---|---|
| `schemaVersion` | Meta | **SemVer 점표기 문자열** — `meta.schemaVersion`에 `"MAJOR.MINOR"` 형태 문자열(예 형태 `"1.0"`; 03 §8 예2가 `1.0`→`1.1` MINOR 상승 예시). MINOR·MAJOR 자리의 정수 상승으로 표기. | 03 §3.3-B SemVer 규율 |
| `instanceVersion` | Meta | **단조 증가 정수** — `meta.instanceVersion`에 `1`, `2`, … 정수(03 §8 예3이 `1`→`2` 예시). 갱신마다 1씩 증가하며 파일명 `v<N>`과 정합. | 03 §3.4 인스턴스 거버넌스 |
| `supersedes` | Meta | **이전 인스턴스 참조** — `meta.supersedes`에 이전 `instanceVersion`(또는 그 인스턴스 문서 참조). 최초 인스턴스는 `null`. | 03 §3.4 supersedes 계보 |

### §5.2 물리 표기가 버저닝 불변을 훼손하지 않음 (PC-INV 4·5·6)

- **MINOR = 후방 호환 추가만.** 선택 필드·부속 네임스페이스 추가는 MINOR 자리 상승으로 표기되고, tolerant reader가 추가된 미지 key를 must-ignore하므로(§3.3 ⓑ) 기존 소비 거동은 불변이다.
- **MAJOR = 파괴 변경(원칙 금지).** MAJOR는 원칙적으로 금지되며 불가피 시 마이그레이션 경로 + 거버넌스 개정 절차가 필수다(03 §3.3-B). 본 문서의 표기 형식은 MAJOR를 물리적으로 허용·자동화하지 않는다 — MAJOR 상승 자체가 03 §3.3-E 거버넌스를 거친다.
- **필드 제거 금지·deprecated 마킹.** 확정 필드는 제거하지 않는다. 사용 중단 시 해당 key에 `deprecated: true` 성격의 마킹을 부기하고 **key를 유지**한다(03 §3.3-D). 물리적 key 삭제는 파괴 변경(MAJOR)이며 위 거버넌스 대상이다.

### §5.3 스키마 개정 거버넌스의 물리 반영

논리 스키마 개정은 정본 03의 spec 버전 상승 + §9 Revision History append로만 이뤄지고(03 §3.3-E), **본 바인딩 문서(직렬화·경로·표기)의 개정**은 Advisor 승인으로 이뤄진다(거버넌스 문단). 인스턴스 갱신(§5.1 `instanceVersion`)은 또 별개의 append-only 인스턴스 거버넌스다(03 §3.4). 세 거버넌스는 구분된다.

---

## §6. Provenance 불투명 컨테이너 외형·must-ignore 경계

03 §4.1 행 4의 물리 실현 중 **컨테이너 외형·must-ignore 경계만** 확정하고 내부 내용은 후속 바인딩에 위임한다(03 §3.2-D 동형).

- **외형 확정.** Provenance는 Contract 인스턴스 front-matter 내 **분리 네임스페이스 `provenance` key**(불투명 블록)로 놓인다 — 코어 필드 그룹(§3.2-A 그룹 1~8)과 물리적으로 구분되는 top-level key 하나로 격리된다.
- **must-ignore 경계 확정.** UAHF tolerant reader는 `provenance` 컨테이너(및 그 하위 전체)를 **must-ignore**한다 — 존재를 오류로 취급하지 않고 소비하지 않는다(03 §3.2-D·§3.3-C, PC-INV 3·5). 이 경계로 Discovery 내부 변경이 만드는 실행 메타는 `provenance`와 `instanceVersion`에만 반영되고 `schemaVersion`·코어 스키마에 도달하지 못한다(PC-INV 2·10).
- **내부 형식 비정의 — 후속 위임.** `provenance` 내부 직렬화 형식·필드는 본 문서가 정의하지 않는다. 03 §3.2-D가 지정한 Discovery 측 소관(`discovery/specs/02-discovery.md` §3.5·§3.16)과 후속 바인딩 **discovery-binding.md**에 포인터로만 위임한다 — 내부 구조를 창설하면 불투명 부속 계약을 침범하므로 외형·경계에서 멈춘다.

---

## §7. 상시 불변 자기 점검 (요지 — 판정 기준은 03 §3.6)

자체 점검은 최종 승인이 아니다 — Verifier 독립 판정(CP2)·Advisor 승인(CP3)이 뒤따른다.

- **PC-INV 2(Discovery 내부 개념 역참조 금지).** 점검 scope = 코어 필드 정의부(§3.4 예시 front-matter의 그룹 1~8 코어 필드 key + §5 버전 표기 표). `uaf-verified:` 그 scope에 Discovery 내부 개념 다중 패턴 {질문 선택·전략·예산·Strategy·Capability}를 문면 스캔한 결과 0건이며, 그 어휘는 본 문서에서 오직 **불변·경계·근거 서술 문안**(근거 정본 인용·§3.4 경계 문면·§6 근거·본 절)에만 등장한다 — mention과 use의 경계를 지킨다. Readiness 산출 기록과 Provenance(그룹 9)는 03 §3.2-A 경계 문면·PC-INV 2대로 scope에서 제외된다.
- **PC-INV 4·5·6·11(Stable Contract 규율).** SemVer 표기·tolerant reader must-ignore·필드 제거 금지(deprecated 마킹 후 key 유지)는 §5.2·§3.3 ⓑ·§6이 규율을 있는 그대로 담는다 — 물리 표기가 규율을 자동 완화·훼손하지 않으며 Public API 장기 호환성은 유지된다(루트 §7.1 ②·§8 UAF-INV ①②).
- **PC-INV 8·UAF-INV ①(UAHF 무수정·창설 금지).** UAHF spec의 연산·필드·불변을 추가·변경하지 않는다. Contract의 UAHF 소비(tolerant reader·Consult 정독·Scaffold 배치)는 기존 관행으로 성립하며(03 §3.5-B) 정식 등재는 03 §3.5-C 확장 포인트로 남는다 — 본 문서는 그 등재를 설계하지 않는다. 새 계약 요소 창설 0.

---

## §8. 03 §4.2 이식 교체 지점 대응

"유지되는 것" 열이 이식 축에서 03 §3 Core Contract 불변(structure.md §7 C-1 동형)을 재확인한다.

| 03 §4.2 교체 지점 | 본 문서 대응 절 | 이 환경 바인딩 = 교체되는 것 | 유지되는 것 (03 §3 불변) |
|---|---|---|---|
| Contract 직렬화 형식 → 대상 환경의 문서·레코드 포맷 | §2 행1, §3 | Markdown 본문 + YAML front-matter 단일 문서, §3.4 물리 front-matter 형태. | 03 §3.1 지위·논리 스키마, §3.2-A 필드 그룹 9종·§3.2-B 필수 코어 필드·§3.2-C Dimension 매핑(PC-INV 1). |
| Contract 저장 위치·경로 관례 → 대상 환경의 배치 메커니즘 | §2 행2, §4 | 일반 `.claude/project-contract/`·본 저장소 `uahf/framework/adapters/claude/discovery-data/contracts/uahf/`, `project-contract.v<N>.md` 파일명. | 03 §3.4 인스턴스 거버넌스(append-only·supersedes 계보), §3.5 UAHF Interface(선택 입력·두 소비 지점, PC-INV 9). |
| 버전 표기·Provenance 물리 형식 → 대상 환경의 표기·기록 메커니즘 | §2 행3·4, §5, §6 | `schemaVersion` SemVer 점표기 문자열·`instanceVersion` 정수·`supersedes` 참조, `provenance` 분리 컨테이너 외형. | 03 §3.3 버저닝 규율(SemVer·tolerant reader·필드 제거 금지), §3.2-D Provenance 불투명·§3.6 Invariants PC-INV 3·4·5·6·10·11. |

- "유지되는 것" 열의 계약은 다른 AI·저장 환경으로 이식해도 바뀌지 않는다 — 03 §4.2 "유지되는 것" 목록의 이식 불변성이며 structure.md §7 C-1과 동형이다.
- 본 문서는 03 §4.2를 넘어서는 새 교체 지점·바인딩 계약을 창설하지 않고 v1.2 물리 실현 매핑에 한정한다(창설 금지, §0).

---

## §11. 정본 경계·격리·계약 소유 (self-note)

- **재정의·확장 0.** 본 문서의 모든 매핑은 planning/specs/03 §3·§4의 물리 실현이며, 어떤 필드 그룹·코어 필드·버저닝 규율·인스턴스 거버넌스·불변(PC-INV 1~12)도 이 문서에서 진위가 새로 확정되지 않는다 — 판정 기준은 03 §3이다.
- **소유·확정하는 것 = 넷.** ① 직렬화 형식(§3) ② 저장 위치(§4 이원화) ③ 버전 표기(§5) ④ Provenance 컨테이너 외형·must-ignore 경계(§6). Provenance **내부 형식**은 discovery-binding.md 소관(그 문서 §10이 해소), contract-presence **존재 판정 수단**은 entry-binding.md 소관(그 문서 §4.1이 해소)이다 — 본 문서는 포인터 위임만 하며 선취하지 않는다.
- **격리 토큰의 단일 자리.** 구체 직렬화 형식·물리 경로(`planning/adapters/claude/…`·`.claude/…`)·파일 확장자·버전 값 형태는 이 Adapter 경계 문서에 둔다. UAF 정본은 이 토큰을 "Adapter 소관" 포인터로만 미뤘고 본 문서가 그 소관자다(structure.md §5 C-3 비적용 — 격리 보유).

---

**개정 기록.** 본 문서에는 §9 이력 표가 없고 절 번호가 §8→§11로 건너뛴다 — 작성 당시의 관례이며 여기서 신설·재번호하지 않는다(외부 § 포인터 보존). 2026-07-26: md 슬림화 Wave 4 — 비계약 격리 개정(머리 근거 정본 산문·§3.3 재유도·§7 자기 점검·§8/§11/§12 3중 매핑의 중복 압축 및 §12 요약 삭제)이며, **계약 문면·확정 값(§3.1 직렬화·§3.4 골격 예시·§4 저장 경로·§5.1 표기·§6 Provenance 외형·§8 교체 표)은 무변경**이다. 종전 문면 = git 앵커 90ca19c. `uaf-allow-legacy:` 종전 절 구성(§7 상시 불변 자기 점검 전문·§12 요약)은 git 이력에 보존되며 본 개정은 그 요지만 남긴다.
