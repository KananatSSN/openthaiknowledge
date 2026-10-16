# posn2561_math — transcription and verified answers

`posn1-61-math.pdf` is 8 pages. **Page 1 is the cover and คำชี้แจง** — the
questions start on page 2 — but `split_items` handled the numbered-instructions
trap correctly here: `extract/item01.txt` really is question 1. As on every sheet
in this folder, the display maths is vector art, so `itemNN.txt` is unusable for
the mathematics (`item02.txt` shows `7m` for `7^m`, with the exponents dumped
after it). Transcribe from the page renders:

```python
import fitz
doc = fitz.open("openthaiknowledge-bank/สอวน_math/posn1-61-math.pdf")   # 8 pages
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=200).save(f"p{i:02d}.png")
```

The Thai *prose* on this sheet does extract cleanly, so `itemNN.txt` is a fine
cross-check on wording — just never on a formula, an exponent or a constant
inside one.

Two conventions are printed on the cover and are worth knowing before deriving
anything: **22/7 may be used for π**, and **a fractional answer must be given in
lowest terms**.

Every answer below was derived twice by different routes and the two agreed.
`ANSWER` in a solver module must be copied from here, never re-guessed.

Status: **all 30 digested** — solver + independent `check` + generator.
`verify` reports `30/30 green, 186 variant runs, 0 without an independent check`.

| # | Question (abridged) | Answer | Both routes |
|---|---|---|---|
| 1 | five boys, each always truthful or always lying, two rounds of statements; how many homework problems | **7** | round two alone forces ก✗ ข✗ ค✗ ง✓ จ✓, then round one gives N = 7 · fix N first and read each boy's label off his own claim |
| 2 | units digit of `7^m` where m is the digit count of `25²⁵·8²⁰` | **9** | the inner number is `1024·10⁵⁰`, so m = 54, and 54 ≡ 2 (mod 4) · build the integer, `len(str(...))`, `pow(base, m, 10)` |
| 3 | smallest number with 60 divisors and exactly 3 distinct primes | **10800** | `(4+1)(3+1)(2+1)`, larger exponents on smaller primes · try every prime-to-exponent permutation, and scan the integers below the winner |
| 4 | gcd 30, lcm 5400; min `m + n` | **870** | coprime split `9·20 = 180`, so `30·29` · walk the divisors of the lcm and test gcd and lcm directly |
| 5 | how many n in 1…200 have `n² + 9` divisible by 5 | **80** | `n ≡ 1, 4 (mod 5)` — 2 residues in 5, and 200 is whole cycles · test every n against the printed condition |
| 6 | least n > 350 that is a sum of 3, of 4 and of 5 consecutive positive integers | **390** | 15 \| n and n ≡ 2 (mod 4) · build the runs and add them up |
| 7 | `N = 7373…73` (2560 digits) mod 37 | **10** | `10³ ≡ 1 (mod 37)`, the terms cycle 1, 26, 10 summing to 0, leaving 27; and 73 ≡ −1 · build the 2560-digit integer and take the remainder |
| 8 | subsets of {1,…,22} with min + max = 23 | **1398101** | 11 pairs, `2^(gap−1)` free middles each, `(4¹¹−1)/3` · enumerate the pairs, and every subset outright for small universes |
| 9 | island coastline split equally, 5 and 10 million per km, whole km | **195** | the cut AE is not coastline, so each side is half the perimeter ≈ 12.854 → 13 km · slide E along CD until the two coasts match |
| 10 | `3x²+3y² = 7`, `x³+y³ = 3`; max x + y | **2** | `s³ − 7s + 6 = 0` with the reality bound `s² ≤ 14/3` killing s = −3 · sweep x on the circle and bisect the cubic's residual |
| 11 | `y² + 2x²y² = 96x² + 864` over ℤ; find `x² + y²` | **89** | `(2x²+1) \| 1632`, four odd divisors, only d = 51 leaves both squares · sweep a grid of (x, y) against the printed equation |
| 12 | `Σxᵢ² = (Σxᵢ)² + 2561` with `\|xᵢ\| < 1`; least n | **2562** | f is linear in each xᵢ, so sup f is n (n even) or n − 1 (n odd) · search the ±u family for an explicit witness |
| 13 | cube root of `3⁷(9 − 5⁵) + 5¹⁰(81 − 5⁵)` | **−3098** | it is `(3³ − 5⁵)³` in disguise · build the four-term integer and bisect for an exact integer cube root |
| 14 | `Σ p(n)`, n = 1…99, p = product of nonzero digits | **2115** | zero-pad: the sum factorises as `46² − 1` · multiply out the digits of every n |
| 15 | `P(x−1) + P(x+1) = x³`; sum of coefficients | **−1** | match coefficients: a = ½, c = −3/2, so P(1) = −1 · carry P(0), P(1) up the recurrence and kill the 4th finite difference |
| 16 | remainders 5 at x = 2 and −7 at x = −3; remainder mod `x² + x − 6` | **(12/5, 1/5)** | the line through (2, 5) and (−3, −7) · interpolate two different cubics with those values and long-divide each |
| 17 | square straddling the incircle's tangent point on a leg of a 3-4-5 | **64/25** | `(s−r)² + (s/2)² = r²` gives s = 8r/5, so the area is 64r²/25 · build the figure with r = area/semiperimeter and bisect for s |
| 18 | shaded share of a square, `AC : CB = 2 : 1` | **13/30** | `(m² + S²)/(2S(m+S))` with S = m + k · Cramer for the crossing point, shoelace all four regions, check they total S² |
| 19 | base 20, altitude 8, the two halves similar but not congruent | **20 + 12√5** | pq = h², so the perimeter is `base + √(base(base+2h))` · bisect for the foot and measure the three sides |
| 20 | tangents from A to a circle of radius 5, `CE ⊥ BD`, `CE = 4` | **10** | the two tangent lines meet at `x = −r`, giving `r(r+√(r²−h²))/h` · construct both tangents as perpendiculars and measure, checking AB = AC |
| 21 | closed cylinder with V = S, still V = S after +50% height and −25% radius | **64π** | `rh = 2r + 2h` twice gives r/h = 1, then r = h = 4 · bisect r along the one-parameter V = S family |
| 22 | parallelogram cut by one line; PR = a, PQ = b, find AR | **√(a(a+b))** | the three parameters along the transversal eliminate to `AR² = PR(PR + PQ)` · measure AR in two unrelated parallelograms and require agreement |
| 23 | acute ΔABC, `∠BAO = 15°`, `∠ACO = 45°`; `CD : BD` | **2** | `sin 2γ / sin 2β` · place A, B, C from the central angles, intersect AO with BC, measure |
| 24 | two secants from P, `AB = 8`, `CD = 5`, `BP = 6`, `∠APD = 60°`; `r²` | **43** | power 84 fixes PC = 7, then the chord midpoints put O at (10, 3√3) · fit the circle through A, B, C and slide C until D lands on it |
| 25 | Markov rain chain, dry on Tuesday; dry on both Thursday and Friday | **1/3** | `f₂ = 2/3` from `f_n = π + (1−π)(p−q)ⁿ`, times p · enumerate all eight weather paths |
| 26 | 8 identical balls on the four sides of a square table, ≥ 1 each | **10** | Burnside over the four rotations: (35 + 1 + 3 + 1)/4 · list every composition and fold rotations together |
| 27 | how many n ≤ 10000 have digit set exactly {0, 4, 7} | **28** | 4 of three digits, 24 of four by inclusion–exclusion · test `set(str(n))` for every n |
| 28 | frog at ±1 per jump; P(at 2018 after 2561 jumps) | **0** | 2561 is odd and 2018 even — parity settles it · sum `C(n,u)` over every u whose landing point matches |
| 29 | die game, thresholds 2 then 3 then 4, three rounds | **8/9** | `2/3 + (1/3)(1/2 + 1/6)` · enumerate all 216 roll sequences |
| 30 | positive square divisors of `2³3⁵5⁷7²` | **48** | `⌊e/2⌋ + 1` per prime: 2·3·4·2 · list all 576 divisors and test each with `isqrt` |

