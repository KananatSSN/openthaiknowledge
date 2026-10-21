"""Cross-check the 2561 chemistry pools and generated wording."""

import re
from random import Random

import pytest

from otk.core import generate
from otk.sheets.posn2561_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18,
)


def test_first_wave_solves_source_and_variants_independently():
    for module in (q01, q02, q03, q04, q05, q06, q07, q08, q09,
                   q10, q11, q12, q13, q14, q15, q16, q17, q18):
        assert module.solve(**module.PARAMS) == module.ANSWER
        for params in (module.PARAMS, *module.VARIANTS):
            assert module.solve(**params) == module.check(**params)


@pytest.mark.parametrize("number", range(1, 19))
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
        elif number == 3:
            a, b, c, d = map(int, re.search(
                r"A=(\d+) nm, B=(\d+) nm, C=(\d+) nm และ D=(\d+) nm", stem,
            ).groups())
            assert a > b > c > d
            assert answer == "พลังงานของ C มากกว่า B"
        elif number == 4:
            x_min, x_max, offset = map(int, re.search(
                r"เลขอะตอมตั้งแต่ (\d+) ถึง (\d+).*?มากกว่า X (\d+) ตัว", stem,
            ).groups())
            assert q04.check(x_min=x_min, x_max=x_max, offset=offset) == 1
            assert answer == "ธาตุ Z มีอิเล็กตรอนในชั้นที่สองมากกว่า 6 เสมอ"
        elif number == 5:
            from otk.sets.chemistry.olympiad.posn2561 import _ELECTRON_CONFIGS
            reverse = {configuration: z for z, configuration in _ELECTRON_CONFIGS.items()}
            options = tuple(reverse[choice.content[0].text] for choice in question.choices)
            assert reverse[answer] == q05.check(options=options)
        elif number == 6:
            data = {label: float(value) for label, value in re.findall(
                r"([LMQRT]): ([\d.]+)", stem,
            )}
            assert len(data) == 5
            false = [f"IE₂({left}) < IE₂({right})"
                     for left, right in zip("LMQR", "MQRT")
                     if not data[left] < data[right]]
            assert false == [answer]
        elif number == 7:
            radii = {species: int(value) for species, value in re.findall(
                r"(Na⁺|Br⁻|Na|Cl|Ca|Br)=(\d+)", stem,
            )}
            assert len(radii) == 6
            valid = [choice.content[0].text for choice in question.choices
                     if all(radii[left] > radii[right]
                            for left, right in zip(choice.content[0].text.split(" > "),
                                                   choice.content[0].text.split(" > ")[1:]))]
            assert valid == [answer]
        elif number == 8:
            labels = dict(re.findall(r"(P|Ca|As)=(P|Ca|As)", stem))
            assert len(labels) == 3
            reverse = {label: element for element, label in labels.items()}
            valid = []
            for choice in question.choices:
                name, order = choice.content[0].text.split(": ")
                property_name = {"IE₁": "ie", "EN": "en", "รัศมี": "radius",
                                 "จุดหลอมเหลว": "melting"}[name]
                values = [q08.PROPERTIES[property_name][reverse[label]]
                          for label in order.split(" > ")]
                if not values[0] > values[1] > values[2]:
                    valid.append(choice.content[0].text)
            assert valid == [answer]
        elif number == 9:
            products = {"BeO": None, "N₂O₅": "acid", "SiO₂": None,
                        "CaO": "base", "Cl₂O₇": "acid", "Al₂O₃": None,
                        "SO₃": "acid", "Na₂O": "base"}
            valid = []
            for choice in question.choices:
                x, y = re.match(r"X=(.*), Y=(.*)", choice.content[0].text).groups()
                if products[x] == "acid" and products[y] == "base":
                    valid.append(choice.content[0].text)
            assert valid == [answer]
        elif number == 10:
            assert "ชั้นสีม่วง" in stem and "น้ำร้อน" in stem
            assert answer == "สารประกอบ Y เป็น MgI₂ และละลายน้ำได้ดี"
            assert set(choice.content[0].text for choice in question.choices) == set(q10.CLAIMS)
        elif number == 11:
            label = re.search(r"ธาตุ ([DQXT]) อยู่คาบ 3", stem).group(1)
            assert answer == f"ธาตุ {label} มีเลขออกซิเดชันเป็นบวกในออกไซด์"
            assert set(choice.content[0].text for choice in question.choices) == set(
                q11.claims(label)
            )
        elif number == 12:
            color = {"K₂SO₄": False, "MnCl₂": True, "NaCl": False,
                     "Co(NO₃)₂": True, "K₂Cr₂O₇": True, "FeCl₃": True,
                     "[Ni(NH₃)₆]Cl₂": True, "RbCl": False}
            valid = []
            for choice in question.choices:
                left, right = choice.content[0].text.split(" และ ")
                if color[left] and color[right]:
                    valid.append(choice.content[0].text)
            assert valid == [answer]
        elif number == 13:
            assert "A ให้ตะกอนขาวเฉพาะกับ Na₂CO₃" in stem
            expected_cations = ("Mg", "K", "Ba")
            possible = []
            for choice in question.choices:
                formulas = re.findall(r"[ABC]=([^,]+)", choice.content[0].text)
                if len(formulas) == 3 and tuple(q13.CATIONS[f] for f in formulas) == expected_cations:
                    possible.append(choice.content[0].text)
            assert possible == [answer]
        elif number == 14:
            oxidation = {"K₄[Fe(CN)₆]": 2, "[Cr(NH₃)₆]Cl₃": 3}
            eligible = [choice.content[0].text for choice in question.choices
                        if choice.content[0].text in oxidation]
            assert answer == max(eligible, key=lambda compound: oxidation[compound])
        elif number == 15:
            z, a, daughter = map(int, re.search(
                r"เลขอะตอม (\d+) และเลขมวล (\d+).*?เลขอะตอม (\d+)", stem,
            ).groups())
            assert daughter == z + 1 and a > z
            assert answer == "β⁻"
        elif number == 16:
            initial, half_life = map(int, re.search(
                r"เริ่มต้นมวล (\d+) หน่วย และมีครึ่งชีวิต (\d+)", stem,
            ).groups())
            valid = []
            for choice in question.choices:
                masses = [int(value) for value in re.findall(r"m\(\d+\)=(\d+)",
                                                       choice.content[0].text)]
                if masses == [initial, initial // 2, initial // 4]:
                    valid.append(choice.content[0].text)
            assert valid == [answer]
            assert f"m({half_life})=" in answer
        elif number == 17:
            assert answer == "³₂He + ²₁H → ⁴₂He + ¹₁H"
            assert set(choice.content[0].text for choice in question.choices) == set(
                q17.REACTIONS
            )
        else:
            assignments = dict((label, int(z)) for label, z in re.findall(
                r"([ADLM])=(\d+)", stem,
            ))
            assert assignments == {"A": 7, "D": 16, "L": 20, "M": 37}
            valid = []
            for choice in question.choices:
                left, right = re.findall(r"[ADLM]", choice.content[0].text)
                if {assignments[left], assignments[right]} == {20, 37}:
                    valid.append(choice.content[0].text)
            assert valid == [answer]
        assert len(question.choices) == 4
