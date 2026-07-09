# v0.9 Scaffold 시연 픽스처 — 경계 고지 (FIXTURE NOTICE)

**시연 픽스처 — 실계약 문서·라이브 설정 표면 아님.**

이 디렉터리(`docs/v0.9-demo-fixtures/`)와 그 하위 전부는 v0.9 Scaffold 설치 시연을 위해 구성된 **격리 대상물**이다. 검증 대상 계약 문서(specs/·framework/core·framework/runtime)나 라이브 하네스 설정(라이브 `.claude/`)이 **아니다** (DP-E7 라이브 표면 비오염, 절차서 §4.1).

## 오인·중복 로드 방지 (필수 고지)

- **`new-project/.claude/`는 라이브 `.claude/`가 아니다.** 이는 신규 프로젝트 픽스처에 설치된 **설치본**(scaffold-template 사본)이며, 이 저장소의 라이브 `.claude/`(주 세션 설정)와 구분된다. 설치본 `.claude/`를 라이브 설정으로 로드하지 말 것.
- **`new-project/specs/`·`new-project/framework/`도 설치본**이며 라이브 계약 문서가 아니다.

## 설치본 파일의 바이트 충실성 (머리 주석 부재 이유 — 정직 고지)

- 설치본 내용 파일(`new-project/.claude/*`·`new-project/framework/*`·`new-project/specs/*`)에는 **개별 머리 주석을 넣지 않았다.** 이유: 이 파일들은 scaffold-template/·라이브 기준선의 **바이트 동일 사본**이어야 멱등성(INV-4·CK-8 재설치 diff 0)·설치 충실성 실증이 유효하기 때문이다. 머리 주석 삽입은 설치본을 원본과 다르게 만들어 멱등성 실증을 무효화한다.
- 따라서 픽스처 경계 고지는 이 파일(FIXTURE-NOTICE.md)과 수행 기록(`docs/v0.9-demo.md`)이 경계 전체에 대해 수행한다 — 절차서 §4.2 "픽스처가 라이브가 아님을 표시"의 목적을 설치 충실성을 보존하며 달성한다. (이 처리는 T10 수행 재량 — 정확한 파일 배치 방식; 게이트 검토를 위해 수행 기록 §관측에 투명 기재.)

## 픽스처 구성

| 항목 | 성격 |
|---|---|
| `new-project/` | ① Install + ⑤ 재설치 후 설치본 실물(존치). 설치 대상 신규 프로젝트 픽스처. |
| `new-project/README.md` | 사용자 소유 기존 파일(보호 대상 INV-3·CK-8 시연용). 결함 아님. |
| `new-project/install-manifest.md` | ⑤ 재설치 후 Install Manifest(preservedPaths [README.md]). |
| `install-manifest-initial.md` | ① 최초 설치 스냅샷(빈 프로젝트, preservedPaths []). |
| `new-project-uninstall-copy/` | ⑤ Uninstall 결과 사본 — installedArtifacts 제거·README.md만 잔존(잔여물 0). 설치본 실물(new-project/) 존치 위해 별도 사본에서 수행. |
| `verify-scaffold.md` | 시연 오케스트레이션 사이클 CP2 검증 리포트(독립 Verifier 산출). |
| `FIXTURE-NOTICE.md` | 이 고지. |

## 마일스톤 CP2 정적 스캔 verifier_scope 제외 (DP-E7)

specs/12 §3 본문 AI 비의존 정적 스캔(12 §7-10, 마일스톤 CP2 소관)이 수행될 때, **이 픽스처 경계와 설치본의 물리 토큰**(설치본 `.claude/`·Adapter 경계 배치·Install Manifest의 `"v0.9"` 등)은 대상 경계에서 **제외**하고 제외 사실을 `verifier_scope`에 명시한다 — 픽스처의 정당한 환경 토큰이 실계약 spec 경계의 위반으로 계상되지 않게 한다 (절차서 §4.1).
