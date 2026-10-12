"""A seed must give the same question in every Python process.

Python randomises string hashing per process, so a set of strings iterates in a
different order each run. Wrong answers collected in such a set and then turned
into a tuple made the same seed produce differently ordered options in different
processes. These types did exactly that; they now collect into insertion-ordered
dicts. Each process here gets a different ``PYTHONHASHSEED``.
"""

from __future__ import annotations

import os
import subprocess
import sys

FIXED = (
    "biology.animal_digestion_application", "biology.animal_nervous_application",
    "biology.behavior_evolution_fluency", "biology.heart_flow_application",
    "biology.hydra_planaria_foundation", "biology.kidney_structure_fluency",
    "biology.leaf_structure_fluency", "biology.mammal_lung_foundation",
    "biology.root_structure_foundation", "biology.succession_application",
    "biology.taxonomy_foundation", "chem.empirical_formula_foundation",
    "geo.fossil_foundation", "geo.geologic_history_fluency", "geo.petroleum_coal_fluency",
    "geo.water_amount_foundation", "geo.weather_forecast_foundation",
)

SCRIPT = """
import hashlib, sys
from random import Random
from otk.core import generate
h = hashlib.sha256()
for key in sys.argv[1:]:
    for seed in range(40):
        h.update(generate(key, Random(seed)).model_dump_json().encode())
print(h.hexdigest())
"""


def _digest(hash_seed: str) -> str:
    env = {**os.environ, "PYTHONHASHSEED": hash_seed}
    done = subprocess.run([sys.executable, "-c", SCRIPT, *FIXED], env=env,
                          capture_output=True, text=True, check=True)
    return done.stdout.strip()


def test_questions_do_not_depend_on_the_process_hash_seed():
    assert _digest("1") == _digest("2") == _digest("3")
