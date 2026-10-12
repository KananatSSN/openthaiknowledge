"""สูตรเคมีของสารตั้งต้น ผลิตภัณฑ์ และสัญลักษณ์ในสมการเคมี

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/20

Sets moved here from: science_wave_e8.
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

from otk.core.content import math, text
from otk.core.distractors import fixed, label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e8 import (
    EQUATIONS,
    HEAT,
    SUBJECT,
    UPPER_FIVE,
    Species,
    equation_tex,
    formula_tex,
)

PROVENANCE = Provenance("original")


TOPIC_EQUATION = "สูตรเคมีของสารตั้งต้น ผลิตภัณฑ์ และสัญลักษณ์ในสมการเคมี"


STATE_MEANING = {
    "s": "อยู่ในสถานะของแข็ง",
    "l": "อยู่ในสถานะของเหลว",
    "g": "อยู่ในสถานะเป็นแก๊ส",
    "aq": "เป็นสารละลายในน้ำ",
}


ATOMIC_MASS = {
    "H": Fraction(1), "C": Fraction(12), "N": Fraction(14), "O": Fraction(16),
    "Na": Fraction(23), "Mg": Fraction(24), "Al": Fraction(27), "S": Fraction(32),
    "Cl": Fraction(71, 2), "Ca": Fraction(40), "Fe": Fraction(56),
    "Cu": Fraction(127, 2), "Zn": Fraction(65), "Ag": Fraction(108),
    "Ba": Fraction(137),
}


_TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)")


def element_counts(formula: str) -> dict[str, int]:
    """Atoms of each element in one formula unit; a repeated symbol adds up."""
    counts: dict[str, int] = {}
    for symbol, digits in _TOKEN.findall(formula):
        counts[symbol] = counts.get(symbol, 0) + int(digits or 1)
    return counts


def side_counts(side: tuple[Species, ...]) -> dict[str, int]:
    total: dict[str, int] = {}
    for species in side:
        for symbol, n in element_counts(species.formula).items():
            total[symbol] = total.get(symbol, 0) + species.coef * n
    return total


def molar_mass(formula: str) -> Fraction:
    return sum((ATOMIC_MASS[s] * n for s, n in element_counts(formula).items()), Fraction(0))


def _formula_list(items) -> str:
    return r",\ ".join(formula_tex(s.formula) for s in items)


def _labelled_with_stem(*, stem: list, correct: str, wrongs: tuple[str, ...],
                        hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=stem,
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=TOPIC_EQUATION,
        hint=[text(hint)],
    )


OTHER_STATE = {"s": "aq", "aq": "s", "l": "g", "g": "l"}


def _restate(side, index):
    s = side[index]
    return tuple(Species(x.coef, x.formula, OTHER_STATE[s.state]) if i == index else x
                 for i, x in enumerate(side))


def _recoef(side, index, delta):
    return tuple(Species(x.coef + delta, x.formula, x.state) if i == index else x
                 for i, x in enumerate(side))


def _mass_text(value: Fraction) -> str:
    tenths = value * 10
    assert tenths.denominator == 1, value
    whole, part = divmod(int(tenths), 10)
    return f"{whole}.{part}" if part else f"{whole}"


@question_type(
    "chem.chemical_equation_foundation",
    display_name={"th": "ระบุสูตรเคมีของสารตั้งต้นและผลิตภัณฑ์จากสมการเคมี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class ChemicalEquationFoundation(QuestionType):
    """The first free verb: which formulas are reactants, which are products."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(EQUATIONS)
        side = rng.choice(("สารตั้งต้น", "ผลิตภัณฑ์"))
        wanted, other = ((eq.reactants, eq.products) if side == "สารตั้งต้น"
                         else (eq.products, eq.reactants))
        hint = "สารตั้งต้นเขียนทางซ้ายของลูกศร ผลิตภัณฑ์เขียนทางขวาของลูกศร"
        if rng.random() < 0.6:
            everything = (*eq.reactants, *eq.products)
            mixed = (wanted[0], other[0])
            wrongs = [_formula_list(other), _formula_list(everything), _formula_list(mixed)]
            if eq.condition not in (None, HEAT):
                # The catalyst over the arrow is neither reactant nor product.
                wrongs.insert(0, _formula_list(wanted) + r",\ " + formula_tex(eq.condition))
            return GeneratedQuestion(
                stem=[text("จากสมการเคมี "), math(equation_tex(eq)),
                      text(f" {side}ทั้งหมดของปฏิกิริยานี้คือข้อใด")],
                correct=[math(_formula_list(wanted))],
                distractors=fixed(*[[math(w)] for w in wrongs]),
                topic=TOPIC_EQUATION, hint=[text(hint)],
            )
        # One formula: which of these is a {side}?
        answer = rng.choice(wanted)
        present = {s.formula for s in (*eq.reactants, *eq.products)}
        outsiders = sorted({s.formula for e in EQUATIONS for s in (*e.reactants, *e.products)}
                           - present)
        wrongs = [s.formula for s in other] + rng.sample(outsiders, 3)
        return GeneratedQuestion(
            stem=[text("จากสมการเคมี "), math(equation_tex(eq)),
                  text(f" สารในข้อใดเป็น{side}ของปฏิกิริยานี้")],
            correct=[math(formula_tex(answer.formula))],
            distractors=fixed(*[[math(formula_tex(w))] for w in wrongs]),
            topic=TOPIC_EQUATION, hint=[text(hint)],
        )


