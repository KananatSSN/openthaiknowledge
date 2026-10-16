"""Process-skill units beyond ม.1: each answer re-derived from what the stem shows."""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

from otk.core import generate
from otk.sets.general_science.p4.process_skill import (
    ACTIONS,
    ANIMALS,
    CRITERIA,
    OBSERVATION_PAIRS,
    SKILL_NAMES,
)
from otk.sets.general_science.p5.process_skill import QUANTITIES, TIMES
from otk.sets.general_science.p6.process_skill import TESTS, TRIALS
from otk.sets.general_science.m2.process_skill import DEFINITIONS, RELATIONS, SETUPS
from otk.sets.general_science.m3.process_skill import CASES, MODELS, VERDICTS

SEEDS = 300


def _stem(question) -> str:
    return " ".join(block.text for block in question.stem)


def _answer(question) -> str:
    return " ".join(block.text for block in question.choices[question.answer].content)


def test_every_p4_action_names_one_listed_skill_and_each_skill_has_two():
    assert all(skill in SKILL_NAMES for _, skill in ACTIONS)
    for name in SKILL_NAMES:
        assert sum(skill == name for _, skill in ACTIONS) == 2, name
    assert len({action for action, _ in ACTIONS}) == len(ACTIONS)


def test_observations_and_inferences_never_share_a_sentence():
    observed = {o for o, _ in OBSERVATION_PAIRS}
    inferred = {i for _, i in OBSERVATION_PAIRS}
    assert not observed & inferred
    assert len(observed) == len(inferred) == len(OBSERVATION_PAIRS)


def test_the_sorting_criterion_is_the_only_one_that_makes_the_two_groups():
    by_name = {animal.name: animal for animal in ANIMALS}
    for seed in range(SEEDS):
        question = generate("sci.process_skill_p4_application", Random(seed))
        stem = _stem(question)
        first = re.search(r"กลุ่มที่ 1: (.*?) กลุ่มที่ 2:", stem).group(1).split()
        second = re.search(r"กลุ่มที่ 2: (.*?) นักเรียนใช้", stem).group(1).split()
        fits = [label for label, field in CRITERIA
                if len({getattr(by_name[n], field) for n in first}) == 1
                and len({getattr(by_name[n], field) for n in second}) == 1
                and getattr(by_name[first[0]], field) != getattr(by_name[second[0]], field)]
        assert fits == [_answer(question)], (seed, stem, fits)


def test_the_measuring_answer_pairs_the_right_tool_with_its_unit():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_p5_foundation", Random(seed))
        quantity = next(q for q in QUANTITIES if any(t in _stem(question) for t in q.things))
        assert _answer(question) == f"ใช้{quantity.tool} และบอกหน่วยเป็น{quantity.unit}"


def test_the_temperature_table_is_read_back_from_the_stem():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_p5_fluency", Random(seed))
        stem = _stem(question)
        values = dict(zip(TIMES, map(int, re.findall(r"น\. (\d+) องศาเซลเซียส", stem))))
        assert len(values) == len(TIMES)
        if "สูงที่สุด" in stem:
            assert _answer(question) == max(values, key=values.get)
        elif "ต่ำที่สุด" in stem:
            assert _answer(question) == min(values, key=values.get)
        else:
            a, b = re.search(r"เวลา (\S+ น\.) กับเวลา (\S+ น\.)", stem).groups()
            assert _answer(question) == f"{abs(values[a] - values[b])} องศาเซลเซียส"


def test_the_prediction_continues_the_recorded_step():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_p5_application", Random(seed))
        stem = _stem(question)
        values = [int(v) for v in re.findall(r"\d+: (\d+) ", stem)]
        step = values[1] - values[0]
        assert all(b - a == step for a, b in zip(values, values[1:]))
        target = int(re.search(r"ที่ (\d+) จะมีค่าเท่าใด", stem).group(1))
        assert _answer(question).split()[0] == str(values[0] + step * (target - 1))


def test_every_p6_test_keeps_its_variables_apart():
    for test in TESTS:
        assert len({test.changed, test.measured, test.kept}) == 3
        assert test.hypothesis.startswith("ถ้า")
        assert test.hypothesis not in test.untestable


def test_the_conclusion_follows_the_trial_and_level_data_shows_no_trend():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_p6_application", Random(seed))
        stem = _stem(question)
        trial = next(t for t in TRIALS if t.setup in stem)
        values = [int(v) for v in re.findall(r": (\d+) ", stem)]
        answer = _answer(question)
        if trial.trend == "up":
            assert values == sorted(values) and answer.endswith("มากขึ้น")
        elif trial.trend == "down":
            assert values == sorted(values, reverse=True) and answer.endswith("น้อยลง")
        else:
            assert max(values) - min(values) <= 2
            assert values not in (sorted(values), sorted(values, reverse=True))
            assert "ไม่มีผล" in answer
        assert answer.startswith(f"เมื่อ{trial.changed}") or answer.startswith(trial.changed)


def test_each_definition_offers_three_ways_of_not_being_operational():
    for item in DEFINITIONS:
        assert item.operational not in item.wrongs and len(set(item.wrongs)) == 3


def test_the_stray_variable_is_the_one_control_that_differs_between_the_sets():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_m2_fluency", Random(seed))
        stem = _stem(question)
        setup = next(s for s in SETUPS if s.aim in stem)
        second = stem.split("ชุดที่ 2:")[1]
        strays = [c.name for c in setup.controls if c.stray in second]
        assert strays == [_answer(question)], (seed, strays)


def test_the_estimate_lies_on_the_recorded_line():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_m2_application", Random(seed))
        stem = _stem(question)
        rel = next(r for r in RELATIONS if r.setup in stem)
        pairs = [(int(x), int(y)) for x, y in re.findall(
            rf"(\d+) {rel.x_unit}: (\d+) {rel.y_unit}", stem)]
        (x0, y0), (x1, y1) = pairs[0], pairs[1]
        slope = Fraction(y1 - y0, x1 - x0)
        assert all(y == y0 + slope * (x - x0) for x, y in pairs)
        x = int(re.search(rf"เมื่อ{rel.x_name} (\d+) {rel.x_unit}", stem).group(1))
        assert _answer(question) == f"{y0 + slope * (x - x0)} {rel.y_unit}"


def test_the_odd_trial_and_the_average_of_the_rest_are_read_back():
    for seed in range(SEEDS):
        question = generate("sci.process_skill_m3_fluency", Random(seed))
        stem = _stem(question)
        values = [int(v) for v in re.findall(r"ครั้งที่ \d: (\d+)", stem)]
        median = sorted(values)[1:3]
        odd = max(range(4), key=lambda i: abs(values[i] - sum(median) / 2))
        if "ผิดปกติและควรตรวจสอบ" in stem:
            assert _answer(question) == f"ครั้งที่ {odd + 1}"
        else:
            rest = [v for i, v in enumerate(values) if i != odd]
            assert _answer(question).split()[0] == str(sum(rest) // 3)
            assert sum(rest) % 3 == 0


def test_every_model_and_case_answers_one_way():
    assert len({m.stands_for for m in MODELS}) == len(MODELS)
    for model in MODELS:
        assert model.limit not in model.not_limits
    assert {verdict for _, verdict in CASES} == set(VERDICTS)
    assert len({case for case, _ in CASES}) == len(CASES)
