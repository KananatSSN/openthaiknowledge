# posn2562_math — transcription and verified answers

`posn1-62-math.pdf` is 6 pages. Its item boundaries extract cleanly, but — like
every sheet in this folder — **the display equations are vector art**, so
`extract/itemNN.txt` cannot be trusted for the mathematics. Transcribe from the
page renders:

```python
import fitz
doc = fitz.open("openthaiknowledge-bank/สอวน_math/posn1-62-math.pdf")   # 6 pages
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=150).save(f"p{i:02d}.png")
```

Only page 4 carries artwork, so `extract/pages/` holds just that one; the figure
crops on disk are `item20.png` and `item21.png`.

Every answer below was derived twice by different routes and the two agreed.
`ANSWER` in a solver module must be copied from here, never re-guessed.

Status: **all 30 digested** (solver + independent check + generator).

| # | Question (abridged) | Answer | Both routes |
|---|---|---|---|
| 1 | `a³ⁿ = 5`; find `(a^{4n}+a^{7n}+a^{−5n})/(a^{−2n}+a^{n})` | **751/30** | multiply above and below by t⁵ so every power becomes a power of t³ · compute in ℚ[t]/(t³−v) and check the t and t² parts vanish |
| 2 | gcd 20, lcm 50400; min `m + n` | **2020** | m = 20a, n = 20b coprime with ab = 2520: split the four prime powers · walk the divisors of the lcm and test gcd and lcm directly |
| 3 | `2x² − 10x + 7 + 4√(x²−5x+3) = 31`; sum of real roots | **5** | the radicand *is* the polynomial part: u + 2√u − 15 = 0 · sweep, bracket and bisect the printed expression |
| 4 | three daughters, product 48, the two **older** are twins; sum of ages | **11** | t²y = 48 with y < t leaves only (4, 4, 3) · enumerate ordered age triples and read the twin condition off the sentence |
| 5 | box in a sphere, 6 faces = 384, 12 edges = 112; find r | **10** | (2r)² = (a+b+c)² − 2(ab+bc+ca) = 784 − 384 · build real edge lengths that fit and measure the diagonal |
| 6 | right angle at C, CD ⊥ AB, AD = 2, BD = 3; find CD | **√6** ≈ 2.4495 | the altitude is the geometric mean of the two pieces · place the figure in coordinates, assert both defining properties, measure |
| 7 | 9 pens of pigs and ducks, all head counts distinct, 40 legs each; P(head count prime) | **4/9** | 2p + d = 20 makes the head count 20 − p, i.e. 11…19 · enumerate (pigs, ducks) pairs and tabulate |
| 8 | 5 runners, prizes 7000/5000/2500/1500/500, three statements; A+B+C prize total | **9000** | C's count fixes third, then A/D, then E/B: the order E, B, C, A, D · seat C first and fit the others around him clue by clue |
| 9 | 10 games, win 4 / loss 0 / draw 1; max combined total − min | **20** | each game adds 4 or 2, so the spread is g·|w+l−2d| · build every combined total from 0…g decided games |
| 10 | `x³ + mx² + nx + p`, p prime, f(1) = 4, f(−3) = 0; find mn | **−4** | eliminating n gives m = 3 − p/3, so 3 \| p and p = 3 · sweep (m, n, p) and divide the cubic by synthetic division |
| 11 | 555 and 670 leave the same prime remainder p mod m; m + p | **26** | m divides 115 = 5·23; only m = 23 leaves a prime (p = 3) · try every modulus and compare the two remainders directly |
| 12 | remainder of `((2^2562·3^2019)^2020)^2563` mod 10 | **6** | last digits have period 4 and 2020 ≡ 0 (mod 4), so 6·1 · hand the ten-digit exponent to three-argument `pow` |
| 13 | a² + b² = 425, gcd = 5; find lcm | **20** | x² + y² = 17 has only 1 + 16, so (5, 20) · sweep a and b over the printed equation and use the Euclidean algorithm |
| 14 | `(p(x))³ − x` divisible by `x³−13x²+44x−32`; find a − 7b − 2c | **3 − 4∛4** ≈ −3.3496 | p interpolates (1,1), (4,∛4), (8,2); solve the Vandermonde system in ℚ(∛2) · Lagrange-interpolate numerically, then long-divide the sextic by the cubic |
| 15 | chord of `y = 4x²+7x−1` bisected by the origin; its length | **5√2** ≈ 7.0711 | B = −A gives u² = −c/a and v = bu, so AB = 2\|u\|√(1+b²) · sweep u and bisect the reflection residual |
| 16 | `a²+12a+3 = 0`, `3b²+12b+1 = 0`, ab ≠ 1; find (ab+a+1)/b | **−9** = q − p | 1/b solves the first equation too, so Vieta gives both pieces · solve all four roots and evaluate every admissible pairing |
| 17 | two square-based boxes, S = 2V and S = 3V after scaling; first volume | **54** | the two conditions are linear in (s, h) and s cancels: h = 3/2, s = 6 · bisect on h until the second box's condition holds |
| 18 | cube inscribed in a cone, R = 1, H = 3; edge length | **(9√2 − 6)/7** ≈ 0.9611 | top corners sit at radius a/√2 and height a on `R(1 − z/H)` · grow the cube and measure how far its corners escape the cone |
| 19 | isosceles triangle, DE tangent to the incircle ∥ BC, DE = 20, BC = 52; find r | **2√65** ≈ 16.1245 | the gap between the parallels is 2r, and everything collapses to r = √(BC·DE)/2 · rebuild the triangle and cut the chord for real |
| 20 | two right triangles on AB, AB=4, BC=6, AD=8, L the midpoint of AD; area of BMN | **72/35** | the right angles make the whole figure rational: M=(16/7,24/7), N=(8/5,12/5) · locate M and N along AC and subtract the triangles ABM and ABN |
| 21 | square, E the midpoint of AD, ∠CEF = 90°, ∠BCF = α; find ∠DCE | **45° − α/2** | CE bisects ∠DCF, and only at the midpoint: (2e−1)(e−... ) → 2e³−5e²+6e−2 = 0 · build the square, find F, measure both angles with atan2 |
| 22 | ∠B = 2∠C and BC = 2AB; find ∠A + ∠C | **120°** | sin3γ = 2sinγ gives sinγ = ½, so it is a 30-60-90 triangle · build the triangle from the two sides and measure ∠C |
| 23 | 50 guests, a handshake cycle then every even guest to all larger; total | **626** | 50 + (47+45+…+1) = 50 + 24², i.e. n + (n/2−1)² · build the set of pairs and count it |
| 24 | 4×5 grid, choose 3 cells all in different rows and columns | **240** | C(4,3)·C(5,3)·3! — the factorial is the matching step · enumerate the cell subsets and test the condition |
| 25 | digits a,b,c with 20ab13c divisible by 792; find a+b+c | **12** | 792 = 8·9·11: c = 6, a+b ∈ {6,15}, a−b ∈ {5,−6} → a=0, b=6 · walk the multiples of 792 and match the template |
| 26 | r₁,r₂ roots of x²−17x−632 = p; largest root of (x−r₁)(x−r₂)+p+2 = 0 | **35** | p cancels exactly, leaving x²−17x−630 = 0 with 2809 = 53² · rebuild the second equation from real roots at several p |
| 27 | a₁ = 2019²⁵⁶², aₙ₊₁ = aₙ − f(aₙ); index of the first term < 2 | **35869** | removals are additive: T(3)=2, T(673)=12, so 2562·14 + 1 · walk the sequence as a multiset of primes |
| 28 | frog on 7 stairs with jumps 1,2,3; P(never jumps 3) | **21/44** | Fibonacci over tribonacci · enumerate the climbs themselves |
| 29 | 2562 bulbs and 2562 students toggling multiples; how many end up on | **50** | a bulb is flipped d(n) times, odd exactly for squares, so ⌊√2562⌋ · flip the switches for real and count |
| 30 | Som tells the truth only on her birthday; three utterances on three consecutive days | **20** | four cases, and only B = d+2 with 19 ∉ S₂ survives · lay out the month's schedule and test every utterance against it |

