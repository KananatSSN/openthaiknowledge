"""Cross-check the 2561 chemistry pools and generated wording."""

import re
from random import Random

import pytest

from otk.core import generate
from otk.sheets.posn2561_chemistry import q01, q02, q03


def test_first_wave_solves_source_and_variants_independently():
    for module in (q01, q02, q03):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


@pytest.mark.parametrize("number", (1, 2, 3))
def test_generated_answers_follow_the_stem(number):
    for seed in range(60):
        question = generate(f"chem.posn2561_q{number:02d}", rng=Random(seed))
        stem = " ".join(block.text for block in question.stem if block.kind == "text")
        answer = question.choices[question.answer].content[0].text
        if number == 1:
            a, d, e, g = map(int, re.search(
                r"มีเลขอะตอม (\d+), (\d+), (\d+) และ (\d+)", stem,
            ).groups())
            groups = {
                "A⁺, A⁻, D⁺": ((a, 1), (a, -1), (d, 1)),
                "E⁻, E⁺, G": ((e, -1), (e, 1), (g, 0)),
                "E⁻, A⁻, D⁺": ((e, -1), (a, -1), (d, 1)),
                "E⁻, G, A⁺": ((e, -1), (g, 0), (a, 1)),
            }
            assert set(choice.content[0].text for choice in question.choices) == set(groups)
            assert len({z - charge for z, charge in groups[answer]}) == 1
            assert sum(len({z - charge for z, charge in group}) == 1
                       for group in groups.values()) == 1
        elif number == 2:
            charge, electrons, neutrons = map(int, re.search(
                r"ไอออน X ประจุ \+(\d+) มี (\d+) อิเล็กตรอน .*?มี (\d+) นิวตรอน", stem,
            ).groups())
            atomic = electrons + charge
            assert answer == f"{atomic} และ {atomic + neutrons}"
        else:
            a, b, c, d = map(int, re.search(
                r"A=(\d+) nm, B=(\d+) nm, C=(\d+) nm และ D=(\d+) nm", stem,
            ).groups())
            assert a > b > c > d
            assert answer == "พลังงานของ C มากกว่า B"
        assert len(question.choices) == 4
