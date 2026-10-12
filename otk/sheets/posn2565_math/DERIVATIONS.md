# posn2565_math — transcription and verified answers

The text layer of `posn1-65-math.pdf` reads its **Thai prose** correctly — unlike
the 2567 sheet — but flattens every display equation: `2^a = 3^b = 216^c` comes
out as `2a = 3b = 216c`, and `a + 3/b = 3` as `a + 3 b = 3`. Superscripts and
fraction bars are simply gone, so a stem taken from `extract/itemNN.txt` will be
subtly *wrong* rather than obviously garbled. **Transcribe from the page renders.**

Only pages 1 and 6 carry artwork, so `extract/pages/` holds just those two.
Render the rest yourself:

```python
import fitz
doc = fitz.open("sheet_database/สอวน_math/posn1-65-math.pdf")   # 7 pages
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=150).save(f"p{i:02d}.png")
```

Every answer below was derived twice by different routes and the two agreed.
`ANSWER` in a solver module must be copied from here, never re-guessed. Where a
question is already digested, the module is the authority and this file is the
provenance.

Status: **q01–q20 digested** (solver + independent check + generator).
q21–q30 are not yet transcribed.

| # | Question (abridged) | Answer | Both routes |
|---|---|---|---|
| 1 | `2^a = 3^b = 216^c`; find `ab/(bc+ca)` | **3** = `ln N / ln(b₁b₂)` | divide through by `abc`, take logs · read a, b, c off two unrelated values of the common power and measure |
| 2 | `√a = √(8+4√3)/(√2+√(2+√3))` | **4/3** = `2k/3` | both radicals denest, `(√3+1)` cancels · evaluate the nested radicals numerically and square |
| 3 | two equations in four unknowns; value of `5a−4b+3c−2d` | **13** | the target row is `(1/5)r₁ + (6/5)r₂`, so the value is forced · row-reduce, sweep the free variables, check the target is constant |
| 4 | `a+3/b=3`, `b+2/c=2`, `c+1/a=1`; find `a+2b+3c` | **2** (`a=−3, b=1/2, c=4/3`) | eliminate round the cycle to a quadratic in `a` · sweep the first equation's residual, bisect, verify each root exactly |
| 5 | `P(x²)+4x = P(x)+4x⁴`, `deg P = 2`; find `P(4)−P(0)` | **80** = `k(m²+m)` | match coefficients: `α = β = k`, `γ` free · fit α and β from two sample points, then verify at five more |
| 6 | 110 sweets 4:7, eat 10 sweets and some chocolate → 1:6 | **30** | 40:70 → 60 sweets forces 10 chocolates left · try every number he could have eaten |
| 7 | ordered `(a,b,c)` positive with `ab+bc+ca = 11` | **9** | sorted triples `(1,1,5)` and `(1,2,3)` with multiplicities 3 and 6 · flat triple loop |
| 8 | two dice, `P(at least one prime face)` | **3/4** | `1 − ((f−p)/f)^n`, and **1 is not prime** · enumerate every throw |
| 9 | `p: ∀x∃y, x²−y = y²−x`; `q: ∃x, 2x²+x+2 = 0`; `p, q, p→q` | **(T, F, F)** | `y = x` witnesses p; q's discriminant is −15 · search for a witness y numerically, scan for a sign change in q |
| 10 | cylinder `H = 3R`, marble `r = R/2`; water fraction | **17/18** = `1 − 4/(3m³k)` | the marble displaces its own volume · build both volumes numerically and divide |
| 11 | quadrilateral cut by `EF, EG, EH` with `DF:FA = 1:2`; `[ECH]` | **14** | peel `[ADE], [ABE], [BCE]` = 15, 18, 21 off the three given areas · shoelace a real quadrilateral, measure the area map and invert it |
| 12 | `D` the midpoint of `AB`, `∠ADC = 45°`, `∠BCD = 15°`; `∠ACD` | **30°** | `AD = DB` + sine rule ⇒ `tan x = k sinδ/(1 − k cosδ)` · build the triangle and slide until `DA = DB` |
| 13 | tetrahedron, `AB=AC=AD=1`, apex angles 60/90/120; `OA` | **1/2** | `OA ⊥ base`, so `OA = 3V/[BCD]` · place the three edges in coordinates and drop a perpendicular |
| 14 | three circles on a line, radii 4, 1, x | **4/9** | `1/√x = 1/√R₁ + 1/√R₂` · rest the circles on a line and bisect the third radius |
| 15 | `AB=8, AC=12, AD=18`, `∠BAC = ∠CAD = 30°`; `∠BCD` | **150°** = `180° − θ` | `AB·AD = AC²` ⇒ `△ABC ∼ △ACD` · build the quadrilateral and measure the angle |
| 16 | sum of solutions of `(x²−x−1)^(2x²−11x+15) = 1` | **15/2** | three cases: exponent 0 (5/2, 3), base 1 (2, −1), base −1 with even exponent (1 only) · gather roots by bisection, then evaluate the original power |
| 17 | quartic with remainder `k²` at `x−k`, `k = 1,2,3`; `f(−1) − 4f(0)` | **25** | `f = x² + (x−1)(x−2)(x−3)(x−r)`; the multiplier 4 = `P(−1)/P(0)` cancels r · build f at four unrelated r and check they agree |
| 18 | `4a² + b + c + 4 = 0` with `a = 11x+55`, `b = 440`, `c = 88x` | **−448** = `−8(T+1)` | the quadratic is `(22x+112)²`, a perfect square by design · sum the series term by term and solve what comes out |
| 19 | `x³ − y³ + 9x² + 12y² + 34x − 55y + 140 = 0`; `y − x` | **7** = `p + q` | it is `(x+3)³+7(x+3) = (y−4)³+7(y−4)` and `t³+7t` is injective · solve for y at six different x and subtract |
| 20 | five sorted digits: unique mode, mean = median < mode, min an odd prime | **3 5 6 8 8** | walk the 2002 non-decreasing tuples · sweep all 10⁵ ordered strings and sort each |
| 21 | `a = 1 + 1/a`, `b² = 3 − 1/b²`, `c³ = 2 − 1/c³` (b > 0); `a³ + b³ + c⁴ − 1/a³ + 1/b³ + 1/c⁴` | **6 + 2√5** ≈ 10.4721 | each equation gives one symmetric sum: `a − 1/a = 1`, `b + 1/b = √5`, `c = 1` · find every real root of the three printed polynomials by bisection and evaluate on each |
| 22 | 2 tennis + 2 ping-pong balls in boxes 5–8 on shelves 1–4, three adjacency rules, white ball in box 7; all (a, b) | **(8, 1) and (8, 4)** | enumerate the 4! box orders and the choice of orange box · place box 8 from rule (ค) first (it can have at most one neighbour), then fill and scan the rack |
| 23 | right triangle, semicircle inscribed with diameter DE on AB, DG ⊥ AC = 6, EF ⊥ BC = 12; shaded area at C | **900 − 225π** ≈ 193.1417 | CPOQ is a square of side r, so the area is r²(1 − π/4) with r = p + q + √(2pq) · find the legs by bisection, then [ABC] − ½πr² − two corner regions (triangle minus sector) |
| 24 | square ABCD, E, F midpoints of BC, CD, G = AE ∩ BF; sin(∠ADG/2)cos(∠AED/2) | **2/5** | AE ⊥ BF always, ∠ADG = ∠AED always, cos θ = 3/5 so the product is (sin θ)/2 · lay out coordinates, intersect the lines, measure both angles with atan2 |
| 25 | m ≥ n positive integers, 1/m + 1/n = 2/33; max m − n | **544** = (33²−1)/2 | m = 33n/(2n−33): drive the denominator to 1, at n = 17, m = 561 · sweep m instead and recover n as an exact rational, keeping it only when its numerator is 1 |
| 26 | x√y + y√x = √2, x√x + y√y = 13√2; x + y | **7** | u = √x, v = √y: uv(u+v) = √2 and s³ − 3·√2 = 13√2 give s = 2√2, uv = 1/2, x + y = s² − 2uv · solve the printed system for (x, y) by two-dimensional bisection and add |
| 27 | a = 1000¹⁰/(10¹⁰ + 11); ⌊a⌋ mod 1000 | **120** = c² − 1 | x³/(x+c) = x² − cx + c² − c³/(x+c) with 0 < c³/(x+c) < 1 · build both integers and let big-int floor division do it |
| 28 | x, y **rational**, x² + 8xy − 11y² − 16x + 8y + 16 = 0; max x + y | **4** | the x-discriminant is 12(3y−4)², and 12 is not a square, so 3y = 4 · sweep rational y with small denominators, keep the points that really are rational |
| 29 | digit coefficients, P(1) = 3, P(3) = 33; the polynomial | **x³ + 2x** = (1,0,2,0) | three coefficient shapes sum to 3; only 2·3 + 27 works · search top-down by power vs. bottom-up by residue mod 3 |
| 30 | permutations of 1…10 with x₁ − x₂ + … − x₁₀ = 25 | **14400** | A = 40, B = 15, and {1,2,3,4,5} is the only 5-subset summing to 15, so 5!·5! · enumerate all permutations for n ≤ 8, the C(10,5) position sets for n = 10 |