## Notes for whoever continues

* **q1's answer is rational only because every exponent leaves the same
  remainder mod 3.** `4, 7, −5, −2, 1` are all ≡ 1, so one factor of t⁵ clears
  the negatives *and* turns every surviving power into a power of t³ = 5. Mix the
  residues and the value is a genuine element of ℚ(5^{1/3}); `solve` returns None
  there, and `check` discovers it by finding a non-zero t or t² component.
* **q2 turns on coprimality, not on balance.** The instinct to make the two
  cofactors as equal as possible wants 2520 ≈ 50·50, which no coprime split
  reaches; the real candidates are the 16 unitary divisors, and 45·56 wins.
* **q3's radicand is the polynomial part in disguise**, and squaring the equation
  drags in the `√u = −5` branch as extraneous roots. Note also that the answer is
  just `−s`, the root sum of `x² + sx + (t−u)`, whenever that quadratic has two
  real roots — u itself never has to be rational.
* **q3's `check` needed two extras beyond sign changes.** A root can sit exactly
  where the domain ends (u = 0, no sign change at all — the `target = 1` variant)
  and a root can be a tangential touch. The sweep now also bisects
  defined/undefined boundaries and refines local minima of |lhs|.
* **q4 needs "2 คนโต".** Without the twins being the *older* pair, (2, 2, 12)
  fits just as well and the answer would be 16.
