"""Wave F slice 83 — how bright stars are, their colours, their distances, and their lives.

Four ``additional_outcome`` indicators, each filed whole:

* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/6`` — luminosity and magnitude;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/7`` — colour, surface temperature
  and spectrum;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/8`` — distance by parallax;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/9`` — evolution by starting mass,
  read on the Hertzsprung-Russell diagram.

The core ม.6 sets hold ``astro.star_luminosity``, ``astro.star_spectrum`` and
``astro.stellar_evolution``, so these keys are distinct. Every rule used is
stated in the stem: five magnitudes is 100 times, L ∝ R²T⁴, Wien's
λmax = 2,900,000 / T (nm, K), d = 1 / p, L ∝ M⁴, and a main-sequence life of
10,000 million years × M / L. Only values that give exact answers are drawn.
"""

from __future__ import annotations

SUBJECT = "ดาราศาสตร์"
UPPER_SIX = {"th": "ม.6"}
NAMES = ("ดาว ก", "ดาว ข", "ดาว ค", "ดาว ง")

# ══ 3 ม.6/6 — ความส่องสว่างและโชติมาตร ═══════════════════════════════════════════════


# ══ 3 ม.6/7 — สี อุณหภูมิ และสเปกตรัม ═══════════════════════════════════════════════


# ══ 3 ม.6/8 — แพรัลแลกซ์ ══════════════════════════════════════════════════════════


# ══ 3 ม.6/9 — วิวัฒนาการของดาวฤกษ์และแผนภาพ H-R ═════════════════════════════════════


