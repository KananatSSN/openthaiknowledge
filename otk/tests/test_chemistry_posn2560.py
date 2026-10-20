"""Audit the complete supported parameter pools and re-read generated stems."""

from random import Random
import re

import pytest

from otk.core import generate
from otk.sheets.posn2560_chemistry import q03, q04, q06


def test_all_spectral_level_variants_have_distinct_energy_differences():
    for upper in range(2, 9):
        assert q03.solve(upper=upper) == q03.check(upper=upper)


def test_isotope_constraints_across_the_generator_pool():
    for electrons in (10, 18):
        for charge in (-2, -1, 0, 1, 2, 3):
            for extra in range(4, 11):
                for fewer in range(2, 6):
                    params = dict(electrons=electrons, charge=charge,
                                  neutrons=electrons + extra, fewer=fewer)
                    assert q04.solve(**params) == q04.check(**params)


def test_oxide_electroneutrality_and_orbital_removal():
    for atomic in range(25, 29):
        for metal_count, oxygen_count in ((1, 1), (2, 3), (1, 2)):
            params = dict(atomic=atomic, metal_count=metal_count, oxygen_count=oxygen_count)
            assert q06.solve(**params) == q06.check(**params)


@pytest.mark.parametrize("number", (3, 4, 6))
def test_generated_answers_follow_the_written_data(number):
    for seed in range(60):
        question = generate(f"chem.posn2560_q{number:02d}", rng=Random(seed))
        stem = " ".join(b.text for b in question.stem if b.kind == "text")
        answer = question.choices[question.answer].content[0].tex
        if number == 3:
            upper = int(re.search(r"n = (\d+)", stem)[1])
            expected = str(q03.check(upper=upper))
        elif number == 4:
            fewer, charge, electrons, neutrons = map(int, re.search(
                r"น้อยกว่า Y (\d+).*?ประจุ \+(\d+).*?อิเล็กตรอน (\d+).*?นิวตรอน (\d+)", stem,
            ).groups())
            atomic, mass = q04.check(electrons=electrons, charge=charge,
                                     neutrons=neutrons, fewer=fewer)
            expected = rf"{{}}^{{{mass}}}_{{{atomic}}}\mathrm{{X}}"
        else:
            atomic = int(re.search(r"เลขอะตอม (\d+)", stem)[1])
            counts = (2, 3) if "₂O₃" in stem else (1, 1)
            expected = str(q06.check(atomic=atomic, metal_count=counts[0], oxygen_count=counts[1]))
        assert answer == expected
        assert len(question.choices) == 4