## Notes for whoever continues

* **q1's second round is self-contained.** ก's own statement is what breaks it
  open: substituting ง's equation into it gives `Tก = ¬Tข ∧ Tข`, false whatever
  ข is. Nothing about the number enters until the labels are settled.
* **q2's inner number is a power of ten in disguise** — `5⁵⁰·2⁶⁰ = 2¹⁰·10⁵⁰` —
  so its digit count is 4 + 50 with no multiplication needed. `solve` deliberately
  takes the *risky* route (logarithms) so that `check`'s exact `len(str(...))`
  is testing something real.
* **q3 rewards the balanced split.** The four ways to write 60 as three factors
  give 245760, 23040, 12960 and 10800; the nearly-equal exponents (4, 3, 2) win,
  which is the opposite of the "make one exponent big" instinct. `check` tries
  every permutation of exponents against primes rather than sorting, so the
  "larger exponent on the smaller prime" step is verified.
* **q4 is the same item as 2562 q2** with different constants — coprimality, not
  balance, decides the split.
* **q5's squares mod 5 are only 0, 1 and 4**, which is why most shifts give no
  solutions at all; two of the six variants land on zero for exactly that reason.
* **q6's even run length is the constraint that bites.** An odd number of terms
  *forces* divisibility (3 terms ⟹ 3 | n); an even number *forbids* it (4 terms
  ⟹ n ≡ 2 mod 4, so 4 ∤ n). That is what stops the answer being a multiple of 60.
* **q7 never needs 2560 or 1280 as numbers** — only 1280 mod 3, because
  `10³ ≡ 1 (mod 37)` makes each period of three terms sum to 37 ≡ 0.