* **q5's edge lengths are not determined** — many boxes fit both printed totals.
  They all share a diagonal, which is exactly why the question can ask for r and
  why `check` builds several different boxes and demands they agree.
* **q7's "all different" is a determination, not a restriction.** There are
  exactly nine possible head counts (11…19) and exactly nine pens, so the pens
  are forced to be precisely those. `solve` returns None when the two counts do
  not match, which is what makes the generator's pool honest.
* **q8's order is forced, and that is the point.** Every clue is needed: drop
  A's "at least two ahead" and two orders survive. `solve` and `check` both
  return None unless exactly one placement comes out.
* **q9 never needs to know who won.** Each game contributes `w + l` or `2d` to
  the *combined* score, so the ten-game score space collapses to a single count.
  Note the answer is `g·|w + l − 2d|` with the absolute value — a scheme where
  draws pay more is still a valid question.
* **q10's primality is load-bearing.** `12m = 36 − 4p` puts m in ℤ only when
  3 divides p, and 3 is the only positive prime that does. Without the primality
  the two conditions leave a one-parameter family and there is no single mn.
* **q11's primality picks the divisor.** m must divide 670 − 555 = 115, which
  leaves four candidates; only m = 23 gives a prime remainder. `check`
  deliberately ignores the divisibility argument and tries every modulus.
* **q12 uses none of its big numbers.** 2562, 2019 and 2563 are decoration: the
  2020 in the middle is divisible by 4, which is the period of both last-digit
  cycles, so both exponents land on the end of their cycle.
* **q13's gcd selects the representation.** 425 is `5² + 20²` *and* `13² + 16²`;
  only the first has gcd 5. Reducing by the gcd first is what makes the search
  small enough to be obviously complete.
* **q14's answer really is irrational**, and this was checked against the page at
  420 dpi before it was recorded. The t² parts of `a − 7b − 2c` contribute
  `−1/12 − 21/4 + 4/3 = −4`; the combination that *does* cancel them is
  `a + b + c`, which is just p(1) = 1. Reading `(p(x))³` as threefold composition
  instead makes the question ambiguous — the 3-cycle 1→4→8 gives −27 and its
  reverse gives 8 — which is the strongest argument that the cube of the value is
  meant. This sheet is comfortable with surds: q6, q15, q18 and q19 all have them.
* **q15's `check` was caught by the exact-hit trap again.** The sweep lands
  precisely on u = ±1/2, so `prev * cur < 0` is never true and the roots vanish.
  The same bug the 2565 sheet paid for; an explicit `cur == 0.0` branch fixes it.
* **q16's two equations are one equation.** The second is the first reversed, so
  1/b is a root of the first, and `ab ≠ 1` is what makes a and 1/b the two
  *distinct* roots. The answer is `q − p` and the roots are never computed.