## Notes for whoever continues

* **q1 is only rational when the third base is a power of the product of the
  other two.** `216 = 6³` is what makes the answer `3`; for `2^p 3^q` with
  `p ≠ q` the value is a genuine combination of logarithms and the sheet's
  "เท่ากับเท่าใด" has no exact answer, so `solve` returns `None` there.
* **q3's answer depends on the target row being in the span of the two given
  rows.** Most rows are not, and then *every* real number is possible — `solve`
  returns `None` rather than a number, and the generator only draws rows that
  are combinations.
* **q4 becomes a genuine quadratic when `r ≠ 1`** and can then have two
  solutions with different values of `a + 2b + 3c`; `solve` returns `None`
  unless all of them agree.
* **q5 never determines `γ`** — that is why the question asks for a difference.
  A generated version must keep asking for `P(m) − P(0)`, not for `P(m)`.
* **q7 asks for สามสิ่งอันดับ — ordered triples.** Counting the two sorted
  solutions gives 2, not 9; the multiplicities are the question.
* **q8's answer turns on 1 not being prime.** Counting it gives 8/9, which the
  generator offers as its first distractor.
* **q9's p needs no algebra at all**: `x² − y = y² − x` is `x² + x = y² + y`, and
  the y you need is x itself. Reaching for a discriminant here is how the item
  gets read as false, which would flip the implication too.
