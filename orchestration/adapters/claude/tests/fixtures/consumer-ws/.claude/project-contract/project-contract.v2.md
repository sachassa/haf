# Project Contract v2 (테스트 픽스처)

contract_to_graph 테스트용 최소 소비 워크스페이스 픽스처다. resolve_contract 가 이 파일
(v2 = 최대 버전)을 선택해야 한다. 내용은 파싱되지 않는다(경로 임베드만).

같은 디렉터리의 `coverage-ledger.json` 은 커버리지 백스톱(축 4) 통과용 픽스처 원장이다 —
픽스처 Contract 수정이 훅에 차단되지 않게 한다. 축 id 는 정책 데이터에서 생성했고 드리프트
통제는 `discovery/adapters/claude/tests/test_skill_axis_binding.py` 가 소유한다.
