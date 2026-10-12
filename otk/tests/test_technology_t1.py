"""Phase 7 Technology wave T1 — the ว 4 outcomes multiple choice can test in full.

Filing and stages are checked structurally by ``test_science_curriculum.py`` and
``test_science_stage_registry.py``; this file checks what is particular to the
technology sets: each is filed under a ``ว 4`` outcome that the interaction
classification marks ``full``, each clears the same 25-question variety floor
Wave H set for the sciences, and the authored tables answer only one way.
"""

from __future__ import annotations

import csv
from pathlib import Path
from random import Random


from otk.core import REGISTRY, catalog, generate
from otk.core.curriculum_science import (
    REVIEW_PENDING,
    SCIENCE_PLACEMENTS,
    SCIENCE_TECHNOLOGY_KEYS,
)
from otk.sets.design_technology.m1 import technology_concept as t1
from otk.sets.design_technology.m2.technology_trend import CHOICES, EFFECTS, SIDES, TRENDS

ROOT = Path(__file__).resolve().parents[2]


def _interaction() -> dict[str, dict]:
    with (ROOT / "docs/for_admin/technology_ipst_interaction.csv").open(
        encoding="utf-8", newline="",
    ) as handle:
        return {row["outcome_code"]: row for row in csv.DictReader(handle)}


def _answer(question) -> str:
    return " ".join(b.text for b in question.choices[question.answer].content)


def _stem(question) -> str:
    return " ".join(getattr(b, "text", "") for b in question.stem).strip()


# ── filing ────────────────────────────────────────────────────────────────────

def test_the_classification_covers_every_technology_outcome_once():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        official = [row["outcome_code"] for row in csv.DictReader(handle)
                    if row["standard_or_group"].startswith("ว 4")]
    rows = _interaction()
    assert list(rows) == official
    assert {row["mc_scope"] for row in rows.values()} == {"full", "partial", "none"}


