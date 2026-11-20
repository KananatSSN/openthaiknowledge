"""Audit the complete supported parameter pools and re-read generated stems."""

from random import Random
import re

import pytest

from otk.core import generate
from otk.sheets.posn2560_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24,
    q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36,
    q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48,
    q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60,
    q61, q62, q63, q64, q65, q66, q67, q68, q69, q70,
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


def test_polarity_mixed_bonds_and_dative_lewis_depiction():
    for module in (q25, q26, q27):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_noble_gas_shapes_names_and_alkene_bond_cleavage():
    for module in (q28, q29, q30):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)
    assert q29.ANSWER == 0  # all four printed names are correct


def test_interhalogen_octets_polar_pairs_and_liquid_trends():
    for module in (q31, q32, q33):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_phase_lattice_and_charles_law_variants():
    for module in (q34, q35, q36):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_helium_ideality_stp_and_ideal_gas_claim_variants():
    for module in (q37, q38, q39):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_stp_density_graham_law_and_alloy_variants():
    for module in (q40, q41, q42):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_blast_furnace_lioh_and_carbonate_variants():
    for module in (q43, q44, q45):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)
    assert q43.ANSWER == (0, 3)  # two source choices are true


def test_methanol_hydrate_and_mass_rank_variants():
    for module in (q46, q47, q48):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_combustion_precipitation_and_zinc_acid_variants():
    for module in (q49, q50, q51):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)
    assert q50.ANSWER == (0, 1)  # after making BaCl2 addition exact


def test_product_mass_ammonia_fraction_and_hydrate_dilution_variants():
    for module in (q52, q53, q54):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_molality_hypochlorite_dilution_and_nitrate_masses_variants():
    for module in (q55, q56, q57):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_chloride_dilution_mixed_solution_and_boiling_variants():
    for module in (q58, q59, q60):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_written_ion_configs_oxidation_extremes_and_decay_variants():
    for module in (q61, q62, q63):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_written_metallicity_lattice_and_bond_energy_variants():
    for module in (q64, q65, q66):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


def test_written_yields_combustion_perchlorate_and_freezing_variants():
    for module in (q67, q68, q69, q70):
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


