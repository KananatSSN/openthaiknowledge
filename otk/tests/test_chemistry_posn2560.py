"""Audit the complete supported parameter pools and re-read generated stems."""

from random import Random
import re

import pytest

from otk.core import generate
from otk.sheets.posn2560_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24,
)


def test_canal_ray_mass_from_independent_acceleration_route():
    for nucleons in (1, 2, 4, 20):
        assert q01.solve(nucleons=nucleons) == q01.check(nucleons=nucleons)


def test_group_17_model_claims_and_hunds_rule():
    for params in (q02.PARAMS, *q02.VARIANTS):
        assert q02.solve(**params) == q02.check(**params) == "only_minus_one"


def test_ionic_shells_from_orbital_filling():
    for params in (q05.PARAMS, *q05.VARIANTS):
        assert q05.solve(**params) == q05.check(**params)


def test_unpaired_counts_for_source_and_variant_pairs():
    for params in (q07.PARAMS, *q07.VARIANTS):
        assert q07.solve(**params) == q07.check(**params)
    assert q07.solve(**q07.PARAMS)
    assert not q07.solve(first_symbol="Cu", first_charge=2,
                         second_symbol="Cr", second_charge=3)


def test_group_two_dications_reach_closed_shells():
    for params in (q08.PARAMS, *q08.VARIANTS):
        assert q08.solve(**params) == q08.check(**params)


def test_three_oxidation_balances():
    for params in (q09.PARAMS, *q09.VARIANTS):
        assert q09.solve(**params) == q09.check(**params)


def test_hund_violation_from_orbital_box_enumeration():
    for params in (q10.PARAMS, *q10.VARIANTS):
        assert q10.solve(**params) == q10.check(**params)


def test_source_radius_ionization_choices_have_no_correct_answer():
    for params in (q11.PARAMS, *q11.VARIANTS):
        assert q11.solve(**params) == q11.check(**params)
    radius, ionization = q11.check(**q11.PARAMS)
    printed = (
        (("G", "E", "D"), ("A", "D", "E")),
        (("D", "G", "A"), ("E", "G", "A")),
        (("A", "E", "G"), ("D", "G", "A")),
        (("E", "G", "A"), ("G", "A", "E")),
    )

    def descending(subsequence, order):
        return list(subsequence) == sorted(subsequence, key=order.index)

    assert not any(descending(r, radius) and descending(ie, ionization)
                   for r, ie in printed)
    assert (radius, ionization) == (("E", "G", "D", "A"), ("A", "D", "G", "E"))


def test_isoelectronic_ion_positions_against_element_lookup():
    for params in (q12.PARAMS, *q12.VARIANTS):
        assert q12.solve(**params) == q12.check(**params)


def test_acidic_oxide_products_precipitation_and_halogen_order():
    for module in (q13, q14, q15):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_nuclear_balance_valence_counts_and_halide_boiling_order():
    for module in (q16, q17, q18):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_net_ionic_conductivity_and_nitrogen_oxygen_bonds():
    for module in (q19, q20, q21):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_vsepr_shapes_angles_and_central_lone_pairs():
    for module in (q22, q23, q24):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


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


