"""Audit the complete supported parameter pools and re-read generated stems."""

from random import Random
import re

import pytest

from otk.core import generate
from otk.sheets.posn2560_chemistry import q01, q02, q03, q04, q05, q06


def test_canal_ray_mass_from_independent_acceleration_route():
    for nucleons in (1, 2, 4, 20):
        assert q01.solve(nucleons=nucleons) == q01.check(nucleons=nucleons)


def test_group_17_model_claims_and_hunds_rule():
    for params in (q02.PARAMS, *q02.VARIANTS):
        assert q02.solve(**params) == q02.check(**params) == "only_minus_one"


def test_ionic_shells_from_orbital_filling():
    for params in (q05.PARAMS, *q05.VARIANTS):
        assert q05.solve(**params) == q05.check(**params)


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


@pytest.mark.parametrize("number", (1, 2, 3, 4, 5, 6))
def test_generated_answers_follow_the_written_data(number):
    for seed in range(60):
        question = generate(f"chem.posn2560_q{number:02d}", rng=Random(seed))
        stem = " ".join(b.text for b in question.stem if b.kind == "text")
        answer = question.choices[question.answer].content[0].tex
        if number == 1:
            isotope = re.search(r"ไอออนของ (H-1|H-2|He-4|Ne-20)", stem)[1]
            nucleons = int(isotope.split("-")[1])
            expected = str(q01.check(nucleons=nucleons))
        elif number == 2:
            states = tuple(int(s) for s in re.search(r"S = \{([^}]+)\}", stem)[1].split(", "))
            assert q02.check(states=states) == "only_minus_one"
            expected = r"S=\{-1\}"
        elif number == 3:
            upper = int(re.search(r"n = (\d+)", stem)[1])
            expected = str(q03.check(upper=upper))
        elif number == 4:
            fewer, charge, electrons, neutrons = map(int, re.search(
                r"น้อยกว่า Y (\d+).*?ประจุ \+(\d+).*?อิเล็กตรอน (\d+).*?นิวตรอน (\d+)", stem,
            ).groups())
            atomic, mass = q04.check(electrons=electrons, charge=charge,
                                     neutrons=neutrons, fewer=fewer)
            expected = rf"{{}}^{{{mass}}}_{{{atomic}}}\mathrm{{X}}"
        elif number == 5:
            matches = re.search(r"A = (\w+) \((\d+)\) ที่มีประจุ ([+-]\d+) และ B = (\w+) \((\d+)\) ที่มีประจุ ([+-]\d+)", stem)
            first_atomic, first_charge = int(matches[2]), int(matches[3])
            second_atomic, second_charge = int(matches[5]), int(matches[6])
            smaller = "A" if q05.check(first_atomic=first_atomic, first_charge=first_charge,
                                         second_atomic=second_atomic, second_charge=second_charge) == "first" else "B"
            larger = "B" if smaller == "A" else "A"
            expected = rf"r_{{{smaller}}}<r_{{{larger}}}"
        else:
            atomic = int(re.search(r"เลขอะตอม (\d+)", stem)[1])
            counts = (2, 3) if "₂O₃" in stem else (1, 1)
            expected = str(q06.check(atomic=atomic, metal_count=counts[0], oxygen_count=counts[1]))
        assert answer == expected
        assert len(question.choices) == 4