@pytest.mark.parametrize("number", tuple(range(1, 71)))
def test_generated_answers_follow_the_written_data(number):
    for seed in range(60):
        question = generate(f"chem.posn2560_q{number:02d}", rng=Random(seed))
        stem = " ".join(b.text for b in question.stem if b.kind == "text")
        answer_block = question.choices[question.answer].content[0]
        answer = getattr(answer_block, "tex", getattr(answer_block, "text", None))
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
        elif number == 24:
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
        elif number in (25, 26, 27):
            listed = re.search(r"(?:ในบรรดา|พิจารณาสารบริสุทธิ์) (.+?) (?:โมเลกุลใด|สารใด)", stem)[1]
            formulas = tuple(listed.split(", "))
            module = {25: q25, 26: q26, 27: q27}[number]
            parameter = "compounds" if number == 26 else "species"
            result = module.check(**{parameter: formulas})
            expected = {
                "SF4": r"\mathrm{SF_4}", "SCl2": r"\mathrm{SCl_2}",
                "PCl3": r"\mathrm{PCl_3}", "PF5": r"\mathrm{PF_5}",
                "H2O": r"\mathrm{H_2O}", "NH3": r"\mathrm{NH_3}",
                "CO2": r"\mathrm{CO_2}", "BF3": r"\mathrm{BF_3}",
                "XeF4": r"\mathrm{XeF_4}", "ClF3": r"\mathrm{ClF_3}",
                "Na2O": r"\mathrm{Na_2O}", "COCl2": r"\mathrm{COCl_2}",
                "H2SO4": r"\mathrm{H_2SO_4}", "CaCO3": r"\mathrm{CaCO_3}",
                "NaNO3": r"\mathrm{NaNO_3}", "NH4Cl": r"\mathrm{NH_4Cl}",
                "K2SO4": r"\mathrm{K_2SO_4}", "NaCl": r"\mathrm{NaCl}",
                "O3": r"\mathrm{O_3}", "H2O2": r"\mathrm{H_2O_2}",
                "H2CO": r"\mathrm{H_2CO}", "CH2NH": r"\mathrm{CH_2NH}",
                "CH4": r"\mathrm{CH_4}", "HCl": r"\mathrm{HCl}",
            }[result]
        elif number == 28:
            formula = re.search(r"ของ (KrO2H2|XeO2F2|XeOF4|XeO3|XeF4) เป็น", stem)[1]
            expected = {
                "seesaw": "ทรงสี่หน้าบิดเบี้ยว", "square_pyramidal": "พีระมิดฐานสี่เหลี่ยม",
                "trigonal_pyramidal": "พีระมิดฐานสามเหลี่ยม",
                "square_planar": "สี่เหลี่ยมแบนราบ",
            }[q28.check(formula=formula)]
        elif number == 29:
            names_thai = re.findall(r"(?:CrO3|Na2S2O3|Hg2Cl2|Ba\(NO2\)2) = ([^;]+?)(?:;| มี)", stem)
            assert len(names_thai) == 4
            thai_to_code = {
                "โครเมียมไตรออกไซด์": "chromium_trioxide",
                "โครเมียมไดออกไซด์": "chromium_dioxide",
                "โซเดียมไทโอซัลเฟต": "sodium_thiosulfate",
                "โซเดียมซัลไฟต์": "sodium_sulfite",
                "เมอร์คิวรี(I)คลอไรด์": "mercury_i_chloride",
                "เมอร์คิวรี(II)คลอไรด์": "mercury_ii_chloride",
                "แบเรียมไนไตรต์": "barium_nitrite",
                "แบเรียมไนเตรต": "barium_nitrate",
            }
            expected = str(q29.check(names=tuple(thai_to_code[name] for name in names_thai)))
        elif number == 30:
            alkene = re.search(r"จาก ([A-Z0-9=]+)\(g\)", stem)[1]
            left, right = q30.check(alkene=alkene)

            def fragment_tex(formula):
                return r"\mathrm{" + re.sub(r"([A-Z][a-z]?)(\d+)", r"\1_\2", formula) + "}"

            reactant = "=".join(fragment_tex(part) for part in alkene.split("="))
            expected = (reactant + r"_{(g)}\rightarrow "
                        + fragment_tex(left) + r"_{(g)}+"
                        + fragment_tex(right) + r"_{(g)}")
        elif number == 31:
            def parse_interhalogen(tex):
                match = re.fullmatch(
                    r"\\mathrm\{(I|Br|Cl)F\}(?:_\{(\d+)\})?(?:\^\{(\d*)\+\})?", tex,
                )
                assert match
                return (match[1], int(match[2] or 1),
                        0 if match[3] is None else int(match[3] or 1))

            species = tuple(parse_interhalogen(choice.content[0].tex)
                            for choice in question.choices)
            nonoctet = q31.check(species=species)
            expected = next(choice.content[0].tex for choice in question.choices
                            if parse_interhalogen(choice.content[0].tex) == nonoctet)
        elif number == 32:
            formula_tex = {
                "HCN": r"\mathrm{HCN}", "KrF4": r"\mathrm{KrF_4}",
                "AsI5": r"\mathrm{AsI_5}", "SBr2": r"\mathrm{SBr_2}",
                "ClH3": r"\mathrm{ClH_3}", "TeF4": r"\mathrm{TeF_4}",
                "SO3": r"\mathrm{SO_3}", "PBr3": r"\mathrm{PBr_3}",
                "NH3": r"\mathrm{NH_3}", "H2O": r"\mathrm{H_2O}",
                "CO2": r"\mathrm{CO_2}", "XeF4": r"\mathrm{XeF_4}",
                "BF3": r"\mathrm{BF_3}", "PCl3": r"\mathrm{PCl_3}",
                "SF4": r"\mathrm{SF_4}",
            }
            reverse = {tex: formula for formula, tex in formula_tex.items()}
            pairs = tuple(tuple(reverse[part] for part in choice.content[0].tex.split(r",\;"))
                          for choice in question.choices)
            polar_pair = q32.check(pairs=pairs)
            expected = formula_tex[polar_pair[0]] + r",\;" + formula_tex[polar_pair[1]]
        elif number == 33:
            direction = "cool" if "เมื่อลดอุณหภูมิ" in stem else "warm"
            trend_text = {
                "ความดันไอลดลง": ("vapor_pressure", "decrease"),
                "ความดันไอเพิ่มขึ้น": ("vapor_pressure", "increase"),
                "ความตึงผิวลดลง": ("surface_tension", "decrease"),
                "ความตึงผิวเพิ่มขึ้น": ("surface_tension", "increase"),
                "พลังงานจลน์เฉลี่ยของโมเลกุลลดลง": ("kinetic_energy", "decrease"),
                "พลังงานจลน์เฉลี่ยของโมเลกุลเพิ่มขึ้น": ("kinetic_energy", "increase"),
                "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมลดลง":
                    ("fixed_distance_attraction", "decrease"),
                "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมเพิ่มขึ้น":
                    ("fixed_distance_attraction", "increase"),
                "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมไม่เปลี่ยน":
                    ("fixed_distance_attraction", "same"),
            }
            claims = tuple(trend_text[choice.content[0].text] for choice in question.choices)
            expected = question.choices[q33.check(direction=direction, claims=claims)].content[0].text
        elif number == 34:
            from otk.sets.chemistry.olympiad.posn2560 import _PHASE_CLAIMS
            reverse = {value: key for key, value in _PHASE_CLAIMS.items()}
            claims = tuple(reverse[choice.content[0].text] for choice in question.choices)
            expected = question.choices[q34.check(claims=claims)].content[0].text
        elif number == 35:
            from otk.sets.chemistry.olympiad.posn2560 import (
                _LATTICE_CLAIMS, _LATTICE_OPTION_TEXT,
            )
            claims = tuple(next(key for key, value in _LATTICE_CLAIMS.items()
                                if f"{label}. {value}" in stem)
                           for label in "abc")
            expected = _LATTICE_OPTION_TEXT[q35.check(claims=claims)]
        elif number == 36:
            volume, initial, final = map(int, re.search(
                r"ปริมาตร (\d+) cm³ ที่ (\d+) °C.*?เป็น (\d+) °C", stem,
            ).groups())
            expected = f"{q36.check(initial_volume=volume, initial_celsius=initial, final_celsius=final):.1f}"
        elif number == 37:
            conditions = []
            for choice in question.choices:
                temp, pressure, unit = re.fullmatch(
                    r"(\d+) K และ ([\d.]+) (mmHg|atm)", choice.content[0].text,
                ).groups()
                conditions.append((int(temp), round(float(pressure) *
                                                    (760 if unit == "atm" else 1))))
            expected = question.choices[q37.check(conditions=tuple(conditions))].content[0].text
        elif number == 38:
            volume, pressure, celsius = re.search(
                r"ปริมาตร ([\d.]+) L ที่ความดัน ([\d.]+) atm และอุณหภูมิ (\d+) °C",
                stem,
            ).groups()
            expected = f"{q38.check(volume_l=float(volume), pressure_atm=float(pressure), initial_celsius=int(celsius)):.2f}"
        elif number == 39:
            initial, final, factor = map(int, re.search(
                r"อุณหภูมิจาก (\d+) °C เป็น (\d+) °C ความดันเพิ่ม (\d+) เท่า", stem,
            ).groups())
            assert q39.check(factor=factor, initial_celsius=initial,
                             final_celsius=final) == 2
            expected = "ค"
        elif number == 40:
            density, amount = re.search(
                r"ความหนาแน่น ([\d.]+) g/L แก๊สจำนวน (\d+) mol", stem,
            ).groups()
            expected = f"{q40.check(density_g_l=float(density), amount_mol=int(amount)):.1f}"
        elif number == 41:
            first, seconds, second = map(int, re.search(
                r"มวลโมลาร์ (\d+) g/mol\) ปริมาณเท่ากันแพร่ผ่านรูพรุนใน (\d+) s .*?มวลโมลาร์ (\d+) g/mol",
                stem,
            ).groups())
            expected = f"{q41.check(first_molar=first, second_molar=second, first_seconds=seconds):.1f}"
        elif number == 42:
            alloy, product = map(float, re.search(
                r"มวล ([\d.]+) g ทำปฏิกิริยา.*?ได้ ZnCl₂ ([\d.]+) g", stem,
            ).groups())
            expected = f"{q42.check(alloy_g=alloy, zinc_chloride_g=product):.1f}"
        elif number == 43:
            iron = float(re.search(r"ผลิต Fe ([\d.]+) kg", stem)[1])
            values = tuple(map(float, re.search(
                r"a\. ต้องใช้ C ([\d.]+) kg; b\. ต้องใช้ Fe₂O₃ ([\d.]+) mol; "
                r"c\. ต้องใช้ O₂ ([\d.]+) mol; d\. เกิด CO₂ ([\d.]+) dm³", stem,
            ).groups()))
            kinds = ("carbon_kg", "hematite_mol", "oxygen_mol", "co2_l")
            pair = q43.check(iron_kg=iron, claims=tuple(zip(kinds, values)))
            expected = f"{'abcd'[pair[0]]} และ {'abcd'[pair[1]]}"
        elif number == 44:
            mass, pressure, temperature = re.search(
                r"LiOH (\d+) g.*?ความดัน ([\d.]+) atm และอุณหภูมิ (\d+) K", stem,
            ).groups()
            expected = str(q44.check(lioh_g=int(mass), pressure_atm=float(pressure),
                                     temperature_k=int(temperature)))
        elif number == 45:
            mass, acid, acid_ml, gas_ml = re.search(
                r"คาร์บอเนตมวล ([\d.]+) g.*?HCl ([\d.]+) mol/L "
                r"ปริมาตร (\d+) cm³ ได้ CO₂ (\d+) cm³", stem,
            ).groups()
            carbonate = q45.check(carbonate_g=float(mass), acid_molar=float(acid),
                                  acid_ml=int(acid_ml), co2_ml=int(gas_ml))
            expected = {
                "Na2CO3": r"\mathrm{Na_2CO_3}", "MgCO3": r"\mathrm{MgCO_3}",
                "CaCO3": r"\mathrm{CaCO_3}", "BaCO3": r"\mathrm{BaCO_3}",
            }[carbonate]
        elif number == 46:
            co_g, hydrogen_g = re.search(r"CO (\d+) g ทำปฏิกิริยากับ H₂ ([\d.]+) g", stem).groups()
            expected = f"{q46.check(co_g=int(co_g), hydrogen_g=float(hydrogen_g)):.1f}"
        elif number == 47:
            water, sample = re.search(r"มีน้ำ ([\d.]+)% โดยมวล สารตัวอย่าง ([\d.]+) g", stem).groups()
            expected = f"{q47.check(water_percent=float(water), sample_g=float(sample)):.2f}"
        elif number == 48:
            a, b, c, xmass = re.search(
                r"a: H₂ ([\d.]+)×10²³ โมเลกุล; b: NH₃ ([\d.]+) L ที่ STP; "
                r"c: สาร X ([\d.]+)×10²² โมเลกุล โดย X 0.25 mol มีมวล ([\d.]+) g",
                stem,
            ).groups()
            order = q48.check(a_molecules=float(a) * 1e23, b_l=float(b),
                              c_molecules=float(c) * 1e22, x_sample_g=float(xmass))
            expected = " > ".join(order)
        elif number == 49:
            hydro, oxygen, carbon_dioxide = map(int, re.search(
                r"CxHy (\d+) cm³.*?O₂ (\d+) cm³ ได้ CO₂ (\d+) cm³", stem,
            ).groups())
            expected = ", ".join(map(str, q49.check(
                hydrocarbon_ml=hydro, oxygen_ml=oxygen,
                carbon_dioxide_ml=carbon_dioxide)))
        elif number == 50:
            barium, sulfate, sulfate_ml = re.search(
                r"BaCl₂ ([\d.]+) mol/L กับ Na₂SO₄ ([\d.]+)%.*?ปริมาตร (\d+) cm³",
                stem,
            ).groups()
            claim_x, claim_solid, claim_sodium = re.search(
                r"a\. ใช้ BaCl₂ ([\d.]+) cm³; b\. ได้ BaSO₄ ([\d.]+) g; "
                r"c\. Na⁺ ในสารละลายสุดท้าย ([\d.]+)%", stem,
            ).groups()
            truth = q50.check(sulfate_percent=float(sulfate), sulfate_ml=int(sulfate_ml),
                              barium_molar=float(barium), claim_x_ml=float(claim_x),
                              claim_precipitate_g=float(claim_solid),
                              claim_sodium_percent=float(claim_sodium))
            expected = "กขคง"[((0,), (1,), (0, 1), (1, 2)).index(truth)]
        elif number == 51:
            zn, acid, acid_ml = re.search(
                r"Zn ([\d.]+) g เติมใน HCl ([\d.]+) mol/L ปริมาตร (\d+) cm³",
                stem,
            ).groups()
            hydrogen, chloride, used, left = re.search(
                r"a\. ได้ H₂ ([\d.]+) L.*?b\. ZnCl₂ มีความเข้มข้น ([\d.]+)%.*?"
                r"c\. HCl ใช้ไป ([\d.]+) mol และเหลือ ([\d.]+) mol", stem,
            ).groups()
            truth = q51.check(zn_g=float(zn), acid_molar=float(acid), acid_ml=int(acid_ml),
                              claim_hydrogen_l=float(hydrogen),
                              claim_zinc_chloride_percent=float(chloride),
                              claim_acid_used_mol=float(used), claim_acid_left_mol=float(left))
            expected = "กขคง"[((0, 1), (0, 2), (1, 2), (0, 1, 2)).index(truth)]
        elif number == 52:
            a_g, b_g, c_g, a_molar, b_molar = re.search(
                r"ใช้ A ([\d.]+) g และ B ([\d.]+) g ได้ C ([\d.]+) g "
                r"โดย A มีมวลโมลาร์ (\d+) g/mol และ B (\d+) g/mol", stem,
            ).groups()
            expected = f"{q52.check(a_g=float(a_g), b_g=float(b_g), c_g=float(c_g), a_molar=int(a_molar), b_molar=int(b_molar)):.1f}"
        elif number == 53:
            ammonia = float(re.search(r"มี NH₃ ([\d.]+)% โดยโมล", stem)[1]) / 100
            expected = f"{q53.check(ammonia_fraction=ammonia):.2f}"
        elif number == 54:
            mass, stock, target, final = re.search(
                r"MgCl₂·6H₂O ([\d.]+) g เป็นสารละลายสต็อก (\d+) cm³ "
                r"ต้องการ MgCl₂ ([\d.]+) mol/L ปริมาตร (\d+) cm³", stem,
            ).groups()
            expected = f"{q54.check(hydrate_g=float(mass), stock_ml=int(stock), target_molar=float(target), target_ml=int(final)):.1f}"
        elif number == 55:
            molar, density = re.search(
                r"H₂SO₄ ([\d.]+) mol/L มีความหนาแน่น ([\d.]+) g/cm³", stem,
            ).groups()
            expected = f"{q55.check(molar=float(molar), density=float(density)):.2f}"
        elif number == 56:
            percent, aliquot, final = re.search(
                r"NaClO ([\d.]+)% โดยมวลต่อปริมาตร ตวงมา ([\d.]+) cm³ "
                r"เติมน้ำจนได้ ([\d.]+) cm³", stem,
            ).groups()
            expected = f"{q56.check(percent_wv=float(percent), aliquot_ml=float(aliquot), final_ml=float(final)):.3f}"
        elif number == 57:
            volume, potassium, lead = re.search(
                r"สารละลาย (\d+) cm³ ให้ KNO₃ ([\d.]+) mol/L และ Pb\(NO₃\)₂ "
                r"([\d.]+) mol/L", stem,
            ).groups()
            k_mass, pb_mass = q57.check(volume_ml=int(volume), potassium_molar=float(potassium), lead_molar=float(lead))
            expected = f"{k_mass:.3f}, {pb_mass:.3f}"
        elif number == 58:
            stock_molar, chloride, target_molar = re.search(
                r"CdCl₂ ([\d.]+) mol/L มี Cl⁻ (\d+) mmol .*?"
                r"CdCl₂ ([\d.]+) mol/L", stem,
            ).groups()
            stock_ml, water_ml = q58.check(chloride_mmol=int(chloride),
                                            stock_molar=float(stock_molar),
                                            target_molar=float(target_molar))
            expected = f"{stock_ml:.1f}, {water_ml:.1f}"
        elif number == 59:
            first_molar, first_ml, second_molar, second_ml, final_ml = re.search(
                r"CaCl₂ ([\d.]+) mol/L ([\d.]+) cm³ กับ CaCl₂ "
                r"([\d.]+) mol/L ([\d.]+) cm³ แล้วเติมน้ำจนเป็น "
                r"([\d.]+) cm³", stem,
            ).groups()
            expected = f"{q59.check(first_molar=float(first_molar), first_ml=float(first_ml), second_molar=float(second_molar), second_ml=float(second_ml), final_ml=float(final_ml)):.1f}"
        elif number == 60:
            solution_freeze, benzene_freeze, benzene_kf, benzene_kb, sucrose_mol, water_kg, water_kb = re.search(
                r"A ของตัวละลายไม่แตกตัวในเบนซีนแข็งตัวที่ ([\d.]+) °C \(เบนซีนบริสุทธิ์ "
                r"([\d.]+) °C; Kf=([\d.]+), Kb=([\d.]+) °C/m\) "
                r"สารละลาย C มีซูโครส ([\d.]+) mol ในน้ำ ([\d.]+) kg "
                r"\(Kb น้ำ=([\d.]+) °C/m\)", stem,
            ).groups()
            expected = f"{q60.check(benzene_freeze=float(benzene_freeze), solution_freeze=float(solution_freeze), benzene_kf=float(benzene_kf), benzene_kb=float(benzene_kb), sucrose_mol=float(sucrose_mol), water_kg=float(water_kg), water_kb=float(water_kb)):.3f}"
        elif number == 61:
            d, offset = re.search(
                r"X²⁺ จัดเรียงอิเล็กตรอนเป็น \[Ar\]3d(\d+) "
                r"และ Y มีเลขอะตอมมากกว่า X (\d+)", stem,
            ).groups()
            x_config, y_config = q61.check(x2_d=int(d), y_offset=int(offset))
            expected = f"{x_config}; {y_config}"
        elif number == 62:
            formulas = tuple(re.search(r"พิจารณา ([A-Za-z0-9, ]+) สารใด", stem)[1].split(", "))
            high, high_ox, low, low_ox = q62.check(formulas=formulas)
            expected = f"{high} ({high_ox:+d}); {low} ({low_ox:+d})"
        elif number == 63:
            half_life, initial, decayed = re.search(
                r"I-131 มีครึ่งชีวิต ([\d.]+) วัน เริ่มต้น ([\d.]+) g "
                r"เมื่อสลายไป ([\d.]+)%", stem,
            ).groups()
            days, mass = q63.check(half_life_days=float(half_life),
                                   initial_g=float(initial), decayed_percent=float(decayed))
            expected = f"{days:.1f}, {mass:.1f}"
        elif number == 64:
            period = int(re.search(r"A อยู่หมู่ IA คาบ (\d+)", stem)[1])
            order, oxides = q64.check(metal_period=period)
            expected = f"{' < '.join(order)}; {', '.join(oxides)}"
        elif number == 65:
            sublimation, first_ie, second_ie, dissociation, affinity, formation = re.search(
                r"M\(s\)→M\(g\)=(-?\d+), IE₁=(-?\d+), IE₂=(-?\d+), "
                r"G₂→2G=(-?\d+), EA ของ G=(-?\d+), และ ΔHf\(MG₂\)=(-?\d+)", stem,
            ).groups()
            expected = str(q65.check(sublimation=int(sublimation), first_ie=int(first_ie),
                                     second_ie=int(second_ie), dissociation=int(dissociation),
                                     electron_affinity=int(affinity), formation=int(formation)))
        elif number == 66:
            hh, oo, oh, nn, nh = re.search(
                r"H–H=(\d+), O=O=(\d+), O–H=(\d+), N≡N=(\d+), N–H=(\d+)", stem,
            ).groups()
            water_type, ammonia_type, difference = q66.check(
                hh=int(hh), oo=int(oo), oh=int(oh), nn=int(nn), nh=int(nh),
            )
            expected = f"{water_type}; {ammonia_type}; {difference:.1f} kJ"
        elif number == 67:
            a, reacted, decomposed, d_molar, e_molar = re.search(
                r"เริ่ม A ([\d.]+) mol.*?ทำปฏิกิริยา ([\d.]+)% "
                r"และ C ที่เกิดสลาย ([\d.]+)% ถ้า D=(\d+) และ E=(\d+)", stem,
            ).groups()
            d_g, e_g = q67.check(initial_a_mol=float(a),
                                 a_reacted_percent=float(reacted),
                                 c_decomposed_percent=float(decomposed),
                                 d_molar=int(d_molar), e_molar=int(e_molar))
            expected = f"{d_g:.1f}, {e_g:.1f}"
        elif number == 68:
            sample, carbon_dioxide, water = re.search(
                r"มวล ([\d.]+) g เผากับ O₂ มากเกิน ได้ CO₂ ([\d.]+) g "
                r"และ H₂O ([\d.]+) g", stem,
            ).groups()
            expected = q68.check(sample_g=float(sample),
                                 carbon_dioxide_g=float(carbon_dioxide),
                                 water_g=float(water))
        elif number == 69:
            perchlorate = float(re.search(r"KClO₄ ([\d.]+) g ต้องใช้", stem)[1])
            chlorine, chloride = q69.check(perchlorate_g=perchlorate)
            expected = f"{chlorine:.1f}, {chloride:.1f}"
        else:
            solute, water, freezing, pure, kf = re.search(
                r"ไม่แตกตัว ([\d.]+) g ในน้ำ ([\d.]+) g สารละลายแข็งตัวที่ "
                r"(-?[\d.]+) °C \(น้ำบริสุทธิ์ (-?[\d.]+) °C, "
                r"Kf=([\d.]+) °C", stem,
            ).groups()
            molar_mass, molality = q70.check(solute_g=float(solute),
                                             water_g=float(water),
                                             solution_freeze_c=float(freezing),
                                             pure_freeze_c=float(pure),
                                             kf=float(kf))
            expected = f"{molar_mass:.1f}, {molality:.2f}"
        assert answer == expected
        assert len(question.choices) == 4