* **q11 never needs E's position** — it is not given, and the chain of four
  regions peels `[ADE]`, `[ABE]`, `[BCE]` off in turn without it.
* **q12 barely generalises.** Over every integer pair (δ, γ) the only answers in
  whole degrees are the sheet's own and the degenerate δ = 90° family (where
  CD̅ is the perpendicular bisector and x = γ). Its generator therefore varies
  *which angle is asked for* — `ask` — rather than the constants. Its `BC > AB`
  condition is load-bearing too: drop it and δ = 60°, γ = 30° looks solvable but
  describes a different figure.
* **q13 is rational only at {60°, 90°, 120°}**, where `OA` is exactly half the
  edge. The solver returns a float (the value is irrational elsewhere), so
  `sheet.json` records `0.5` and a test ties the generator's exact half-edge back
  to it.
* **q14's "smallest circle between the other two" comes from the picture**, not
  from the text — the generated prompt says it out loud, and the crop is shown
  only when the radii are still 4 and 1.
* **q20's answer was 3 5 6 8 8, not what I first guessed.** Both routes agreed
  on it immediately; the hand-written `ANSWER` was wrong. Run the solver first,
  always.
* **q16's third case is the whole item**: base −1 needs an *even integer*
  exponent, and only one of that case's two roots qualifies. Dropping the case,
  or keeping both roots, are the two distractors.
* **q17's multiplier is not arbitrary.** `f(−1) − m·f(0)` is only determined for
  `m = P(−1)/P(0)` — 4 for the nodes 1, 2, 3 — because the quartic has a free
  root. Node triples where that is not a whole number are excluded from the pool.
* **q18's constants are engineered for a zero discriminant.** The coefficient of
  `c` has to be `8(n+1)` or there is no double root, and `check` asserts the
  discriminant really is zero rather than quietly taking one root.
