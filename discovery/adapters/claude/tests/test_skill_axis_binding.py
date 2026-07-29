"""축 실값 사본의 드리프트 통제 — 정책 데이터 ↔ SKILL.md 표 ↔ 픽스처 원장 대조.

축 집합의 **단일 소유자는 정책 데이터**(`policy/*-policy.yaml` 의 `coverage.requiredAxes`)다
(discovery-binding §8.2 (마) 「축 집합 사본 금지」). 그럼에도 두 곳에 사본이 존재한다:

  (1) `.claude/skills/discovery-interview/SKILL.md` Part 1 커버리지 맵의 「축 id」 열
      — 인터뷰 수행자가 원장에 쓸 기계 키를 알아야 하므로 사람이 읽는 표에 id 를 둔다.
  (2) `orchestration/adapters/claude/tests/fixtures/consumer-ws/.claude/project-contract/
      coverage-ledger.json` — 픽스처 Contract 가 커버리지 백스톱에 차단되지 않게 하는 테스트 데이터.

사본을 두는 대신 **드리프트를 이 테스트가 고정**한다(어휘 드리프트 테스트 `TestVocabularyDrift`
선례 동형 — 문서 문자열과 코드 상수를 대조해 조용한 분기를 차단하는 방식).

stdlib unittest + PyYAML 만 쓴다(형제 테스트 관례 정합·오프라인·네트워크 0·순수 판독).
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml

_TEST_FILE = Path(__file__).resolve()
_REPO = _TEST_FILE.parents[4]

_POLICY_DIR = _REPO / "uahf/framework/adapters/claude/discovery-data/policy"
_DEFAULT_POLICY = _POLICY_DIR / "default-policy.yaml"
_LIGHTWEIGHT_POLICY = _POLICY_DIR / "lightweight-policy.yaml"
_SKILL_MD = _REPO / ".claude/skills/discovery-interview/SKILL.md"
_FIXTURE_LEDGER = (_REPO / "orchestration/adapters/claude/tests/fixtures/consumer-ws"
                   / ".claude/project-contract/coverage-ledger.json")

# Part 1 커버리지 맵 표의 절 제목(이 제목 이후 첫 표가 대상).
_MAP_HEADING = "### 커버리지 맵"

# 표 행: | 질문축 | `축-id` | 확인 대상 | 차원 |
# id 셀이 백틱 코드인 행만 축 행으로 본다(하류 위임 행은 `—` 이므로 자연히 제외된다).
_ROW_RE = re.compile(r"^\|([^|]+)\|\s*`([a-z][a-z0-9-]*)`\s*\|", re.MULTILINE)


def _policy_axes(path: Path):
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    return doc["coverage"]["requiredAxes"]


def _skill_rows():
    """SKILL.md 커버리지 맵 표에서 (라벨, id) 쌍을 문서 순서대로 뽑는다."""
    text = _SKILL_MD.read_text(encoding="utf-8")
    seg = text.split(_MAP_HEADING, 1)
    if len(seg) != 2:
        raise AssertionError("SKILL.md 에 %r 절이 없다" % _MAP_HEADING)
    body = seg[1].split("\n### ", 1)[0]
    rows = []
    for label_cell, axis_id in _ROW_RE.findall(body):
        label = label_cell.replace("*", "").strip()
        rows.append((label, axis_id))
    return rows


class TestSkillAxisBinding(unittest.TestCase):
    """SKILL.md Part 1 표 ↔ 정책 `coverage.requiredAxes` 결속."""

    @classmethod
    def setUpClass(cls) -> None:
        for p in (_DEFAULT_POLICY, _SKILL_MD):
            if not p.exists():
                raise unittest.SkipTest("대조 대상 부재: %s" % p)
        cls.axes = _policy_axes(_DEFAULT_POLICY)
        cls.rows = _skill_rows()

    def test_S1_row_count_matches(self) -> None:
        self.assertEqual(len(self.rows), len(self.axes),
                         "축 행 수 드리프트 — SKILL.md %d행 vs 정책 %d축 (표 %r)"
                         % (len(self.rows), len(self.axes), [r[1] for r in self.rows]))

    def test_S2_ids_match_in_order(self) -> None:
        doc_ids = [r[1] for r in self.rows]
        pol_ids = [a["id"] for a in self.axes]
        self.assertEqual(doc_ids, pol_ids,
                         "축 id 드리프트(순서 포함) — SKILL.md %r vs 정책 %r" % (doc_ids, pol_ids))

    def test_S3_labels_match(self) -> None:
        # 라벨은 표기(굵게)만 벗기면 정책 `label` 과 문자 단위로 같아야 한다.
        doc_labels = [r[0] for r in self.rows]
        pol_labels = [a["label"] for a in self.axes]
        self.assertEqual(doc_labels, pol_labels,
                         "축 라벨 드리프트 — SKILL.md %r vs 정책 %r" % (doc_labels, pol_labels))

    def test_S4_no_stray_axis_id_outside_the_table(self) -> None:
        # 표 밖 본문에 축 id 를 재열거하면 통제되지 않는 3번째 사본이 된다(사본 금지 규율).
        text = _SKILL_MD.read_text(encoding="utf-8")
        body = text.split(_MAP_HEADING, 1)[1]
        outside = text.split(_MAP_HEADING, 1)[0] + body.split("\n### ", 1)[1]
        for axis in self.axes:
            self.assertNotIn(axis["id"], outside,
                             "축 id %r 이 커버리지 맵 표 밖 본문에 재열거됐다(통제 밖 사본)"
                             % axis["id"])

    def test_S5_profiles_agree(self) -> None:
        # 두 프로파일의 축 집합이 동일해야 SKILL.md 표 하나가 양쪽을 대표할 수 있다
        # (discovery-binding §8.3 (b) `coverage` 행 = 동일 값).
        if not _LIGHTWEIGHT_POLICY.exists():
            self.skipTest("경량 프로파일 부재")
        lw = [(a["id"], a["label"]) for a in _policy_axes(_LIGHTWEIGHT_POLICY)]
        std = [(a["id"], a["label"]) for a in self.axes]
        self.assertEqual(lw, std, "프로파일 간 축 집합 드리프트 — 경량 %r vs 표준 %r" % (lw, std))


class TestFixtureLedgerConformance(unittest.TestCase):
    """픽스처 원장 ↔ 정책 결속 — 픽스처 Contract 수정이 백스톱에 막히지 않게 유지한다."""

    @classmethod
    def setUpClass(cls) -> None:
        for p in (_DEFAULT_POLICY, _FIXTURE_LEDGER):
            if not p.exists():
                raise unittest.SkipTest("대조 대상 부재: %s" % p)
        cls.ledger = json.loads(_FIXTURE_LEDGER.read_text(encoding="utf-8"))

    def test_X1_policy_ref_resolves(self) -> None:
        ref = self.ledger.get("policyRef")
        self.assertIsInstance(ref, str)
        self.assertTrue((_POLICY_DIR / ("%s-policy.yaml" % ref)).exists(),
                        "픽스처 원장 policyRef=%r 이 해소되지 않는다" % (ref,))

    def test_X2_covers_every_policy_axis(self) -> None:
        ref = self.ledger["policyRef"]
        pol_ids = [a["id"] for a in _policy_axes(_POLICY_DIR / ("%s-policy.yaml" % ref))]
        led_ids = [a["id"] for a in self.ledger["axes"]]
        self.assertEqual(sorted(led_ids), sorted(pol_ids),
                         "픽스처 원장 축 드리프트 — 원장 %r vs 정책 %r" % (led_ids, pol_ids))

    def test_X3_checker_passes(self) -> None:
        # 결속의 최종 근거는 결정적 체커다 — 형식 대조가 아니라 실판정으로 확인한다.
        import sys
        sys.path.insert(0, str(_TEST_FILE.parents[1]))
        from coverage_check import check_coverage  # noqa: E402
        policy = _POLICY_DIR / ("%s-policy.yaml" % self.ledger["policyRef"])
        errors = check_coverage(policy, _FIXTURE_LEDGER)
        self.assertEqual(errors, [], "픽스처 원장이 체커를 통과하지 못한다: %r" % (errors,))


if __name__ == "__main__":
    unittest.main()