def _mapping_notes() -> dict[str, str]:
    with (ROOT / "docs/for_admin/science_ipst_mapping.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        return {row["key"]: row["review_note"] for row in csv.DictReader(handle)}


def test_technology_sets_claim_only_testable_outcomes():
    """``full`` outcomes are tested whole; a ``partial`` one only by a set that
    says, in its reviewed filing, that it takes the knowledge half. ``none``
    outcomes are never claimed."""
    rows, notes = _interaction(), _mapping_notes()
    for key in SCIENCE_TECHNOLOGY_KEYS:
        spec = SCIENCE_PLACEMENTS[key]
        assert spec.strand_code == "ว 4", key
        for code in spec.indicator_codes:
            scope = rows[code]["mc_scope"]
            assert scope in {"full", "partial"}, (key, code)
            if scope == "partial":
                assert "knowledge half" in notes[key], key


def test_technology_sets_are_awaiting_review():
    assert REVIEW_PENDING["Phase 7 Technology"] == SCIENCE_TECHNOLOGY_KEYS


def test_every_outcome_touched_has_all_three_stages():
    stages: dict[str, set[int]] = {}
    for row in catalog():
        if row["key"] in SCIENCE_TECHNOLOGY_KEYS:
            for code in row["indicator_codes"]:
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert stages and all(found == {1, 2, 3} for found in stages.values()), stages


def test_design_sets_carry_their_own_subject():
    for key in SCIENCE_TECHNOLOGY_KEYS:
        if SCIENCE_PLACEMENTS[key].standard_code == "ว 4.1":
            assert REGISTRY[key].subject == "การออกแบบและเทคโนโลยี", key


# ── slice 1: ว 4.1 ม.1/1 and ม.2/1 ────────────────────────────────────────────

def test_system_parts_are_distinct_and_feedback_splits_the_systems():
    for system in t1.SYSTEMS:
        parts = list(system.parts().values())
        assert len(set(parts)) == len(parts), system.name
    with_feedback = [s for s in t1.SYSTEMS if s.feedback]
    # The fluency set draws three of the other group, so each needs at least three.
    assert len(with_feedback) >= 3 and len(t1.SYSTEMS) - len(with_feedback) >= 3


def test_resources_use_every_kind_once_per_project():
    for project in {r.project for r in t1.RESOURCES}:
        kinds = [r.kind for r in t1.RESOURCES if r.project == project]
        assert sorted(kinds) == sorted(t1.RESOURCE_KINDS), project


def test_every_factor_of_change_has_cases_and_answers_are_unique():
    for factor in t1.FACTORS:
        assert sum(1 for c in t1.CHANGES if c[2] == factor) >= 2, factor
    assert len({c[0] for c in t1.CHANGES}) == len(t1.CHANGES)


def test_effect_sides_are_distinct_and_trend_and_choice_banks_hold_five_wrongs():
    for effect in EFFECTS:
        assert len({effect.of(side) for side in SIDES}) == 3, effect.technology
    for bank in (TRENDS, CHOICES):
        for stem, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, stem


def test_generated_answers_match_the_tables():
    roles = {part: role for s in t1.SYSTEMS for role, part in s.parts().items()}
    factor_of = {f"{c} เพราะ{r}": f for c, r, f in t1.CHANGES}
    for seed in range(300):
        q = generate("tech.technology_concept_fluency", Random(seed))
        stem = _stem(q)
        if "เป็นองค์ประกอบใดของระบบ" in stem:
            part = stem.split("“")[1].split("”")[0]
            assert _answer(q) == roles[part]
        elif "ไม่มีข้อมูลย้อนกลับ" in stem:
            assert not next(s for s in t1.SYSTEMS if s.name == _answer(q)).feedback
        else:
            assert next(s for s in t1.SYSTEMS if s.name == _answer(q)).feedback
        q = generate("tech.technology_concept_application", Random(seed))
        stem = _stem(q)
        if stem.startswith("ข้อใดเป็นการเปลี่ยนแปลง"):
            assert factor_of[_answer(q)] in stem
        else:
            change = stem.split("“")[1].split("”")[0]
            assert _answer(q) == next(f for c, _, f in t1.CHANGES if c == change)


# ── slice 2: ว 4.1 ม.3/1 and ม.4/1 ────────────────────────────────────────────

def test_link_tables_pair_each_technology_and_problem_with_one_knowledge():
    from otk.sets.design_technology.m3 import technology_link as t2
    for table in (t2.FOUNDATIONS, t2.PROBLEMS):
        assert len({a for a, _ in table}) == len({b for _, b in table}) == len(table)
    for history in t2.HISTORIES:
        wrongs = (*history.wrongs, *t2.ANY_HISTORY_WRONGS)
        assert len(set(wrongs)) == len(wrongs) and history.analysis not in wrongs


def test_impact_tables_keep_sides_apart_and_remedies_unique():
    from otk.sets.design_technology.m4 import technology_impact as t2
    for technology, effects in t2.IMPACTS.items():
        assert set(effects) <= set(t2.DIMENSIONS) and len(effects) >= 3, technology
        assert len(set(effects.values())) == len(effects), technology
    assert len({r for _, _, r in t2.REMEDIES}) == len(t2.REMEDIES)
    for proposal, correct, wrongs in t2.PROPOSALS:
        assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, proposal


def test_impact_answers_match_the_table():
    from otk.sets.design_technology.m4 import technology_impact as t2
    side_of = {text: side for effects in t2.IMPACTS.values() for side, text in effects.items()}
    for seed in range(300):
        q = generate("tech.technology_impact_foundation", Random(seed))
        stem = _stem(q)
        if stem.startswith("“"):
            assert _answer(q) == side_of[stem.split("“")[1].split("”")[0]]
        else:
            assert stem.endswith(f"ด้าน{side_of[_answer(q)]}")


# ── slice 3: ว 4.2 ป.1/1, /2 and /5 ───────────────────────────────────────────

def test_computing_sets_carry_their_own_subject():
    for key in SCIENCE_TECHNOLOGY_KEYS:
        if SCIENCE_PLACEMENTS[key].standard_code == "ว 4.2":
            assert REGISTRY[key].subject == "วิทยาการคำนวณ", key


def test_steps_are_unique_across_tasks_and_stories_across_methods():
    from otk.sets.computing.p1 import safe_use as t3
    from otk.sets.computing.p1.simple_problem import NOT_SOLVING, STORIES
    from otk.sets.computing.p1.task_steps import TASKS
    steps = [step for task in TASKS.values() for step in task]
    assert len(set(steps)) == len(steps) and all(len(t) == 4 for t in TASKS.values())
    stories = [s for group in STORIES.values() for s in group] + list(NOT_SOLVING)
    assert len(set(stories)) == len(stories)
    assert not set(t3.SAFE) & set(t3.UNSAFE)
    for situation, correct, wrongs in t3.SITUATIONS:
        assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, situation


def test_trial_and_order_answers_recompute():
    from otk.sets.computing.p1 import task_steps as t3
    for seed in range(300):
        q = generate("comp.simple_problem_fluency", Random(seed))
        stem = _stem(q)
        count = int(stem.split(" ")[1])
        if "อย่างมากกี่ครั้ง" in stem:
            assert _answer(q) == f"{count - 1} ครั้ง"
        else:
            failed = {int(n) for n in stem.split("พบว่า")[1].split("ใช้ไม่ได้")[0].split()
                      if n.isdigit()}
            (left,) = set(range(1, count + 1)) - failed
            assert _answer(q).endswith(f"ที่ {left}")
        q = generate("comp.task_steps_fluency", Random(seed))
        stem = _stem(q)
        task = stem.split("ขั้นตอนการ")[1].split("ต่อไปนี้")[0]
        label = {s: stem.split(f") {s}")[0][-1] for s in t3.TASKS[task]}
        assert _answer(q) == " → ".join(label[s] for s in t3.TASKS[task])


# ── slice 4: ว 4.2 ป.2/1, ป.2/4, ป.3/1 and ป.3/5 ─────────────────────────────

def test_arrow_answers_recompute():
    from otk.sets.computing.p2 import arrow_steps as t4
    for seed in range(300):
        q = generate("comp.arrow_steps_fluency", Random(seed))
        seq = _stem(q).split("ตามลูกศร ")[1].split(" เมื่อเดินครบ")[0].split()
        dx = sum(t4.MOVE[s][0] for s in seq)
        dy = sum(t4.MOVE[s][1] for s in seq)
        assert _answer(q) == t4._where(dx, dy)
        q = generate("comp.arrow_steps_application", Random(seed))
        stem = _stem(q)
        seq = stem.split("เขียนลูกศรเป็น ")[1].split(" ลูกศรตัวใด")[0].split()
        wanted = {t4.RIGHT, t4.LEFT, t4.UP, t4.DOWN} & set(
            d for d, word in t4.SAY.items() if f"เดิน{word}" in stem)
        bad = [i for i, s in enumerate(seq, 1) if s not in wanted]
        assert len(bad) == 1 and _answer(q) == f"ลูกศรตัวที่ {bad[0]}"


def test_repeat_and_condition_answers_recompute():
    for seed in range(300):
        q = generate("comp.algorithm_repeat_fluency", Random(seed))
        stem = _stem(q)
        rounds = int(stem.split("ทำซ้ำ ")[1].split(" ")[0])
        action = stem.split("จะ")[-1].split("ทั้งหมด")[0]
        each = int(stem.split(f"{action} ")[1].split(" ")[0])
        assert _answer(q).split()[0] == str(each * rounds)
        q = generate("comp.algorithm_condition_application", Random(seed))
        stem = _stem(q)
        blocks = stem.split("ได้แก่ ")[1].split(" อัลกอริทึม")[0].split()
        rule = stem.split("ถ้าเป็น")[1].split(" ให้ใส่")[0]
        box_a = stem.endswith("กล่อง ก มีตัวต่อกี่ชิ้น")
        expected = blocks.count(rule) if box_a else len(blocks) - blocks.count(rule)
        assert _answer(q) == f"{expected} ชิ้น"


def test_care_and_internet_tables_do_not_overlap():
    from otk.sets.computing.p3 import internet_rules as t4
    from otk.sets.computing.p2.device_care import AGREEMENTS, CARE_SITUATIONS
    assert not set(t4.PRIVATE) & set(t4.SHAREABLE)
    for table in (AGREEMENTS, t4.INTERNET_RULES):
        assert len({a for a, _ in table}) == len({b for _, b in table}) == len(table)
    for bank in (CARE_SITUATIONS, t4.ONLINE_SITUATIONS):
        for situation, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, situation


# ── slice 5: ว 4.2 ป.4/1, ป.5/1 and ป.6/1 ─────────────────────────────────────

def test_halving_counts_match_a_brute_force_search():
    from otk.sets.computing.p6 import logic_design as t5

    def worst(top):
        def guesses(low, high):
            if low > high:
                return 0
            mid = t5.middle(low, high)
            return 1 + max(guesses(low, mid - 1), guesses(mid + 1, high))
        return guesses(1, top)

    for top in (7, 15, 16, 20, 25, 30, 31, 32, 40, 50, 60, 63, 64, 80, 100):
        assert t5.most_guesses(top) == worst(top), top


def test_logic_answers_recompute():
    from otk.sets.computing.p4 import logic_rule as t5
    from otk.sets.computing.p6.logic_design import middle
    for seed in range(300):
        q = generate("comp.logic_conditions_foundation", Random(seed))
        stem = _stem(q)
        n = int(stem.split("ถึง ")[1].split(" ")[0])
        d = int(stem.split("หารด้วย ")[1].split(" ")[0])
        hits = n // d
        expected = hits if "ไม่ลงตัว" not in stem else n - hits
        assert _answer(q) == f"{expected} ครั้ง"

        q = generate("comp.logic_design_fluency", Random(seed))
        stem = _stem(q)
        top = int(stem.split("ตั้งแต่ 1 ถึง ")[1].split(" ")[0])
        first = int(stem.split("ครั้งแรกทาย ")[1].split(" ")[0])
        assert first == middle(1, top)
        low, high = (first + 1, top) if "มากกว่า" in stem.split("เพื่อนตอบว่า")[1] else (1, first - 1)
        assert _answer(q) == str(middle(low, high))

        q = generate("comp.logic_rule_application", Random(seed))
        stem = _stem(q)
        start = int(stem.split("ใส่เลข ")[1].split(" ")[0])
        rounds = int(stem.split("ทำงาน ")[1].split(" ")[0])
        machine = next(m for m in t5.MACHINES
                       if f"จำนวนคู่ ให้{m[0][0]} ถ้าเป็นจำนวนคี่ ให้{m[1][0]} " in stem)
        assert _answer(q) == str(t5.run_machine(machine, start, rounds))


def test_design_rules_hold_five_wrongs():
    from otk.sets.computing.p4 import logic_rule as t5
    from otk.sets.computing.p6.logic_design import DESIGNS
    for device, rule, wrongs in DESIGNS:
        assert len(set(wrongs)) == len(wrongs) == 5 and rule not in wrongs, device
    assert len({r[0] for r in t5.RULES}) == len(t5.RULES)


# ── slice 6: ว 4.2 ป.4/5, ป.5/5 and ป.6/4 ─────────────────────────────────────

def test_rights_manners_and_teamwork_tables_hold_up():
    from otk.sets.computing.p6 import online_teamwork as t6
    from otk.sets.computing.p5.netiquette import COURTESIES, GROUP_CHATS, IMPOLITE, POLITE
    from otk.sets.computing.p4.digital_rights import (
        REPORTING,
        RESPECT,
        RIGHTS,
        VIOLATE,
        VIOLATIONS,
    )
    for good, bad in ((RESPECT, VIOLATE), (POLITE, IMPOLITE),
                      (t6.SAFE_TEAMWORK, t6.UNSAFE_TEAMWORK)):
        assert len(good) >= 4 and len(bad) >= 4 and not set(good) & set(bad)
    for labels, rows in ((RIGHTS, VIOLATIONS), (t6.PERMISSIONS, t6.NEEDS)):
        assert {label for _, label in rows} == set(labels)
        assert all(sum(1 for _, label in rows if label == x) >= 1 for x in labels)
        assert len({text for text, _ in rows}) == len(rows)
    assert len({a for a, _ in COURTESIES}) == len({b for _, b in COURTESIES}) == len(COURTESIES)
    for bank in (REPORTING, GROUP_CHATS, t6.TEAM_TROUBLES):
        for situation, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, situation


def test_permission_and_right_answers_match_their_tables():
    from otk.sets.computing.p6 import online_teamwork as t6
    from otk.sets.computing.p4.digital_rights import VIOLATIONS
    need_of = dict(t6.NEEDS)
    right_of = dict(VIOLATIONS)
    for seed in range(300):
        q = generate("comp.online_teamwork_fluency", Random(seed))
        stem = _stem(q)
        if stem.startswith("ควรให้สิทธิ์ใดกับ"):
            who = stem.removeprefix("ควรให้สิทธิ์ใดกับ").split(" ในไฟล์งานกลุ่ม")[0]
            assert _answer(q) == need_of[who]
        else:
            permission = (t6.NO_ACCESS if stem.startswith("ใครที่ไม่ควร")
                          else stem.split("สิทธิ์")[1].split("ในไฟล์งานกลุ่ม")[0])
            assert need_of[_answer(q)] == permission
        q = generate("comp.digital_rights_fluency", Random(seed))
        stem = _stem(q)
        if stem.startswith("“"):
            assert _answer(q) == right_of[stem.split("“")[1].split("”")[0]]
        else:
            assert right_of[_answer(q)] in stem


# ── slice 7: ว 4.2 ม.1/4, ม.2/3, ม.2/4, ม.3/3 and ม.3/4 ───────────────────────

def test_strong_passwords_meet_the_stated_rule():
    from otk.sets.computing.m1 import safe_terms as t7
    for seed in range(200):
        rng = Random(seed)
        strong = t7.strong_password(rng)
        assert len(strong) >= 12
        assert any(c.isupper() for c in strong) and any(c.islower() for c in strong)
        assert any(c.isdigit() for c in strong) and any(not c.isalnum() for c in strong)
        for weak in t7.weak_passwords(rng):
            assert len(weak) < 12 or weak.isalnum()


def test_transfer_and_size_answers_recompute():
    for seed in range(300):
        q = generate("comp.computer_system_fluency", Random(seed))
        stem = _stem(q)
        if stem.startswith("ไฟล์ขนาด"):
            size = int(stem.split("ไฟล์ขนาด ")[1].split(" ")[0])
            assert _answer(q) == f"{size * 8} เมกะบิต"
        else:
            size = int(stem.split("ส่งไฟล์ขนาด ")[1].split(" ")[0])
            speed = int(stem.split("ความเร็ว ")[1].split(" ")[0])
            assert size * 8 % speed == 0
            assert _answer(q) == f"{size * 8 // speed} วินาที"


def test_licence_cases_have_one_right_answer():
    from otk.sets.computing.m2 import work_licence as t7
    assert t7.LICENCE_CASES
    for licence, use in t7.LICENCE_CASES:
        assert len(t7.licence_failures(licence, use)) <= 1
    # Every reason is reachable, and so is "allowed".
    reached = {tuple(t7.licence_failures(ell, u)) for ell, u in t7.LICENCE_CASES}
    assert reached == {(), ("BY",), ("NC",), ("ND",), ("SA",)}
    assert {e for _, e in t7.WISHES} == set(t7.ELEMENTS)


def test_secondary_tables_hold_up():
    from otk.sets.computing.m3 import computer_law as t7
    from otk.sets.computing.m2.work_licence import PUBLISHING
    from otk.sets.computing.m3.info_credibility import FALSE_NEWS, RELIABLE, SOURCES, UNRELIABLE
    from otk.sets.computing.m1.safe_terms import GENUINE, SCAMS, TERMS_SITUATIONS
    from otk.sets.computing.m2.computer_system import DEVICES, LINKS, PARTS, UNITS
    for good, bad in ((SCAMS, GENUINE), (RELIABLE, UNRELIABLE),
                      (t7.LAWFUL, t7.OFFENCES), (t7.FAIR, t7.UNFAIR)):
        assert not set(good) & set(bad) and len(good) >= 4 and len(bad) >= 4
    assert {u for _, u in DEVICES} == set(UNITS)
    for _, parts in LINKS:
        assert set(parts) == set(PARTS) and len(set(parts.values())) == 5
    for bank in (TERMS_SITUATIONS, SOURCES, FALSE_NEWS, PUBLISHING, t7.LAW_SITUATIONS):
        for situation, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, situation


def test_t1_covers_every_fully_testable_outcome():
    """The closing condition of wave T1."""
    full = {code for code, row in _interaction().items() if row["mc_scope"] == "full"}
    claimed = {code for key in SCIENCE_TECHNOLOGY_KEYS
               for code in SCIENCE_PLACEMENTS[key].indicator_codes}
    assert full <= claimed and len(full) == 22


# ── wave T2 slice 1: ว 4.1 ม.1/2-ม.1/5, knowledge halves ─────────────────────

def test_design_process_tables_hold_up():
    from otk.sets.design_technology.m1 import problem_finding as s1
    from otk.sets.design_technology.m1.materials_tools import MATERIAL_NEEDS, SAFE_USE, TOOLS
    from otk.sets.design_technology.m1.solution_design import PLANS, PRESENTATIONS
    from otk.sets.design_technology.m1.prototype_testing import FIXES
    assert len(s1.DESIGN_STEPS) == 6 and set(s1.ACTIVITIES) == set(range(6))
    activities = [a for pair in s1.ACTIVITIES.values() for a in pair]
    assert len(set(activities)) == len(activities)
    steps = [s for plan in PLANS.values() for s in plan]
    assert len(set(steps)) == len(steps)
    for table in (FIXES, TOOLS, MATERIAL_NEEDS):
        assert len({a for a, _ in table}) == len(table)
    for table in (FIXES, TOOLS):
        assert len({b for _, b in table}) == len(table)
    for bank in (s1.PROBLEMS, PRESENTATIONS, SAFE_USE):
        for stem, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, stem
    # INFORMATION pairs unneeded facts two by two, as the answer names two, so
    # it holds six facts (three disjoint pairs) rather than five wrongs.
    for stem, correct, facts in s1.INFORMATION:
        assert len(set(facts)) == len(facts) == 6 and correct not in facts, stem


def test_design_answers_recompute():
    import re
    for seed in range(300):
        q = generate("tech.solution_design_foundation", Random(seed))
        stem = _stem(q)
        cap = int(re.search(r"ราคาไม่เกิน (\d+)", stem).group(1))
        need = int(re.search(r"อย่างน้อย (\d+)", stem).group(1))
        options = re.findall(r"แบบ (\S) ราคา (\d+) บาท \S+ (\d+)", stem)
        fits = [ell for ell, p, a in options if int(p) <= cap and int(a) >= need]
        assert len(fits) == 1 and _answer(q) == f"แบบ {fits[0]}"

        q = generate("tech.prototype_testing_application", Random(seed))
        stem = _stem(q)
        runs = [int(n) for n in re.findall(r"(\d+) ซม\.", stem.split("เกณฑ์")[0])]
        need = int(re.search(r"ไม่น้อยกว่า (\d+)", stem).group(1))
        mean = sum(runs) // 3
        assert sum(runs) == 3 * mean
        assert _answer(q) == f"ค่าเฉลี่ย {mean} ซม. {'ผ่านเกณฑ์' if mean >= need else 'ไม่ผ่านเกณฑ์'}"

        q = generate("tech.materials_tools_application", Random(seed))
        stem = _stem(q)
        if stem.startswith("เฟืองขับ"):
            driver, driven, turns = (int(n) for n in re.findall(r"(\d+)", stem)[:3])
            assert _answer(q) == f"{turns * driver // driven} รอบ" and turns * driver % driven == 0


# ── wave T2 slice 2: ว 4.1 ม.2/2-ม.2/5, knowledge halves ─────────────────────

def test_m2_tables_hold_up():
    from otk.sets.design_technology.m2 import electronics_mechanism as s2
    from otk.sets.design_technology.m2.constrained_testing import EXPLANATIONS, FAIR_TESTS
    from otk.sets.design_technology.m2.community_problem import FRAMES, FRAME_PARTS, GATHERING
    for frame in FRAMES:
        assert set(frame) == set(FRAME_PARTS) and len(set(frame.values())) == 4
    for table in (GATHERING, s2.COMPONENTS, s2.MECHANISMS):
        assert len({a for a, _ in table}) == len({b for _, b in table}) == len(table)
    assert set(s2.ElectronicsMechanismApplication.USES) == {n for n, _ in s2.MECHANISMS}
    for bank in (FAIR_TESTS, EXPLANATIONS):
        for stem, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, stem


def test_m2_answers_recompute():
    import re
    from otk.sets.design_technology.m2 import electronics_mechanism as s2
    from otk.sets.design_technology.m2.constrained_testing import ALL_PASS
    from otk.sets.design_technology.m2.constrained_design import weighted
    for seed in range(300):
        q = generate("tech.electronics_mechanism_fluency", Random(seed))
        bands = _stem(q).split("เป็น ")[1].split(" ทอง")[0].split()
        a, b, m = (s2.COLOURS.index(c) for c in bands)
        assert _answer(q) == s2.ohms((10 * a + b) * 10 ** m)

        q = generate("tech.constrained_design_foundation", Random(seed))
        stem = _stem(q)
        budget = int(re.search(r"งบประมาณ (\d+)", stem).group(1))
        total = sum(int(n) * int(p) for n, p in re.findall(r"(\d+) \S+ \S+ละ (\d+) บาท", stem))
        expected = budget - total if "เหลือเงิน" in stem else total - budget
        assert expected >= 0 and _answer(q) == f"{expected} บาท"

        q = generate("tech.constrained_design_application", Random(seed))
        stem = _stem(q)
        totals = {}
        for label, body in re.findall(r"แบบ (\S) ได้ (.*?) คะแนน", stem):
            scores = [int(n) for n in re.findall(r"(\d+)", body)]
            totals[label] = weighted(scores)
        assert _answer(q) == f"แบบ {max(totals, key=totals.get)}"

        q = generate("tech.constrained_testing_foundation", Random(seed))
        stem = _stem(q)
        load, price, width = (int(n) for n in re.findall(r"(\d+)", stem.split("ผลการทดสอบ")[0])[:3])
        got = [int(n) for n in re.findall(r"(\d+)", stem.split("ผลการทดสอบ")[1])[:3]]
        fails = [name for name, ok in (("รับน้ำหนัก", got[0] >= load), ("ราคา", got[1] <= price),
                                       ("ความกว้าง", got[2] <= width)) if not ok]
        assert len(fails) <= 1
        assert _answer(q) == (f"ไม่ผ่านเงื่อนไขเรื่อง{fails[0]}" if fails else ALL_PASS)


# ── wave T2 slice 3: ว 4.1 ม.3/2-ม.3/5, knowledge halves ─────────────────────

def test_m3_tables_hold_up():
    from otk.sets.design_technology.m3 import occupation_problem as s3
    from otk.sets.design_technology.m3.fit_for_job import CIRCUITS, JOINS
    from otk.sets.design_technology.m3.test_reasoning import REASONS
    from otk.sets.design_technology.m3.design_presentation import TECHNIQUES
    assert {k for _, k in s3.IP_ITEMS} == set(s3.IP_KINDS)
    for table in (s3.IP_ITEMS, TECHNIQUES, JOINS):
        assert len({a for a, _ in table}) == len(table)
    for table in (TECHNIQUES, JOINS):
        assert len({b for _, b in table}) == len(table)
    for bank in (s3.IP_USES, REASONS, CIRCUITS):
        for stem, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, stem
    # TRADES pairs unhelpful facts like INFORMATION: six facts, three pairs.
    for stem, correct, facts in s3.TRADES:
        assert len(set(facts)) == len(facts) == 6 and correct not in facts, stem


def test_m3_answers_recompute():
    import re
    from otk.sets.design_technology.m3 import design_presentation as s3
    from otk.sets.design_technology.m3.fit_for_job import _volts
    for seed in range(300):
        q = generate("tech.design_presentation_fluency", Random(seed))
        stem = _stem(q)
        w, d, h = (int(n) for n in re.findall(r"(\d+) เซนติเมตร", stem)[:3])
        dims = {"width": w, "depth": d, "height": h}
        view = next(v for v in s3.VIEWS if f"ภาพฉาย{v}" in stem)
        a, b = s3.VIEWS[view]
        assert _answer(q) == s3._size(dims[a], dims[b])

        q = generate("tech.design_presentation_application", Random(seed))
        stem = _stem(q)
        cut, wire, build = (int(n) for n in re.findall(r"(\d+) นาที", stem))
        hh, mm = (int(n) for n in re.search(r"เริ่มเวลา (\d+):(\d+)", stem).groups())
        assert _answer(q) == s3._clock(hh * 60 + mm + max(cut, wire) + build)

        q = generate("tech.test_reasoning_fluency", Random(seed))
        before, after = (int(n) for n in re.findall(r"(\d+) นิวตัน", _stem(q)))
        assert _answer(q) == f"ร้อยละ {(after - before) * 100 // before}"
        assert (after - before) * 100 % before == 0

        q = generate("tech.fit_for_job_fluency", Random(seed))
        stem = _stem(q)
        cell = float(re.search(r"ขนาด ([\d.]+) โวลต์", stem).group(1))
        if "แบบอนุกรม จะได้" in stem:
            count = int(re.search(r"จำนวน (\d+) ก้อน", stem).group(1))
            assert _answer(q) == _volts(cell * count)
        elif "แบบขนาน" in stem:
            assert _answer(q) == _volts(cell)
        else:
            target = float(re.search(r"ต้องการแรงดัน ([\d.]+)", stem).group(1))
            assert _answer(q) == f"{round(target / cell)} ก้อน"


# ── wave T2 slice 4: ว 4.1 ม.4/2-ม.4/5, knowledge halves ─────────────────────

def test_m4_tables_hold_up():
    from otk.sets.design_technology.m4 import control_system as s4
    from otk.sets.design_technology.m4.cad_design import CAD_USES, SOFTWARE
    from otk.sets.design_technology.m4.complex_problem import CHAINS, DECOMPOSITIONS, SYNTHESES
    from otk.sets.design_technology.m4.product_evaluation import EXTENSIONS
    for chain in CHAINS:
        assert len(set(chain)) == len(chain) == 5
    assert {r for _, r in s4.SYSTEM_PARTS} == set(s4.ROLES)
    for table in (SOFTWARE, EXTENSIONS, s4.SENSORS):
        assert len({a for a, _ in table}) == len({b for _, b in table}) == len(table)
    for bank in (DECOMPOSITIONS, SYNTHESES, CAD_USES, s4.AUTOMATIONS):
        for stem, correct, wrongs in bank:
            assert len(set(wrongs)) == len(wrongs) == 5 and correct not in wrongs, stem


def test_m4_answers_recompute():
    import re
    from otk.sets.design_technology.m4 import product_evaluation as s4
    for seed in range(300):
        q = generate("tech.cad_design_fluency", Random(seed))
        stem = _stem(q)
        scale = int(re.search(r"1 : (\d+)", stem).group(1))
        if stem.startswith("แบบชิ้นงาน"):          # drawing to real
            drawn = int(re.search(r"ความยาวในแบบเป็น (\d+)", stem).group(1))
            assert _answer(q) == f"{drawn * scale} เซนติเมตร"
        else:
            real = int(re.search(r"ยาวจริง (\d+)", stem).group(1))
            assert real % scale == 0 and _answer(q) == f"{real // scale} เซนติเมตร"

        q = generate("tech.product_evaluation_foundation", Random(seed))
        stem = _stem(q)
        scores = {c: int(re.search(rf"{c} (\d+)", stem).group(1)) for c in s4.RUBRIC}
        if "ร้อยละ" in stem:
            total = sum(scores.values())
            assert total % 2 == 0 and _answer(q) == f"ร้อยละ {total * 100 // 40}"
        else:
            assert _answer(q) == min(scores, key=scores.get)

        q = generate("tech.product_evaluation_application", Random(seed))
        stem = _stem(q)
        a = [int(n) for n in stem.split("แบบ ก ได้ ")[1].split(" แบบ ข")[0].split()]
        b = [int(n) for n in stem.split("แบบ ข ได้ ")[1].split(" แบบใด")[0].split()]
        if "สม่ำเสมอ" in stem:
            expected = "แบบ ก" if max(a) - min(a) < max(b) - min(b) else "แบบ ข"
        else:
            expected = "แบบ ก" if sum(a) > sum(b) else "แบบ ข"
        assert _answer(q) == expected


def test_t2_covers_every_partial_design_outcome():
    """The closing condition of wave T2: every partial ว 4.1 outcome has its knowledge half."""
    partial = {code for code, row in _interaction().items()
               if row["mc_scope"] == "partial" and code.startswith("ว 4.1")}
    claimed = {code for key in SCIENCE_TECHNOLOGY_KEYS for code in SCIENCE_PLACEMENTS[key].indicator_codes}
    assert partial <= claimed and len(partial) == 16


# ── wave T3 slice 1: drawn block programs, ป.1/3, ป.2/2, ป.3/2 ─────────────────

def _program(q):
    from otk.sets._support import block_programs as bp
    asset = q.stem[0].asset_id
    return next(s for s in bp.BLOCK_PROGRAM_SPECS if s.asset_id == asset)


def test_block_program_specs_are_valid_and_unique():
    import re
    from otk.sets._support import block_programs as bp
    ids = [s.asset_id for s in bp.BLOCK_PROGRAM_SPECS]
    assert len(ids) == len(set(ids))
    for spec in bp.BLOCK_PROGRAM_SPECS:
        assert re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", spec.asset_id)
        assert all(bp.inside(p) for p in bp.walk(spec.start, spec.blocks))
    for spec in bp.DEBUG:
        bad = [i for i, m in enumerate(spec.blocks, 1)
               if bp.walk(spec.start, spec.blocks[:i - 1] + (bp.OPPOSITE[m],) + spec.blocks[i:])[-1] == spec.target]
        assert (spec.end == spec.target) == (bp.wrong_block(spec) is None)
        if bp.wrong_block(spec):
            assert bad == [bp.wrong_block(spec)]
    for spec in bp.MISSING:
        gap = (spec.target[0] - spec.end[0], spec.target[1] - spec.end[1])
        assert gap in bp.MOVES.values()


def test_block_program_answers_recompute():
    from otk.sets._support import block_programs as bp
    for seed in range(300):
        q = generate("comp.block_basics_fluency", Random(seed))
        assert _answer(q) == bp.cell(_program(q).end)

        q = generate("comp.block_bugs_foundation", Random(seed))
        spec = _program(q)
        assert _answer(q) == (f"ไปถึงดาว หยุดที่ช่อง {bp.cell(spec.target)}" if spec.end == spec.target
                              else f"ไม่ถึงดาว หยุดที่ช่อง {bp.cell(spec.end)}")

        q = generate("comp.block_bugs_fluency", Random(seed))
        assert _answer(q) == f"บล็อกที่ {bp.wrong_block(_program(q))}"

        q = generate("comp.block_trace_foundation", Random(seed))
        k = int(_stem(q).split("บล็อกที่ ")[1].split(" ")[0])
        spec = _program(q)
        assert _answer(q) == bp.cell(bp.walk(spec.start, spec.blocks)[k])

        q = generate("comp.block_basics_application", Random(seed))
        spec = _program(q)
        arrows = {"→": "R", "←": "L", "↑": "U", "↓": "D"}
        moves = [arrows[a] for a in _answer(q).split()]
        assert bp.walk(spec.start, moves)[-1] == spec.target
        for choice in q.choices:
            text = " ".join(b.text for b in choice.content)
            if text != _answer(q):
                assert bp.walk(spec.start, [arrows[a] for a in text.split()])[-1] != spec.target


def test_block_program_sets_always_show_their_picture():
    for key in ("comp.block_basics_foundation", "comp.block_bugs_application", "comp.block_trace_fluency"):
        for seed in range(50):
            q = generate(key, Random(seed))
            assert getattr(q.stem[0], "asset_id", "").startswith("blockprog_"), key


def test_every_block_program_is_a_registered_diagram():
    from otk.core.render.assets import is_diagram
    from otk.sets._support import block_programs as bp
    assert all(is_diagram(spec.asset_id) for spec in bp.BLOCK_PROGRAM_SPECS)


# ── wave T3 slice 2: repeats, a coin rule and everyday robots, ป.4/2-ป.6/2 ────

def test_repeat_blocks_expand_and_coin_runs_split_as_drawn():
    from otk.sets._support import block_programs as bp
    assert bp.expand(("R", "x3UL", "D")) == ["R", "U", "L", "U", "L", "U", "L", "D"]
    for spec in bp.COIN_RUNS:
        landed = set(bp.walk(spec.start, spec.blocks)[1:])
        hits = [c for c in spec.coins if c in landed]
        assert len(spec.coins) == 4 and 1 <= len(hits) <= 3 and spec.start not in spec.coins
    for spec in bp.LOOP_GOALS:
        repeat, turn = spec.blocks
        counts = [k for k in range(1, 8)
                  if bp.walk(spec.start, (f"x{k}{repeat[2:]}", turn))[-1] == spec.target]
        assert len(counts) == 1 and counts[0] != int(repeat[1])


def test_repeat_and_rule_answers_recompute():
    from otk.sets._support import block_programs as bp
    from otk.sets.computing.p5 import block_condition as s2
    for seed in range(300):
        q = generate("comp.block_loop_foundation", Random(seed))
        assert _answer(q) == f"{len(bp.expand(_program(q).blocks))} ช่อง"
        q = generate("comp.block_loop_fluency", Random(seed))
        assert _answer(q) == bp.cell(_program(q).end)
        q = generate("comp.block_condition_foundation", Random(seed))
        assert _answer(q) == f"{len(s2.collected(_program(q)))} เหรียญ"
        q = generate("comp.block_life_foundation", Random(seed))
        spec = _program(q)
        assert _answer(q) == f"{len(set(bp.walk(spec.start, spec.blocks)))} ช่อง"
        q = generate("comp.block_life_fluency", Random(seed))
        spec = _program(q)
        text = _answer(q)
        count = int(text.split("ทำซ้ำ ")[1].split(" ")[0])
        arrows = {"→": "R", "←": "L", "↑": "U", "↓": "D"}
        move = arrows[text.split(": ")[1]]
        assert bp.walk(spec.end, (f"x{count}{move}",))[-1] == spec.start
        q = generate("comp.block_life_application", Random(seed))
        spec = _program(q)
        text = _answer(q)
        count = int(text.split("ทำซ้ำ ")[1].split(" ")[0])
        moves = "".join(arrows[a] for a in text.split(": ")[1].split())
        assert bp.walk(spec.start, (f"x{count}{moves}",))[-1] == spec.target


# ── wave T3 slice 3: drawn flowcharts, ม.1/1 and ม.2/1 ────────────────────────

def _chart(q):
    from otk.sets._support import flowcharts as fc
    asset = q.stem[0].asset_id
    return next(s for s in fc.FLOWCHART_SPECS if s.asset_id == asset)


def _input(q) -> int:
    return int(_stem(q).split("x = ")[1].split(" ")[0])


def _python_run(spec, x, setup=None):
    """The chart run as Python — an independent check on ``flowcharts.run``."""
    env = {"x": x}
    for line in setup or spec.setup:
        exec(line, {}, env)
    passes = 0
    if spec.loop:
        while eval(spec.test, {}, env):
            for line in spec.yes:
                exec(line, {}, env)
            passes += 1
    elif spec.test:
        taken = eval(spec.test, {}, env)
        for line in spec.yes if taken else spec.no:
            exec(line, {}, env)
        passes = int(taken)
    return env[spec.out], passes


def test_flowchart_specs_are_valid_and_unique():
    import re
    from otk.core.render.assets import is_diagram
    from otk.sets._support import flowcharts as fc
    ids = [s.asset_id for s in fc.FLOWCHART_SPECS]
    assert len(ids) == len(set(ids))
    for spec in fc.FLOWCHART_SPECS:
        assert re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", spec.asset_id)
        assert is_diagram(spec.asset_id)
        drawn = [*spec.setup, spec.test, *spec.yes, *spec.no, spec.out]
        assert all(text.isascii() for text in drawn)
        assert all(len(part.split(" = ")[1].split()) in (1, 3) for part in [*spec.setup, *spec.yes, *spec.no])
    for spec in fc.SEQUENCES:
        assert all(fc.run(spec, x).output >= 0 for x in fc.SEQ_INPUTS)
    for spec in fc.LOOPS + fc.SUMS:
        for x in range(0, 41):
            assert fc.run(spec, x)[:2] == _python_run(spec, x)


def test_flowchart_answers_recompute():
    for seed in range(300):
        for key in ("comp.flowchart_trace_foundation", "comp.flowchart_trace_fluency",
                    "comp.flowchart_loop_fluency", "comp.flowchart_loop_application"):
            q = generate(key, Random(seed))
            assert _answer(q) == str(_python_run(_chart(q), _input(q))[0]), key
        q = generate("comp.flowchart_loop_foundation", Random(seed))
        assert _answer(q) == f"{_python_run(_chart(q), _input(q))[1]} รอบ"

        q = generate("comp.flowchart_trace_application", Random(seed))
        spec, x = _chart(q), _input(q)
        shown = int(_stem(q).split("แสดงผลเป็น ")[1].split(" ")[0])
        for choice in q.choices:
            setup = list(spec.setup)
            setup[spec.hole] = " ".join(b.text for b in choice.content)
            fits = _python_run(spec, x, setup)[0] == shown
            assert fits == (" ".join(b.text for b in choice.content) == _answer(q))


def test_flowchart_sets_always_show_their_picture():
    for key in ("comp.flowchart_trace_foundation", "comp.flowchart_trace_application",
                "comp.flowchart_loop_foundation", "comp.flowchart_loop_application"):
        for seed in range(50):
            q = generate(key, Random(seed))
            assert getattr(q.stem[0], "asset_id", "").startswith("flow_"), key


# ── wave T3 slice 4: working with data, ป.1/4, ป.2/3, ป.3/3, ป.3/4 ────────────

def test_data_tables_hold_up():
    from otk.sets.computing.p3 import data_present as s4
    from otk.sets.computing.p2.file_folders import FINDING, FOLDER_SCHEMES, NAMES, POOR_NAMES
    from otk.sets.computing.p3.search_keyword import KEYWORDS, SEARCH_TROUBLE, TOOLS
    from otk.sets.computing.p1.data_store import DEVICES, KEEP, PROGRAMS
    for rows in (DEVICES, PROGRAMS, TOOLS):
        assert len({a for a, _ in rows}) == len(rows) and len({b for _, b in rows}) == len(rows)
    assert {kind for _, kind in s4.SOFTWARE} <= set(s4.SOFTWARE_KINDS)
    assert {step for _, step in s4.STEP_EXAMPLES} == set(s4.STEPS)
    for bank in (KEEP, FINDING, KEYWORDS, SEARCH_TROUBLE, s4.PRESENTATIONS):
        for _, correct, wrongs in bank:
            assert len(set(wrongs)) >= 4 and correct not in wrongs
    for _, folders in FOLDER_SCHEMES:
        files = [f for _, fs in folders for f in fs]
        assert len(files) == len(set(files))
    good = {g for _, g in NAMES}
    assert not good & set(POOR_NAMES)


def test_survey_answers_recompute():
    import re
    for seed in range(300):
        q = generate("comp.data_present_fluency", Random(seed))
        stem = _stem(q)
        counts = {name: int(n) for name, n in re.findall(r"(\S+) (\d+) คน", stem.split("ดังนี้ ")[1])}
        if "ทั้งหมดกี่คน" in stem:
            assert _answer(q) == f"{sum(counts.values())} คน"
        elif "ต่างกันกี่คน" in stem:
            a, b = re.search(r"ผู้ที่เลือก(\S+)กับผู้ที่เลือก(\S+)ต่างกัน", stem).groups()
            assert _answer(q) == f"{abs(counts[a] - counts[b])} คน"
        else:
            pick = max if "มากที่สุด" in stem else min
            assert _answer(q) == pick(counts, key=counts.get)


# ── wave T3 slice 5: searching, judging and sharing online, ป.4/3-ป.6/3 ────────

def test_online_tables_hold_up():
    from otk.sets.computing.p4 import info_evaluate as s5
    from otk.sets.computing.p6.search_operator import OPERATORS, QUERIES, RESULTS
    from otk.sets.computing.p5.online_service import FLAWS, SERVICES
    from otk.sets.computing.p5.online_comm import CHANNELS, EMAIL_PARTS, PASS_ON
    from otk.sets.computing.p4.source_check import DOMAINS, DOUBTFUL, DOUBTS, TRUSTWORTHY
    for rows in (DOMAINS, s5.TOOLS_FOR_JOB, CHANNELS, EMAIL_PARTS, SERVICES, OPERATORS):
        assert len({a for a, _ in rows}) == len(rows) and len({b for _, b in rows}) == len(rows)
    assert not set(TRUSTWORTHY) & set(DOUBTFUL)
    assert not set(s5.INFORMATION) & set(s5.RAW_DATA)
    for bank in (DOUBTS, s5.PURPOSES, PASS_ON, FLAWS, QUERIES, RESULTS):
        for _, correct, wrongs in bank:
            assert len(set(wrongs)) >= 4 and correct not in wrongs
    wants = {"PDF": "filetype:pdf", "หน่วยงานรัฐ": "site:go.th", "มหาวิทยาลัย": "site:ac.th",
             "ตรงตามลำดับ": "“", "ไม่ต้องการ": " -", "ก็ได้": " OR "}
    for need, query, _ in QUERIES:
        used = [op for cue, op in wants.items() if cue in need]
        assert used and all(op in query for op in used), need


def test_form_percentages_recompute():
    import re
    for seed in range(300):
        q = generate("comp.online_service_fluency", Random(seed))
        stem = _stem(q)
        total = int(re.search(r"ทั้งหมด (\d+) คน", stem).group(1))
        counts = {name: int(n) for name, n in re.findall(r"(\S+) (\d+) คน", stem.split("ดังนี้ ")[1])}
        assert sum(counts.values()) == total and len(set(counts.values())) == len(counts)
        picked = re.search(r"ผู้ที่เลือก(\S+)คิดเป็น", stem).group(1)
        assert counts[picked] * 100 % total == 0
        assert _answer(q) == f"ร้อยละ {counts[picked] * 100 // total}"


# ── wave T4: Python programs in a CodeBlock, ม.1/2 and ม.2/2 ──────────────────

def _program_text(q) -> str:
    blocks = [b for b in q.stem if b.kind == "code"]
    assert len(blocks) == 1 and blocks[0].language == "python"
    return blocks[0].code


def _printed(program: str) -> str:
    """Run the program as ordinary Python — independent of ``technology_t4.output``."""
    import contextlib
    import io
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(program, {})
    return " ".join(out.getvalue().split())


def _apply(program: str, change: str) -> str:
    old, new = change.removeprefix("เปลี่ยน ").split(" เป็น ")
    lines = program.split("\n")
    hits = [i for i, line in enumerate(lines) if line.strip() == old]
    assert len(hits) == 1, (old, program)
    indent = lines[hits[0]][: len(lines[hits[0]]) - len(lines[hits[0]].lstrip())]
    lines[hits[0]] = indent + new
    return "\n".join(lines)


def test_code_block_round_trips_through_json():
    from otk.core.content import CodeBlock, code
    from otk.core.question import Question
    q = generate("comp.code_trace_fluency", Random(3))
    again = Question.model_validate_json(q.model_dump_json())
    assert isinstance(again.stem[1], CodeBlock) and again.stem[1] == q.stem[1]
    assert code("print(1)").model_dump() == {"kind": "code", "code": "print(1)", "language": "python"}


def test_traced_programs_print_the_answer():
    for seed in range(300):
        for key in ("comp.code_trace_foundation", "comp.code_trace_fluency",
                    "comp.code_logic_foundation", "comp.code_logic_fluency"):
            q = generate(key, Random(seed))
            program = _program_text(q)
            assert program.isascii()
            assert _printed(program) == _answer(q), (key, program)


def test_exactly_one_offered_change_fixes_the_program():
    import re
    for seed in range(200):
        for key in ("comp.code_trace_application", "comp.code_logic_application"):
            q = generate(key, Random(seed))
            program = _program_text(q)
            want, got = re.search(r"ควรแสดงผล (\S+) แต่แสดงผล (\S+) ", _stem(q)).groups()
            assert _printed(program) == got != want
            for choice in q.choices:
                change = " ".join(b.text for b in choice.content)
                try:
                    fixed = _printed(_apply(program, change)) == want
                except Exception:
                    fixed = False
                assert fixed == (change == _answer(q)), (key, change, program)


# ── wave T3 slice 6: data, decisions and IT in society, ม.1/3-ม.6/1 ───────────

def test_society_tables_hold_up():
    from otk.sets.computing.m6 import it_society as s6
    from otk.sets.computing.m5.value_add import EVIDENCE
    from otk.sets.computing.m1.primary_data import PRIMARY, SECONDARY
    from otk.sets.computing.m3.data_science import CHARTS, STAGES
    for rows in (STAGES, CHARTS, s6.PDPA_TERMS):
        assert len({a for a, _ in rows}) == len(rows) and len({b for _, b in rows}) == len(rows)
    for good, bad in ((PRIMARY, SECONDARY), (s6.SAFE_SHARING, s6.UNSAFE_SHARING)):
        assert not set(good) & set(bad)
    for bank in (EVIDENCE, s6.CHANGES):
        for _, correct, wrongs in bank:
            assert len(set(wrongs)) >= 4 and correct not in wrongs


def test_data_decision_answers_recompute():
    import re
    for seed in range(300):
        q = generate("comp.primary_data_fluency", Random(seed))
        stem = _stem(q)
        values = [int(v) for v in re.search(r"ดังนี้ ([\d ]+) ", stem).group(1).split()]
        expected = sum(values) // 5 if "ค่าเฉลี่ย" in stem else max(values) - min(values)
        assert _answer(q).split()[0] == str(expected)

        q = generate("comp.primary_data_application", Random(seed))
        table = _stem(q).split("ดังนี้ ")[1].split(" ถ้าเลือก")[0].split("; ")
        totals = {row.split(" ได้ ")[0]: sum(int(n) for n in re.findall(r"\d+", row.split(" ได้ ")[1]))
                  for row in table}
        assert len(totals) == 3 and _answer(q) == max(totals, key=totals.get)

        q = generate("comp.data_science_application", Random(seed))
        sales = dict(re.findall(r"(\S+\.) (\d+)", _stem(q).split("ดังนี้ ")[1]))
        sales = {m: int(v) for m, v in sales.items()}
        true_claims = []
        for choice in q.choices:
            claim = " ".join(b.text for b in choice.content)
            if claim.startswith("เดือนที่ขายได้มากที่สุด"):
                ok = claim.split("คือ ")[1] == max(sales, key=sales.get)
            elif claim.startswith("ยอดขายรวม"):
                ok = int(re.search(r"เท่ากับ (\d+)", claim).group(1)) == sum(sales.values())
            elif claim.startswith("เดือน "):
                a, b = re.search(r"เดือน (\S+) ขายได้มากกว่าเดือน (\S+)", claim).groups()
                ok = sales[a] > sales[b]
            else:
                ok = list(sales.values()) == sorted(sales.values())
            if ok:
                true_claims.append(claim)
        assert true_claims == [_answer(q)]

        q = generate("comp.value_add_fluency", Random(seed))
        stem = _stem(q)
        counts = {k: int(n) for k, n in re.findall(r"(\S+) (\d+) ครั้ง", stem.split("ดังนี้ ")[1])}
        total = int(re.search(r"ข้อร้องเรียน (\d+) ครั้ง", stem).group(1))
        assert sum(counts.values()) == total
        if "ร้อยละ" in _answer(q):
            kind = re.search(r"ข้อร้องเรียนเรื่อง(\S+)คิดเป็น", stem).group(1)
            assert _answer(q) == f"ร้อยละ {counts[kind] * 100 // total}" and counts[kind] * 100 % total == 0
        else:
            assert _answer(q) == max(counts, key=counts.get)

        q = generate("comp.value_add_application", Random(seed))
        (sa, ba), (sb, bb) = [tuple(map(int, p)) for p in re.findall(r"ผู้เข้าชม (\d+) คน ซื้อสินค้า (\d+) คน", _stem(q))]
        ra, rb = ba * 100 / sa, bb * 100 / sb
        assert ra != rb
        better = "A" if ra > rb else "B"
        assert _answer(q) == f"หน้าเว็บแบบ {better} ดีกว่า เพราะมีอัตราการซื้อสูงกว่า {abs(ra - rb):g} จุดร้อยละ"