* **q8's singleton case was found by `check`.** The pair argument misses subsets
  with min = max, which qualify whenever the target is even. 23 is odd so the
  sheet's own answer was right either way — the brute-force sweep over small
  universes is what exposed it on a variant.
* **q9's cut is not coastline.** AE is inland, so "the two sides are equal" means
  each is exactly half the whole perimeter and no length has to be found at all.
  Round each side up separately, not the total. The crop on file
  (`extract/figures/item09.png`) is clipped — it loses the labels and the
  dimensions — so it is deliberately **not attached**.
* **q10 needed two corrections, both from the cross-check.** `solve` originally
  looked only for *rational* roots of the cubic, which is wrong whenever the
  largest admissible root is irrational; and `check` missed s = 2 entirely
  because the curves **touch** there (x = y = 1) instead of crossing, so no sign
  change occurs. `solve` now solves the depressed cubic in closed form (Cardano /
  trigonometric) and `check` refines local minima as well as sign changes.
* **A 200 000-step numeric scan inside `solve` makes a generator pool unusable.**
  q10's first version took minutes to build a 2 100-entry pool. The closed form
  is not just tidier — it is what makes the type generatable at all.
* **q11's divisor list is the whole item.** Writing `d = 2x² + 1` turns the
  equation into `d(2y² − 96) = 1632`, and the four odd divisors of 1632 are the
  entire search space. Building a generator pool the other way round — sweeping
  (a, b, c) and asking the solver — succeeds in well under 1% of tries, so
  `posn2561.py` picks (a, x, y) first, solves for c, and *then* vets with the
  solver.
* **q12 turns on f being linear in each variable separately.** ∂²/∂xᵢ² of
  `Σxⱼ² − (Σxⱼ)²` is `2 − 2 = 0`, so the maximum over the closed cube is at a
  corner, where every xᵢ = ±1 and f = n − k² with k ≡ n (mod 2). An odd n
  therefore throws one unit away, which is the only reason the rule is
  "target + 1 if odd, target + 2 if even" rather than just "target + 1".
* **q13's printed grouping splits the binomial across the wrong pairs.**
  `3⁷·9` belongs with `3⁷·5⁵`, and `5¹⁰·81` with `5¹⁰·5⁵`; regrouped it is
  `u³ − 3u²v + 3uv² − v³` with u = 27 and v = 3125.
* **q14's zero digit and zero pad do the same thing** — both contribute a factor
  of 1 — which is why padding every number to the same width changes nothing and
  the sum factorises to `46^d`.
* **q17 has a coincidence that only the figure shows.** At 3-4-5 the square's
  corner B lands exactly on the hypotenuse; in general it is strictly inside
  (`0.8a + 0.6b ≤ √(a²+b²)` by Cauchy–Schwarz, equality only at a : b = 4 : 3).
  So the crop ships only on draws similar to 3-4-5 and the generator passes
  `figure=None` otherwise. The area itself depends on nothing but r.
* **q19's third bullet is the question.** Two right triangles sharing the leg h
  are similar either leg-for-leg (p = q) or crosswise (pq = h²); "ไม่แบ่งครึ่ง
  มุมยอด" is what rules the first out. Everything else follows without ever
  naming p and q.
* **q22 is stated in letters, so its published answer is a formula**,
  `AR = √(a(a+b))`. `PARAMS` instantiates it at a = 4, b = 5, where the answer is
  the whole number 6; `check` measures AR in two unrelated parallelograms and
  refuses to answer unless they agree, which is what proves the result really is
  shape-independent.
* **q23's answer is exact only at a few angles.** `sin 2γ / sin 2β` is rational
  for essentially nothing but β = γ and the sheet's own (15°, 45°), so the
  generator draws β and γ from {15°, 30°, 45°, 60°} — the angles whose doubles
  have sine 1/2, √3/2 or 1 — and prints the exact surd from a four-entry table.
* **q24's figure is filed under q23.** The drawing starts 5 points *above* the
  "24." label, so `figures()` assigns it to the previous question; and because
  the caller keys figures by item number in a dict, it also silently displaces
  q23's own circumcircle diagram. Both crops for this sheet were therefore placed
  by hand from `figure_regions(pdf, 7)`, which does return all three page-7
  regions in reading order.
* **q26 and q30 are ambiguous as printed, in opposite ways.** q26 says the sides
  are "เหมือนกันทุกด้าน" without saying whether the table may be flipped as well
  as turned — rotations alone give 10, the full dihedral group gives 8. q30 asks
  for "ตัวหารบวกทั้งหมด … ที่เป็นจำนวนกำลังสอง", which is a request to list them,
  and only reads as a single number if you take it as a count. Both generated
  questions state the reading they mean out loud.
* **q28 is a parity question wearing a binomial costume.** 2561 is odd and 2018
  is even, so the answer is 0 and nothing else is needed. `check` deliberately
  never tests the parity: it scans every possible number of right-jumps and lets
  the empty sum produce the zero.