@question_type(
    "chem.chemical_equation_fluency",
    display_name={"th": "แปลความหมายของสัญลักษณ์ในสมการเคมี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class ChemicalEquationFluency(QuestionType):
    """The second free verb: state symbols, coefficients, subscripts, the arrow's
    label, and counting atoms from coefficient × subscript."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(EQUATIONS)
        shape = rng.random()
        stem_eq = [text("จากสมการเคมี "), math(equation_tex(eq))]
        if shape < 0.2:
            return self._state(rng, eq, stem_eq)
        if shape < 0.4:
            return self._coefficient(rng, eq, stem_eq)
        if shape < 0.55:
            return self._subscript(rng, eq, stem_eq)
        if shape < 0.7 and eq.condition is not None:
            return self._condition(eq, stem_eq)
        return self._count(rng, eq, stem_eq)

    @staticmethod
    def _state(rng, eq, stem_eq):
        species = rng.choice((*eq.reactants, *eq.products))
        name = formula_tex(species.formula)
        correct = STATE_MEANING[species.state]
        return GeneratedQuestion(
            stem=[*stem_eq, text(f" สัญลักษณ์ ({species.state}) ที่เขียนกำกับ "), math(name),
                  text(" หมายถึงข้อใด")],
            correct=[text(correct)],
            distractors=label_pool(list(STATE_MEANING.values())),
            topic=TOPIC_EQUATION,
            hint=[text("(s) ของแข็ง (l) ของเหลว (g) แก๊ส (aq) สารละลายในน้ำ")],
        )

    @staticmethod
    def _coefficient(rng, eq, stem_eq):
        choices = [s for s in (*eq.reactants, *eq.products) if s.coef >= 2]
        if not choices:
            eq = rng.choice([e for e in EQUATIONS
                             if any(s.coef >= 2 for s in (*e.reactants, *e.products))])
            stem_eq = [text("จากสมการเคมี "), math(equation_tex(eq))]
            choices = [s for s in (*eq.reactants, *eq.products) if s.coef >= 2]
        species = rng.choice(choices)
        c = species.coef
        correct = f"สารนี้มี {c} โมล ตามอัตราส่วนโดยโมลในสมการ"
        return _labelled_with_stem(
            stem=[*stem_eq, text(f" เลข {c} ที่เขียนหน้า "), math(formula_tex(species.formula)),
                  text(" หมายถึงข้อใด")],
            correct=correct,
            wrongs=(f"สารนี้มีมวล {c} กรัม ตามมวลของสารในสมการ",
                    f"สารนี้หนึ่งหน่วยมีอะตอมทั้งหมด {c} อะตอม",
                    f"สารนี้มีความเข้มข้น {c} โมลต่อลิตร"),
            hint="เลขสัมประสิทธิ์หน้าสูตรบอกจำนวนโมล (อัตราส่วนโดยโมล) ส่วนเลขห้อยท้ายธาตุบอกจำนวนอะตอมในหนึ่งหน่วยสูตร",
        )

    @staticmethod
    def _subscript(rng, eq, stem_eq):
        options = []
        for s in (*eq.reactants, *eq.products):
            tokens = _TOKEN.findall(s.formula)
            symbols = [sym for sym, _ in tokens]
            for sym, digits in tokens:
                if digits and int(digits) >= 2 and symbols.count(sym) == 1:
                    options.append((s, sym, int(digits)))
        if not options:
            return ChemicalEquationFluency._count(rng, eq, stem_eq)
        species, symbol, n = rng.choice(options)
        return _labelled_with_stem(
            stem=[*stem_eq, text(f" เลข {n} ที่ห้อยท้ายธาตุ {symbol} ใน "),
                  math(formula_tex(species.formula)), text(" หมายถึงข้อใด")],
            correct=f"หนึ่งหน่วยสูตรมีอะตอม {symbol} อยู่ {n} อะตอม",
            wrongs=(f"สารนี้มีจำนวน {n} โมลในปฏิกิริยา",
                    f"อะตอม {symbol} มีประจุ {n}+ ในสารประกอบนี้",
                    f"ธาตุ {symbol} มีมวล {n} กรัม ในหนึ่งหน่วยสูตร"),
            hint="เลขห้อยท้ายธาตุบอกจำนวนอะตอมของธาตุนั้นในหนึ่งหน่วยสูตร ส่วนเลขหน้าสูตรบอกจำนวนโมล",
        )

    @staticmethod
    def _condition(eq, stem_eq):
        if eq.condition == HEAT:
            return _labelled_with_stem(
                stem=[*stem_eq, text(" สัญลักษณ์ Δ ที่เขียนเหนือลูกศรหมายถึงข้อใด")],
                correct="ต้องให้ความร้อนแก่สารตั้งต้นเพื่อให้เกิดปฏิกิริยา",
                wrongs=("ปฏิกิริยานี้คายความร้อนออกมา",
                        "ปฏิกิริยานี้ต้องใช้ตัวเร่งปฏิกิริยา",
                        "ผลิตภัณฑ์ที่ได้เป็นแก๊สทั้งหมด"),
                hint="สิ่งที่เขียนเหนือลูกศรคือภาวะที่ต้องใช้ให้ปฏิกิริยาเกิด ไม่ใช่สารตั้งต้นหรือผลิตภัณฑ์",
            )
        cat = formula_tex(eq.condition)
        return _labelled_with_stem(
            stem=[*stem_eq, text(" สาร "), math(cat), text(" ที่เขียนเหนือลูกศรทำหน้าที่ใด")],
            correct="เป็นตัวเร่งปฏิกิริยา ช่วยให้เกิดเร็วขึ้นโดยไม่ถูกใช้หมด",
            wrongs=("เป็นสารตั้งต้นที่ถูกใช้หมดไปในปฏิกิริยานี้",
                    "เป็นผลิตภัณฑ์ที่เกิดขึ้นจากปฏิกิริยา",
                    "บอกว่าต้องให้ความร้อนแก่สารตั้งต้น"),
            hint="สิ่งที่เขียนเหนือลูกศรคือภาวะที่ต้องใช้ให้ปฏิกิริยาเกิด ไม่ใช่สารตั้งต้นหรือผลิตภัณฑ์",
        )

    @staticmethod
    def _count(rng, eq, stem_eq):
        side_name, side = rng.choice((("สารตั้งต้น", eq.reactants), ("ผลิตภัณฑ์", eq.products)))
        counts = side_counts(side)
        symbol = rng.choice(sorted(counts))
        answer = counts[symbol]
        # Forgetting the coefficients is the mistake this shape exists to catch.
        bare = sum(element_counts(s.formula).get(symbol, 0) for s in side)
        wrongs = [bare, answer + 1, answer - 1, answer * 2, answer + 2, answer + 3]
        return GeneratedQuestion(
            stem=[*stem_eq, text(f" ทางด้าน{side_name}มีอะตอมของธาตุ {symbol} รวมทั้งหมดกี่อะตอม "
                               "(คิดตามเลขสัมประสิทธิ์ในสมการ)")],
            correct=[text(f"{answer} อะตอม")],
            distractors=fixed(*[[text(f"{w} อะตอม")] for w in wrongs if w > 0]),
            topic=TOPIC_EQUATION,
            hint=[text("จำนวนอะตอม = เลขสัมประสิทธิ์หน้าสูตร × เลขห้อยท้ายธาตุ แล้วรวมทุกสารในด้านนั้น")],
        )


@question_type(
    "chem.chemical_equation_application",
    display_name={"th": "เขียนสมการเคมีจากข้อความ ดุลสมการ และใช้กฎทรงมวล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class ChemicalEquationApplication(QuestionType):
    """Put the symbols to work: the equation for a described reaction, the
    missing coefficient that balances it, and a mass read off conservation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(EQUATIONS)
        shape = rng.random()
        if shape < 0.35:
            return self._from_words(rng, eq)
        if shape < 0.7:
            return self._missing_coefficient(rng, eq)
        return self._conservation(rng, eq)

    @staticmethod
    def _from_words(rng, eq):
        side_index = rng.randrange(len(eq.products))
        unbalanced = _recoef(eq.reactants, rng.randrange(len(eq.reactants)), 1)
        wrongs = (
            equation_tex(eq, products=_restate(eq.products, side_index)),
            equation_tex(eq, reactants=eq.products, products=eq.reactants),
            equation_tex(eq, reactants=unbalanced),
        )
        return GeneratedQuestion(
            stem=[text(f"{eq.thai} เขียนเป็นสมการเคมีที่ดุลแล้วได้ตรงกับข้อใด")],
            correct=[math(equation_tex(eq))],
            distractors=fixed(*[[math(w)] for w in wrongs]),
            topic=TOPIC_EQUATION,
            hint=[text("ตรวจทีละเรื่อง: สารตั้งต้นอยู่ซ้ายลูกศร สถานะตรงกับข้อความ "
                       "และจำนวนอะตอมของแต่ละธาตุสองข้างเท่ากัน")],
        )

    @staticmethod
    def _missing_coefficient(rng, eq):
        blank = rng.choice((*eq.reactants, *eq.products))
        answer = blank.coef
        wrongs = [n for n in (answer + 1, answer - 1, answer + 2, answer * 2, 1, 2, 3, 4)
                  if n > 0 and n != answer]
        return GeneratedQuestion(
            stem=[text("เลขสัมประสิทธิ์ที่เติมใน □ แล้วทำให้สมการเคมีต่อไปนี้ดุลคือเท่าใด "),
                  math(equation_tex(eq, blank=blank))],
            correct=[math(str(answer))],
            distractors=fixed(*[[math(str(n))] for n in wrongs]),
            topic=TOPIC_EQUATION,
            hint=[text("นับอะตอมของธาตุที่อยู่ในสารตัวที่เว้นว่างไว้ทั้งสองข้างของลูกศร "
                       "แล้วเลือกเลขที่ทำให้จำนวนอะตอมเท่ากัน")],
        )

    @staticmethod
    def _conservation(rng, eq):
        # Scale the molar masses so every mass is a whole number of tenths of a gram.
        species = (*eq.reactants, *eq.products)
        scales = [Fraction(k, 10) for k in (1, 2, 3, 4, 5, 10)
                  if all((s.coef * molar_mass(s.formula) * k).denominator == 1
                         for s in species)]
        scale = rng.choice(scales)
        mass = {s: s.coef * molar_mass(s.formula) * scale for s in species}
        asked = rng.choice(eq.products)
        answer = mass[asked]

        def listing(items):
            blocks = []
            for i, s in enumerate(items):
                blocks += [text(" และ " if i else " "), math(formula_tex(s.formula)),
                           text(f" {_mass_text(mass[s])} กรัม")]
            return blocks

        others = [s for s in eq.products if s != asked]
        total_in = sum(mass[s] for s in eq.reactants)
        wrongs = [total_in, answer + Fraction(1), answer - Fraction(1), answer * 2,
                  answer + Fraction(2)]
        return GeneratedQuestion(
            stem=[text("จากสมการเคมี "), math(equation_tex(eq)),
                  text(" ถ้าสารตั้งต้นทำปฏิกิริยากันพอดี โดยใช้"), *listing(eq.reactants),
                  *([text(" ได้"), *listing(others)] if others else []),
                  text(" จะได้ "), math(formula_tex(asked.formula)), text(" กี่กรัม")],
            correct=[text(f"{_mass_text(answer)} กรัม")],
            distractors=fixed(*[[text(f"{_mass_text(w)} กรัม")] for w in wrongs
                                if w > 0 and (w * 10).denominator == 1]),
            topic=TOPIC_EQUATION,
            hint=[text("กฎทรงมวล: มวลของสารตั้งต้นทั้งหมดเท่ากับมวลของผลิตภัณฑ์ทั้งหมด")],
        )