* **q6's constants rarely come out whole.** `solve` returns `None` unless every
  count in the story is a non-negative integer, and the generator draws from a
  pool of the ones that do.
* **q21 never solves for a, b or c.** Each equation is handed over as a symmetric
  combination, and the requested expression is built only from those. Watch the
  signs: the question is `(a³ − 1/a³) + (b³ + 1/b³) + (c⁴ + 1/c⁴)`, a difference
  on the first bracket only. `b > 0` is what picks `+√5` over `−√5`.
* **q21's c-part survives generalisation.** `c³ + 1/c³ = t` has roots `u` and
  `1/u`, and `c⁴ + 1/c⁴` treats them alike, so the value is pinned even when
  `t > 2` and `c ≠ 1` — `check` verifies that by evaluating on every real root.
* **q22 is decided by rule (ค) alone, before any ball is placed.** Every shelf
  next to box 8 must hold a box that is neither 5 nor 7, and only box 6 is left,
  so box 8 has at most one neighbour and must sit on shelf 1 or 4. Four layouts
  survive; the ball rules cut them to two, and the orange ball is in box 8 both
  times.
* **q23's shaded region is a square minus a quarter disk, and nothing more.**
  Putting the right angle at the origin makes the centre (r, r) and the tangency
  points (r, 0) and (0, r) — the rest is `r = p + q + √(2pq)`, from
  `(r−p)² + (r−q)² = r²`. Its attached crop has 6 and 12 written on it, so the
  generator shows the figure only when it draws those.
* **q24 is two hidden invariants, not one.** `AE ⊥ BF` is the familiar one; the
  one the question needs is `∠ADG = ∠AED`, which holds for *every* cut ratio, not
  just the midpoints. `check` measures both angles and refuses to answer if they
  differ, so the invariant is tested rather than assumed.
* **q24 barely generalises either.** The midpoints are the only ratio with
  denominator ≤ 15 for which `(1+m²)(1+(1−m)²)` is a rational square, so the
  generator varies *which product is asked* — sin·cos = 2/5, sin·sin = 1/5,
  cos·cos = 4/5, sin/cos = 1/2. Those four share values, so the distractor list
  needs padding beyond the sibling products.
* **q25's parity is the whole trick.** `2n − k` is odd when k is odd, so it can
  reach 1; for even k it can only reach 2, and the extreme pair moves. `solve`
  gets both from the divisibility test instead of splitting the cases.
* **q26 is rational only when `b + 3a = 2t³`.** Then `s = u + v = t√2`,
  `uv = a/t` and `x + y = 2t² − 2a/t`; the sheet is t = 2, a = 1. Anything else
  leaves `s` an awkward sixth root, which is why the pool is built from t.
* **q27's numerator is a cube.** `1000¹⁰ = (10¹⁰)³`, not `10¹⁰`; the whole answer
  is the `c² − 1` that the cubic division leaves behind, and `x² − cx` vanishes
  mod 1000 only because x is a power of ten. The generator keeps the sheet's own
  disguise and prints `1000^k` over `10^k + c`.
* **q28 lives or dies on the word ตรรกยะ.** Over the reals the curve is a
  hyperbola and `x + y` is unbounded — there is no maximum to find. The
  discriminant being `(non-square)·(linear)²` is what collapses the curve to a
  single rational point, so `solve` returns None when the leading coefficient
  *is* a square (infinitely many points, no maximum) or when the trinomial is not
  a perfect square. The generator builds its constants backwards from `k(py−q)²`.
* **q29's "ผมรู้แล้ว" is the constraint.** Euler can only say that because the
  polynomial is unique; a generated version must check uniqueness, not just find
  one candidate. `solve` returns None whenever two survive — which happens as
  soon as `P(1) ≥ b`, since the digit bound of 9 stops being redundant there.
  Leading zeros have to be trimmed on both routes or `x³+2x` and `0x⁴+x³+2x`
  count as different answers.
* **q30's target sits on the boundary.** 25 forces the even positions to sum to
  15, and `1+2+3+4+5` is the minimum possible, so exactly one subset qualifies.
  At 27 there is nothing at all. That is why the count is as clean as 5!·5!.