@pytest.mark.parametrize("number", tuple(range(1, 25)))
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
        elif number == 6:
            atomic = int(re.search(r"เลขอะตอม (\d+)", stem)[1])
            counts = (2, 3) if "₂O₃" in stem else (1, 1)
            expected = str(q06.check(atomic=atomic, metal_count=counts[0], oxygen_count=counts[1]))
        elif number == 7:
            def pair_is_equal(tex):
                found = re.findall(r"\\mathrm\{([A-Z][a-z]?)\}(\^\{\d*\+\})?", tex)
                assert len(found) == 2
                atoms = [(symbol, int(re.search(r"\d+", suffix)[0]) if re.search(r"\d+", suffix)
                          else 1 if suffix else 0) for symbol, suffix in found]
                return q07.check(first_symbol=atoms[0][0], first_charge=atoms[0][1],
                                 second_symbol=atoms[1][0], second_charge=atoms[1][1])

            assert sum(pair_is_equal(choice.content[0].tex) for choice in question.choices) == 1
            assert pair_is_equal(answer)
            expected = answer
        elif number == 8:
            atomic = int(re.search(r"เลขอะตอม (\d+)", stem)[1])
            expected = rf"\mathrm{{{q08.check(atomic=atomic)}}}"
        elif number == 9:
            first = next(params for formula, params in (
                ("[Co(NH₃)₄SO₄]Cl", (4, -2)), ("NaNO₃", (3, -1)),
                ("Na₃PO₄", (4, -3)),
            ) if formula in stem)
            acid = next(oxygen for formula, oxygen in (
                ("HClO₄", 4), ("HClO₃", 3), ("HBrO₃", 3),
            ) if formula in stem)
            complex_ = next(params for formula, params in (
                ("Na[Au(CN)₂]", (2, -1)), ("K₃[Co(CN)₆]", (6, -3)),
                ("K₂[Pt(CN)₄]", (4, -2)),
            ) if formula in stem)
            states = q09.check(oxo_oxygen=first[0], oxo_charge=first[1],
                               acid_oxygen=acid, cyanide_count=complex_[0],
                               complex_charge=complex_[1])
            expected = "(" + ",".join(f"+{state}" if state > 0 else str(state)
                                     for state in states) + ")"
        elif number == 10:
            def counts(tex):
                boxes = re.findall(r"\\boxed\{([^}]*)\}", tex)
                assert len(boxes) == 5
                return (sum(boxes[1].count(arrow) for arrow in (r"\uparrow", r"\downarrow")),
                        tuple(sum(box.count(arrow) for arrow in (r"\uparrow", r"\downarrow"))
                              for box in boxes[2:]))

            patterns = tuple(counts(choice.content[0].tex) for choice in question.choices)
            assert question.answer == q10.check(patterns=patterns)
            expected = question.choices[q10.check(patterns=patterns)].content[0].tex
        elif number == 11:
            assignments = dict(re.findall(r"([ADEG])=(O|P|Ga|As)", stem))
            elements = tuple(assignments[label] for label in "ADEG")
            radius, ionization = q11.check(elements=elements)
            expected = r"r:" + ">".join(radius) + r",\quad I_1:" + ">".join(ionization)
        elif number == 12:
            gas = re.search(r"แก๊สมีตระกูล (Ne|Ar|Kr|Xe)", stem)[1]
            electrons = {"Ne": 10, "Ar": 18, "Kr": 36, "Xe": 54}[gas]
            expected = "(" + ",".join(map(str, q12.check(noble_electrons=electrons))) + ")"
        elif number == 13:
            oxides = tuple(re.search(r"แดง: ([A-Za-z0-9, ]+)", stem)[1].split(", "))
            expected = r"\mathrm{" + r"},\;\mathrm{".join(q13.check(oxides=oxides)) + "}"
        elif number == 14:
            cations = tuple(re.findall(r"(Ba|Mg|Na|K)(?:²|)⁺", stem))
            anions = tuple(re.findall(r"(Cl|NO3|SO4|HPO4)(?:²|)⁻", stem))
            assert len(cations) == len(anions) == 3
            expected = r",\;".join(r"\mathrm{" + formula + "}" for formula in
                                    q14.check(cations=cations, anions=anions))
        elif number == 15:
            bromine = re.search(r"สารละลาย ([XYZ])₂ ใน CCl₄ มีสีส้ม", stem)[1]
            iodine = re.search(r"สารละลาย K([XYZ]) ชั้น", stem)[1]
            chlorine = (set("XYZ") - {bromine, iodine}).pop()
            assignment = tuple({bromine: "Br", iodine: "I", chlorine: "Cl"}[label]
                               for label in "XYZ")
            expected = ">".join(q15.check(assignment=assignment))
        elif number == 16:
            co, mn, te, iodine, rn = map(int, re.search(
                r"Co-(\d+).*?Mn-(\d+).*?Te-(\d+).*?I-(\d+).*?Rn-(\d+)", stem,
            ).groups())
            first, second, (mass, atomic) = q16.check(
                co_mass=co, mn_mass=mn, te_mass=te, iodine_mass=iodine, rn_mass=rn,
            )
            expected = (rf"(\mathrm{{{first}}},\;\mathrm{{{second}}},\;"
                        rf"{{}}^{{{mass}}}_{{{atomic}}}\mathrm{{Ra}})")
        elif number == 17:
            halogen = re.search(r"แฮโลเจน (F|Cl|Br|I) มีจำนวน", stem)[1]
            hydrogen_count, halogen_count = q17.check(halogen=halogen)
            expected = (rf"n_v(\mathrm{{H}})={hydrogen_count},\;"
                        rf"n_v(\mathrm{{{halogen}}})={halogen_count}")
        elif number == 18:
            molecules = tuple(re.search(r"จุดเดือดปกติของ ([A-Za-z, ]+) จากต่ำไปสูง", stem)[1].split(", "))
            expected = "<".join(rf"\mathrm{{{molecule}}}" for molecule in
                                q18.check(molecules=molecules))
        elif number == 19:
            reaction = next(pair for reagent, pair in (
                ("Pb(NO₃)₂", ("Pb", "SO4")), ("BaCl₂", ("Ba", "SO4")),
                ("AgNO₃", ("Ag", "Cl")), ("CaCl₂", ("Ca", "CO3")),
            ) if reagent in stem)
            positive, negative, product = q19.check(metal=reaction[0], anion=reaction[1])
            ion_tex = {"Pb": r"\mathrm{Pb}", "Ba": r"\mathrm{Ba}",
                       "Ag": r"\mathrm{Ag}", "Ca": r"\mathrm{Ca}",
                       "SO4": r"\mathrm{SO_4}", "Cl": r"\mathrm{Cl}",
                       "CO3": r"\mathrm{CO_3}"}
            product_tex = {"PbSO4": r"\mathrm{PbSO_4}", "BaSO4": r"\mathrm{BaSO_4}",
                           "AgCl": r"\mathrm{AgCl}", "CaCO3": r"\mathrm{CaCO_3}"}
            plus = f"{positive if positive > 1 else ''}+"
            minus = f"{negative if negative > 1 else ''}-"
            expected = (f"{ion_tex[reaction[0]]}^{{{plus}}}_{{(aq)}}+"
                        f"{ion_tex[reaction[1]]}^{{{minus}}}_{{(aq)}}"
                        rf"\rightarrow {product_tex[product]}_{{(s)}}")
        elif number == 20:
            rows = re.findall(
                r"([A-E])=\((-?\d+),(-?\d+);(ไม่นำ|นำ)/(ไม่นำ|นำ)/(ไม่ละลาย|ไม่นำ|นำ)\)",
                stem,
            )
            assert len(rows) == 5
            metal = next(label for label, _, _, solid, liquid, _ in rows
                         if solid == liquid == "นำ")
            ionic = next(label for label, _, _, solid, liquid, water in rows
                         if solid == "ไม่นำ" and liquid == water == "นำ")
            molecular = next(label for label, _, _, solid, liquid, water in rows
                             if solid == liquid == "ไม่นำ" and water == "นำ")
            expected = f"({ionic},{molecular},{metal})"
        elif number == 21:
            listed = re.search(r"ในบรรดาชนิดต่อไปนี้ (.+?) ชนิดใด", stem)[1].split(", ")
            by_text = {"NO⁺": "NO+", "NO": "NO", "NO₂⁺": "NO2+",
                       "NO₂⁻": "NO2-", "NO₃⁻": "NO3-"}
            species = tuple(by_text[value] for value in listed)
            shortest = q21.check(species=species)
            expected = {"NO+": r"\mathrm{NO}^{+}", "NO": r"\mathrm{NO}",
                        "NO2+": r"\mathrm{NO_2}^{+}", "NO2-": r"\mathrm{NO_2}^{-}",
                        "NO3-": r"\mathrm{NO_3}^{-}"}[shortest]
        elif number == 22:
            tex = {"BF4-": r"\mathrm{BF_4}^{-}", "POCl3": r"\mathrm{POCl_3}",
                   "ICl4-": r"\mathrm{ICl_4}^{-}", "XeF4": r"\mathrm{XeF_4}",
                   "TeCl4": r"\mathrm{TeCl_4}", "SF4": r"\mathrm{SF_4}",
                   "NH3": r"\mathrm{NH_3}", "PCl3": r"\mathrm{PCl_3}"}
            reverse = {value: key for key, value in tex.items()}
            pairs = tuple(tuple(reverse[part] for part in
                                choice.content[0].tex.split(r",\;"))
                          for choice in question.choices)
            matching = q22.check(pairs=pairs)
            expected = tex[matching[0]] + r",\;" + tex[matching[1]]
        elif number == 23:
            listed = re.search(r"แต่ละโมเลกุล: (.+?) โมเลกุลใด", stem)[1].split(", ")
            text_to_formula = {"ClF₃": "ClF3", "ClF₅": "ClF5", "SiF₄": "SiF4",
                               "NCl₃": "NCl3", "OCl₂": "OCl2", "BF₃": "BF3",
                               "NH₃": "NH3", "H₂O": "H2O"}
            molecules = tuple(text_to_formula[value] for value in listed)
            shortest = q23.check(molecules=molecules)
            expected = {"ClF3": r"\mathrm{ClF_3}", "ClF5": r"\mathrm{ClF_5}",
                        "SiF4": r"\mathrm{SiF_4}", "NCl3": r"\mathrm{NCl_3}",
                        "OCl2": r"\mathrm{OCl_2}", "BF3": r"\mathrm{BF_3}",
                        "NH3": r"\mathrm{NH_3}", "H2O": r"\mathrm{H_2O}"}[shortest]
        else:
            listed = re.search(r"ในบรรดา (.+?) ชนิดใด", stem)[1].split(", ")
            text_to_formula = {"NH₃": "NH3", "XeF₂": "XeF2", "NO₂⁻": "NO2-",
                               "SO₃²⁻": "SO3^2-", "I₃⁻": "I3-", "XeF₄": "XeF4",
                               "ClF₃": "ClF3", "SF₄": "SF4"}
            species = tuple(text_to_formula[value] for value in listed)
            most = q24.check(species=species)
            expected = {"NH3": r"\mathrm{NH_3}", "XeF2": r"\mathrm{XeF_2}",
                        "NO2-": r"\mathrm{NO_2}^{-}", "SO3^2-": r"\mathrm{SO_3}^{2-}",
                        "I3-": r"\mathrm{I_3}^{-}", "XeF4": r"\mathrm{XeF_4}",
                        "ClF3": r"\mathrm{ClF_3}", "SF4": r"\mathrm{SF_4}"}[most]
        assert answer == expected
        assert len(question.choices) == 4