* **q17's s cancels.** Both printed conditions are linear in (s, h) once divided
  through by s, so subtracting them gives h directly. The individual box is then
  determined, unlike q5 where it never is.
* **q18 lives on the 1/√2.** The top corners are at radius a/√2, not a — using
  the edge midpoints instead gives 3/4 and looks just as plausible.
* **q19 is the geometric mean again**, like q6 on page 1 but reached along a
  completely different road: `r = √(BC·DE)/2`, with the triangle's height
  dropping out of the algebra entirely.
* **q20 is rational all the way through.** Two right angles put A, B, C, D on a
  coordinate grid with no square roots anywhere, so both routes work in exact
  fractions and the answer is a fraction, not a surd.
* **q21's midpoint is the entire hypothesis.** The bisection ∠DCF = 2∠DCE holds
  at exactly one point of AD: the cubic `2e³ − 5e² + 6e − 2` factors as
  `(2e − 1)(e² − 2e + 2)` and the quadratic has no real root. That is also why
  "the answer must not involve trigonometric functions" is a *hint* rather than a
  formatting rule — a linear answer is only possible under the bisection.
* **q21 cannot vary its figure, so it varies its question.** Two more angles at C
  are linear in α for free — ∠DCF = 90° − α and ∠ECB = 45° + α/2 — and the
  generator picks among the three.
* **q22 only needs ∠B.** The answer is `180° − k·γ`, so pinning γ is the whole
  job; the triple-angle identity does it in one line. Both routes had to be
  taught to reject γ → 0, where the triangle collapses to a segment and any side
  ratio "works".
* **Both figures on page 4 are lettered only**, with no numbers baked in, so they
  are attached unconditionally — the first such pair on this sheet. q20's
  generator keeps AD > BC so that D stays above C as the crop draws it.
* **q23's wrap-around matters.** Round 1 is a *cycle*, not a path — the 50–1
  handshake is what makes it 50 rather than 49 — and the two rounds must be
  merged as a set, since {j, j+1} would otherwise be counted twice.
* **q24's factorial is the whole item.** Choosing 3 rows and 3 columns fixes a
  3×3 sub-grid; the cells inside it must form a permutation matrix. Stopping at
  `C(4,3)·C(5,3) = 40` is the natural wrong answer.
* **q26 never needs p.** `(x − r₁)(x − r₂)` *is* `x² − 17x − 632 − p`, so the
  parameter cancels against the `+ p` and only the shift survives. `check`
  deliberately probes five different values of p to test that.
* **q27 is additive, which is what makes it computable at all.** The sequence has
  ~36 000 terms and a₁ has 8 500 digits, so neither route can walk the integers.
  Because the process always attacks the smallest prime, the debris from one
  removal clears before the next larger prime is touched, so the count is
  `Σ e_p·T(p)` with `T(p) = 1 + Σ e_q(p−1)·T(q)`. The note "673 เป็นจำนวนเฉพาะ"
  exists precisely so that 2019 = 3·673 can be factored on sight.
* **q28's model is per-way, not per-jump.** Each *climb* is equally likely; the
  worked example in the statement (3 stairs → 4 ways) is what fixes that reading.
* **q29 needs nothing about 2562.** The answer is the integer square root of the
  bulb count, full stop — the pairing k ↔ n/k fails only on squares.
* **q30 has four cases, not three, and `check` is what found the fourth.** The
  first `solve` assumed the birthday had to be one of the three days; a variant
  disagreed, and the missing case is "the birthday is outside the window, so all
  three statements are lies", which needs B ∈ S₁ ∩ S₃. On the sheet's own data
  those two lists are disjoint, so the wrong model still gave the right answer —
  exactly the kind of silent error the two-route rule exists to catch.
* **q30's three lists were reverse-engineered, not searched.** Random triples
  almost never have a unique answer (1 hit in 40 000 tries), because the puzzle
  is *built*: S₁ and S₃ disjoint kills two cases, then S₂ holds the predecessor
  of every decoy in S₁ and the successor of every member of S₃ while omitting
  B − 1. `q30.build` reproduces the sheet's own three lists character for
  character from B = 20, and the generator uses it to make new puzzles.
