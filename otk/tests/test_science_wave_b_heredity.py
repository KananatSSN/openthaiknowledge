"""Acceptance tests for Wave B — all of ``ว 1.3``, classification to evolution.

One file for all twenty-four indicators. ``ว 1.3`` runs from ป.2 to ม.4 as a
single argument — sort living things, then sort them into groups, then account
for the groups by heredity and evolution — and the filing rules are only legible
with the whole standard in view.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_B_KEYS
from otk.sets.biology.p4.organism_group import GROUPS, ORGANISMS
from otk.sets.biology.p4.flowering_group import PLANTS
from otk.sets.biology.p2.living_thing import THINGS
from otk.sets.biology.p4.vertebrate_group import BACKBONE
from otk.sets.biology.p4.vertebrate_class import CLASSES
from otk.sets.biology.p5.inherited_trait import INHERITED, OBSERVED
from otk.sets.biology.m3.monohybrid import CROSSES
from otk.sets._support.science_wave_b25 import MENDEL_TRAITS, _genotypes
from otk.sets.biology.m3.gene_dna import MODELS
from otk.sets.biology.p5.family_question import WONDERINGS
from otk.sets.biology.m3.division_compare import ASPECTS, SITUATIONS
from otk.sets.biology.m3.genetic_disease import DISEASES
from otk.sets.biology.m3.genotypes_and_offspring_ratios import (
    PARENT_PAIRS,
    _genotype_ratio,
    _phenotype_ratio,
)
from otk.sets.biology.m3.gmo_argument import CLAIMS
from otk.sets.biology.m3.genetic_counsel import COUPLES
from otk.sets.biology.m3.gmo_use import GMOS
from otk.sets.biology.m3.biodiversity_compare import ECOSYSTEMS
from otk.sets.biology.m3.biodiversity_value import LOSSES, VALUES
from otk.sets.biology.m4.sex_linkage import (
    BLOOD_GENOTYPES,
    SEX_CROSSES,
    _blood_group,
    _possible_groups,
)
from otk.sets.biology.m4.protein_synthesis import CHAINS
from otk.sets.biology.m4.mutation_effect import CHANGES
from otk.sets.biology.m4.evolution_diversity import EXAMPLES
from otk.sets.biology.m4.mutation_use import MUTATION_USES
from otk.sets.biology.m4.dna_technology import TECHNOLOGIES


# key -> (indicator, stage, mapping status)
NEW_KEYS = {
    "life.living_thing_foundation": ("ว 1.3 ป.2/1", 1, "standard_scope"),
    "life.living_thing_fluency": ("ว 1.3 ป.2/1", 2, "exact"),
    "life.living_thing_application": ("ว 1.3 ป.2/1", 3, "standard_scope"),
    "life.organism_group_foundation": ("ว 1.3 ป.4/1", 1, "standard_scope"),
    "life.organism_group_fluency": ("ว 1.3 ป.4/1", 2, "exact"),
    "life.organism_group_application": ("ว 1.3 ป.4/1", 3, "standard_scope"),
    "plant.flowering_group_foundation": ("ว 1.3 ป.4/2", 1, "standard_scope"),
    "plant.flowering_group_fluency": ("ว 1.3 ป.4/2", 2, "exact"),
    "plant.flowering_group_application": ("ว 1.3 ป.4/2", 3, "standard_scope"),
    "animal.vertebrate_group_foundation": ("ว 1.3 ป.4/3", 1, "standard_scope"),
    "animal.vertebrate_group_fluency": ("ว 1.3 ป.4/3", 2, "exact"),
    "animal.vertebrate_group_application": ("ว 1.3 ป.4/3", 3, "standard_scope"),
    "animal.vertebrate_class_foundation": ("ว 1.3 ป.4/4", 1, "exact"),
    "animal.vertebrate_class_fluency": ("ว 1.3 ป.4/4", 2, "exact"),
    "animal.vertebrate_class_application": ("ว 1.3 ป.4/4", 3, "standard_scope"),
    "life.inherited_trait_foundation": ("ว 1.3 ป.5/1", 1, "exact"),
    "life.inherited_trait_fluency": ("ว 1.3 ป.5/1", 2, "exact"),
    "life.inherited_trait_application": ("ว 1.3 ป.5/1", 3, "standard_scope"),
    "life.family_question_foundation": ("ว 1.3 ป.5/2", 1, "standard_scope"),
    "life.family_question_fluency": ("ว 1.3 ป.5/2", 2, "standard_scope"),
    "life.family_question_application": ("ว 1.3 ป.5/2", 3, "standard_scope"),
    "cell.gene_dna_foundation": ("ว 1.3 ม.3/1", 1, "standard_scope"),
    "cell.gene_dna_fluency": ("ว 1.3 ม.3/1", 2, "exact"),
    "cell.gene_dna_application": ("ว 1.3 ม.3/1", 3, "standard_scope"),
    "life.monohybrid_foundation": ("ว 1.3 ม.3/2", 1, "exact"),
    "life.monohybrid_fluency": ("ว 1.3 ม.3/2", 2, "exact"),
    "life.monohybrid_application": ("ว 1.3 ม.3/2", 3, "standard_scope"),
    "life.punnett_foundation": ("ว 1.3 ม.3/3", 1, "exact"),
    "life.punnett_fluency": ("ว 1.3 ม.3/3", 2, "exact"),
    "life.punnett_application": ("ว 1.3 ม.3/3", 3, "standard_scope"),
    "cell.division_compare_foundation": ("ว 1.3 ม.3/4", 1, "exact"),
    "cell.division_compare_fluency": ("ว 1.3 ม.3/4", 2, "exact"),
    "cell.division_compare_application": ("ว 1.3 ม.3/4", 3, "standard_scope"),
    "life.genetic_disease_foundation": ("ว 1.3 ม.3/5", 1, "exact"),
    "life.genetic_disease_fluency": ("ว 1.3 ม.3/5", 2, "exact"),
    "life.genetic_disease_application": ("ว 1.3 ม.3/5", 3, "standard_scope"),
    "life.genetic_counsel_foundation": ("ว 1.3 ม.3/6", 1, "standard_scope"),
    "life.genetic_counsel_fluency": ("ว 1.3 ม.3/6", 2, "exact"),
    "life.genetic_counsel_application": ("ว 1.3 ม.3/6", 3, "standard_scope"),
    "life.gmo_use_foundation": ("ว 1.3 ม.3/7", 1, "exact"),
    "life.gmo_use_fluency": ("ว 1.3 ม.3/7", 2, "exact"),
    "life.gmo_use_application": ("ว 1.3 ม.3/7", 3, "standard_scope"),
    "life.gmo_argument_foundation": ("ว 1.3 ม.3/8", 1, "standard_scope"),
    "life.gmo_argument_fluency": ("ว 1.3 ม.3/8", 2, "standard_scope"),
    "life.gmo_argument_application": ("ว 1.3 ม.3/8", 3, "standard_scope"),
    "ecology.biodiversity_compare_foundation": ("ว 1.3 ม.3/9", 1,
                                                "standard_scope"),
    "ecology.biodiversity_compare_fluency": ("ว 1.3 ม.3/9", 2, "exact"),
    "ecology.biodiversity_compare_application": ("ว 1.3 ม.3/9", 3,
                                                 "standard_scope"),
    "ecology.biodiversity_value_foundation": ("ว 1.3 ม.3/10", 1, "exact"),
    "ecology.biodiversity_value_fluency": ("ว 1.3 ม.3/10", 2, "exact"),
    "ecology.biodiversity_value_application": ("ว 1.3 ม.3/10", 3,
                                               "standard_scope"),
    "ecology.biodiversity_care_foundation": ("ว 1.3 ม.3/11", 1,
                                             "standard_scope"),
    "ecology.biodiversity_care_fluency": ("ว 1.3 ม.3/11", 2, "standard_scope"),
    "ecology.biodiversity_care_application": ("ว 1.3 ม.3/11", 3,
                                              "standard_scope"),
    "cell.protein_synthesis_foundation": ("ว 1.3 ม.4/1", 1, "exact"),
    "cell.protein_synthesis_fluency": ("ว 1.3 ม.4/1", 2, "exact"),
    "cell.protein_synthesis_application": ("ว 1.3 ม.4/1", 3, "standard_scope"),
    "life.sex_linkage_foundation": ("ว 1.3 ม.4/2", 1, "exact"),
    "life.sex_linkage_fluency": ("ว 1.3 ม.4/2", 2, "exact"),
    "life.sex_linkage_application": ("ว 1.3 ม.4/2", 3, "standard_scope"),
    "life.mutation_effect_foundation": ("ว 1.3 ม.4/3", 1, "exact"),
    "life.mutation_effect_fluency": ("ว 1.3 ม.4/3", 2, "exact"),
    "life.mutation_effect_application": ("ว 1.3 ม.4/3", 3, "standard_scope"),
    "life.mutation_use_foundation": ("ว 1.3 ม.4/4", 1, "standard_scope"),
    "life.mutation_use_fluency": ("ว 1.3 ม.4/4", 2, "exact"),
    "life.mutation_use_application": ("ว 1.3 ม.4/4", 3, "standard_scope"),
    "life.dna_technology_foundation": ("ว 1.3 ม.4/5", 1, "standard_scope"),
    "life.dna_technology_fluency": ("ว 1.3 ม.4/5", 2, "exact"),
    "life.dna_technology_application": ("ว 1.3 ม.4/5", 3, "standard_scope"),
    "life.evolution_diversity_foundation": ("ว 1.3 ม.4/6", 1, "exact"),
    "life.evolution_diversity_fluency": ("ว 1.3 ม.4/6", 2, "exact"),
    "life.evolution_diversity_application": ("ว 1.3 ม.4/6", 3, "standard_scope"),
}
LEVELS = {"ว 1.3 ป.2/1": "ป.2", "ว 1.3 ป.5/1": "ป.5", "ว 1.3 ป.5/2": "ป.5"}
ROOT = Path(__file__).resolve().parents[2]

# The two ``ตระหนัก`` outcomes in ``ว 1.3`` whose evidence clause is an act:
# ``ม.3/8`` โดยการเผยแพร่ความรู้ and ``ม.3/11`` โดยมีส่วนร่วมในการดูแลรักษา.
# ``ป.5/2`` is the same shape — its evidence is ``โดยการถามคำถาม``.
CONDUCT_OUTCOMES = ("ว 1.3 ป.5/2", "ว 1.3 ม.3/8", "ว 1.3 ม.3/11")


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def _outcomes() -> dict:
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        return {row["outcome_code"]: row for row in csv.DictReader(handle)}


def test_heredity_sets_are_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert len(NEW_KEYS) == 72
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_B_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcome, stage, status) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [outcome], key
        assert rows[key]["mapping_status"] == status, key
        expected = LEVELS.get(outcome, outcome.split()[-1].split("/")[0])
        assert rows[key]["level"] == expected, key


def test_an_outcome_whose_evidence_is_an_act_has_no_exact_set():
    """``ป.5/2``, ``ม.3/8`` and ``ม.3/11`` are filed by their evidence clause."""
    rows = {row["key"]: row for row in catalog()}
    for outcome in CONDUCT_OUTCOMES:
        filed = {rows[key]["mapping_status"]
                 for key, (code, _, _) in NEW_KEYS.items() if code == outcome}
        assert filed == {"standard_scope"}, outcome


def test_the_tranak_outcome_whose_evidence_is_knowing_does_have_an_exact_set():
    """``ม.3/6`` says ``โดยรู้ว่า…``, which an item can ask for directly.

    This is the counterpart to the test above: the word ``ตระหนัก`` does not
    settle the filing — the evidence clause does.
    """
    rows = {row["key"]: row for row in catalog()}
    exact = {key for key, (code, _, _) in NEW_KEYS.items()
             if code == "ว 1.3 ม.3/6" and rows[key]["mapping_status"] == "exact"}
    assert exact == {"life.genetic_counsel_fluency"}


def test_a_sorting_verb_puts_the_exact_set_at_fluency():
    """``เปรียบเทียบ`` and ``จำแนก`` are done by the set that sorts a case."""
    rows = {row["key"]: row for row in catalog()}
    for outcome in ("ว 1.3 ป.2/1", "ว 1.3 ป.4/1", "ว 1.3 ป.4/2", "ว 1.3 ป.4/3",
                    "ว 1.3 ม.3/9"):
        exact = {key for key, (code, _, _) in NEW_KEYS.items()
                 if code == outcome and rows[key]["mapping_status"] == "exact"}
        assert len(exact) == 1, outcome
        assert next(iter(exact)).endswith("_fluency"), outcome


def test_an_outcome_opening_with_a_search_files_only_the_free_half():
    """``ม.4/4`` and ``ม.4/5`` open with ``สืบค้นข้อมูล``, which cannot be asked."""
    rows = {row["key"]: row for row in catalog()}
    for outcome, expected in (("ว 1.3 ม.4/4", {"life.mutation_use_fluency"}),
                              ("ว 1.3 ม.4/5", {"life.dna_technology_fluency"})):
        exact = {key for key, (code, _, _) in NEW_KEYS.items()
                 if code == outcome and rows[key]["mapping_status"] == "exact"}
        assert exact == expected, outcome


def test_no_application_set_in_this_standard_claims_an_exact_indicator():
    rows = {row["key"]: row for row in catalog()}
    for key, (_, stage, _) in NEW_KEYS.items():
        if stage == 3:
            assert rows[key]["mapping_status"] == "standard_scope", key


def test_the_three_group_indicator_is_covered_across_all_three_groups():
    """``ป.4/1`` names three groups; the third is the one usually dropped."""
    assert {group.name for group in GROUPS} == {
        "กลุ่มพืช", "กลุ่มสัตว์", "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์"}
    covered = {organism.group for organism in ORGANISMS}
    assert covered == {group.name for group in GROUPS}
    neither = [organism.name for organism in ORGANISMS
               if organism.group == "กลุ่มที่ไม่ใช่พืชและไม่ใช่สัตว์"]
    assert len(neither) >= 3, neither


def test_the_five_vertebrate_groups_are_all_present_with_examples():
    """``ป.4/4`` names five groups by name, so all five must be reachable."""
    assert len(CLASSES) == 5
    names = [item.name for item in CLASSES]
    assert names == ["กลุ่มปลา", "กลุ่มสัตว์สะเทินน้ำสะเทินบก",
                     "กลุ่มสัตว์เลื้อยคลาน", "กลุ่มนก",
                     "กลุ่มสัตว์เลี้ยงลูกด้วยน้ำนม"]
    seen = set()
    for item in CLASSES:
        assert len(item.examples) >= 3, item.name
        assert not seen & set(item.examples), item.name
        seen |= set(item.examples)


def test_both_verdicts_are_present_in_every_two_way_sorting_table():
    """A table with only one verdict would make the sorting item guessable."""
    for name, table, field in (("things", THINGS, "verdict"),
                               ("plants", PLANTS, "group"),
                               ("backbone", BACKBONE, "group")):
        values = {getattr(item, field).split(" เพราะ")[0] for item in table}
        assert len(values) == 2, (name, values)


def test_the_inherited_trait_table_spans_plants_animals_and_humans():
    """``ป.5/1`` names all three, so the ``exact`` sets must reach all three."""
    assert {item.kind for item in INHERITED} == {"พืช", "สัตว์", "มนุษย์"}
    verdicts = {item.verdict.split(" เพราะ")[0] for item in OBSERVED}
    assert verdicts == {"เป็นลักษณะทางพันธุกรรม", "ไม่ใช่ลักษณะทางพันธุกรรม"}


def test_the_ratio_answers_are_computed_from_the_cross_that_was_stated():
    """Every ``ม.3/3`` answer is recomputed here from the parents in the stem."""
    checked = {"genotype": 0, "phenotype": 0}
    for seed in range(900):
        question = generate("life.punnett_fluency", random.Random(seed))
        stem, answer = _text(question.stem), _answer(question)
        trait = next(item for item in MENDEL_TRAITS if item.subject in stem)
        codes = _genotypes(trait)
        pair = stem.split("เมื่อผสม ")[1].split(" ")
        one, two = pair[0], pair[2]
        assert one in codes and two in codes, stem
        if "จีโนไทป์" in stem.split("ลูก")[-1] or "อัตราส่วนของจีโนไทป์" in stem:
            checked["genotype"] += 1
            assert answer == _genotype_ratio(trait, one, two), stem
        else:
            checked["phenotype"] += 1
            assert answer == _phenotype_ratio(trait, one, two), stem
    assert all(checked.values()), checked


def test_every_monohybrid_cross_and_ratio_is_reachable():
    assert len(CROSSES) == 6
    assert len(PARENT_PAIRS) == 9
    trait = MENDEL_TRAITS[0]
    codes = _genotypes(trait)
    genotypes = {_genotype_ratio(trait, codes[a], codes[b])
                 for a, b in PARENT_PAIRS}
    phenotypes = {_phenotype_ratio(trait, codes[a], codes[b])
                  for a, b in PARENT_PAIRS}
    # Four choices need four distinct values to draw from on each branch.
    assert len(genotypes) >= 4, genotypes
    assert len(phenotypes) >= 4, phenotypes


def test_the_blood_group_answers_follow_from_the_alleles():
    assert _blood_group(("IA", "IB")) == "AB"
    assert _blood_group(("IA", "i")) == "A"
    assert _blood_group(("IB", "i")) == "B"
    assert _blood_group(("i", "i")) == "O"
    # An AB parent can never give an i allele, so no child of theirs is O.
    for other in BLOOD_GENOTYPES:
        assert "O" not in _possible_groups(("IA", "IB"), other)
    assert _possible_groups(("i", "i"), ("i", "i")) == "ลูกอาจมีหมู่เลือด O เท่านั้น"


def test_the_sex_linkage_fluency_answers_come_from_its_own_tables():
    parents = {item.parents: item.outcome for item in SEX_CROSSES}
    checked = {"sex": 0, "blood": 0}
    for seed in range(900):
        question = generate("life.sex_linkage_fluency", random.Random(seed))
        stem, answer = _text(question.stem), _answer(question)
        match = next((key for key in parents if key in stem), None)
        if match is not None:
            checked["sex"] += 1
            assert answer == parents[match], stem
            continue
        checked["blood"] += 1
        assert answer.startswith("ลูกอาจมีหมู่เลือด "), stem
    assert all(checked.values()), checked


def test_the_two_kinds_of_genetic_disease_are_both_represented():
    kinds = {item.kind for item in DISEASES}
    assert kinds == {"การเปลี่ยนแปลงของยีน", "การเปลี่ยนแปลงของโครโมโซม"}
    for kind in kinds:
        # Three wrong choices are drawn from the other kind, so each side needs
        # at least three rows.
        assert sum(1 for item in DISEASES if item.kind == kind) >= 4, kind


def test_the_division_aspects_all_distinguish_the_two_kinds():
    """An aspect the two agree on would give an item three identical choices."""
    assert len(ASPECTS) >= 5
    for item in ASPECTS:
        assert item.mitosis != item.meiosis, item.aspect
    verdicts = {item.verdict.split(" เพราะ")[0] for item in SITUATIONS}
    assert verdicts == {"ไมโทซิส", "ไมโอซิส"}


def test_every_gmo_carries_both_a_benefit_and_a_concern():
    """``ม.3/7`` names ``ผลกระทบ`` alongside ``การใช้ประโยชน์``."""
    assert len(GMOS) >= 6
    for field in ("name", "benefit", "impact"):
        values = [getattr(item, field) for item in GMOS]
        assert len(values) == len(set(values)), field


def test_the_claim_table_holds_both_supported_and_unsupported_statements():
    supported = [item for item in CLAIMS if "มีข้อมูลสนับสนุน" in item.verdict]
    assert len(supported) >= 2
    assert len(CLAIMS) - len(supported) >= 3


def test_every_couple_situation_names_a_distinct_step():
    steps = [item.step for item in COUPLES]
    assert len(steps) == len(set(steps)) >= 6


def test_the_ecosystem_ranks_are_strictly_ordered():
    """Two ecosystems sharing a rank would make the comparison unanswerable."""
    ranks = [item.rank for item in ECOSYSTEMS]
    assert len(ranks) == len(set(ranks)) >= 6
    by_rank = sorted(ECOSYSTEMS, key=lambda item: item.rank)
    assert by_rank[0].name == "ทะเลทราย"
    assert by_rank[-1].name == "ป่าดิบชื้น"


def test_biodiversity_value_covers_both_the_ecosystem_and_people():
    """``ม.3/10`` names both, and the distractors come from the other side."""
    beneficiaries = {item.beneficiary for item in VALUES}
    assert beneficiaries == {"ระบบนิเวศ", "มนุษย์"}
    for beneficiary in beneficiaries:
        assert sum(1 for item in VALUES
                   if item.beneficiary == beneficiary) >= 3, beneficiary
    consequences = [item.consequence for item in LOSSES]
    assert len(consequences) == len(set(consequences)) >= 6


def test_every_protein_answer_carries_the_whole_gene_to_trait_chain():
    """``ม.4/1`` names three things; a protein alone does not answer it."""
    assert len(CHAINS) >= 6
    for field in ("gene", "protein", "trait"):
        values = [getattr(item, field) for item in CHAINS]
        assert len(values) == len(set(values)), field
    wanted = {item.gene: f"กำหนดให้สร้าง{item.protein} ซึ่งทำให้เกิด{item.trait}"
              for item in CHAINS}
    seen = set()
    for seed in range(600):
        question = generate("cell.protein_synthesis_fluency", random.Random(seed))
        stem = _text(question.stem)
        gene = next(key for key in wanted if f"“{key}”" in stem)
        seen.add(gene)
        assert _answer(question) == wanted[gene], stem
    assert seen == set(wanted)


def test_the_mutation_change_table_covers_both_substitution_and_frameshift():
    assert len(CHANGES) >= 6
    effects = [item.effect for item in CHANGES]
    assert len(effects) == len(set(effects))
    joined = " ".join(item.change for item in CHANGES)
    assert "แทนที่" in joined and "เพิ่มเข้ามา" in joined and "ขาดหายไป" in joined


def test_the_dna_technology_effects_name_both_parties():
    """``ม.4/5`` names ``มนุษย์`` and ``สิ่งแวดล้อม``, so both must appear."""
    parties = {item.effect.split(" ")[0] for item in TECHNOLOGIES}
    assert parties == {"ต่อมนุษย์", "ต่อสิ่งแวดล้อม"}
    for field in ("name", "what", "effect"):
        values = [getattr(item, field) for item in TECHNOLOGIES]
        assert len(values) == len(set(values)), field


def test_no_two_mutation_uses_or_evolution_examples_collide():
    for table, fields in ((MUTATION_USES, ("name", "how", "need")),
                          (EXAMPLES, ("case", "account"))):
        assert len(table) >= 6
        for field in fields:
            values = [getattr(item, field) for item in table]
            assert len(values) == len(set(values)), field


def test_the_model_reading_answers_come_from_the_model_table():
    """``ม.3/1`` says ``โดยใช้แบบจำลอง``; the item hands one over to be read."""
    wanted = {item.description: item.reading for item in MODELS}
    seen = set()
    for seed in range(600):
        question = generate("cell.gene_dna_fluency", random.Random(seed))
        stem = _text(question.stem)
        description = next(key for key in wanted if key in stem)
        seen.add(description)
        assert _answer(question) == wanted[description], stem
    assert seen == set(wanted)


def test_every_wondering_has_its_own_question():
    questions = [item.question for item in WONDERINGS]
    assert len(questions) == len(set(questions)) >= 6


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcome, _, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (outcome, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    rows = _outcomes()
    for key, (outcome, _, _) in NEW_KEYS.items():
        assert rows[outcome]["coverage_state"] == "complete", outcome
        assert key in rows[outcome]["current_set_keys"].split("; "), key


def test_wave_b_leaves_no_incomplete_indicator_in_wo_one_three():
    """The closing condition: every one of the 24 ``ว 1.3`` indicators covered."""
    rows = [row for code, row in _outcomes().items()
            if row["standard_or_group"] == "ว 1.3"]
    assert len(rows) == 24
    incomplete = [row["outcome_code"] for row in rows
                  if row["coverage_state"] != "complete"]
    assert not incomplete, incomplete
