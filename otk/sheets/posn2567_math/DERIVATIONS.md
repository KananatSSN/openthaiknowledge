# posn2567_math — transcription and verified answers

The text layer of `posn1-67-math.pdf` **cannot be used**: its display equations
are partly vector-drawn, so extraction returns token soup. Question 1 comes out
as `2 2 2 6 a b c + + =` for `a² + b² + c² = 6`. Everything below was read off
the page renders (`extract/pages/pNN.png`) by eye.

Every answer here was derived twice by different routes and the two agreed —
that is the only reason to trust it. `ANSWER` in a solver module must be copied
from here, never re-guessed. Where a question is already digested, the module is
the authority and this file is the provenance.

Status: **all 30 digested** — every question has a solver, an independently
written `check`, five or six variants and a generator. `verify` reports
`30/30 green, 0 without an independent check`.

| # | Question (abridged) | Answer | Both routes |
|---|---|---|---|
| 1 | `a²+b²+c²=6`, `(a+b)(b+c)+(b+c)(c+a)+(c+a)(a+b)=21`; find `ab+bc+ca` | **5** | identity `T = s²+p`, `S = s²−2p` ⇒ `p=(T−S)/3` · random-sample identity test |
| 2 | `\|{n>0 : n divides 2024 with remainder 24}\|` | **12** | divisors of 2000 above 24 · direct loop `2024 % n == 24` |
| 3 | `15^{1/(x+1)} = (2025·5^{y/2})^{1/(x+13)}`, `x,y ∈ ℤ⁺`; find `x+y` | **7** (x=3, y=4) | match exponents of 3 and 5 · numeric log search |
| 4 | `A = a−a²+⋯−a^2024`, `B = a+a²+⋯+a^2024`; `{a>0 : 2A+B ≥ 0}` | **0 < a ≤ 3** | `2A+B = Σ a^{2j−1}(3−a)` · direct summation, sign flips at 3 |
| 5 | smallest `a` whose leading digit deleted gives `b` with `a = 29b` | **725** | `7·10^d = 28b` forces leading digit 7, `d≥2` · brute force to 10⁷ |
| 6 | all `n` with `n²` of the form `xx44yy` | **n = 880** (`774400`) | `11 \| n`, `x+y ≡ 7 (mod 11)` · scan 317…999 |
| 7 | `a³+1/a³=18`; find `1/a²+1/a⁵+1/a⁶+1/a⁷+a²+a⁵+a⁶+a⁷` | **1295** | `p₁=3`, `p_k = 3p_{k−1} − p_{k−2}` · numeric root for `a` then direct sum |
| 8 | `x²+2x+5 \| x⁴+mx³+4x²−3x+n`; find `m²+n²` | **26** (m=1, n=5) | coefficient matching · polynomial long division, remainder ≡ 0 |
| 9 | `{a : x²+2(a+2)x+a+14 = 0 has a positive real root}` | **a ≤ −5** | discriminant + Vieta sign analysis · numeric scan of a |
| 10 | rhombus `ABCD`, `CE ⊥ BE`; find `AC²/((AB)(AE))` | **2** | `AC² = 2s²(1+cos α)`, `AE = s(1+cos α)` · random-parameter construction |
| 11 | square `ABCD`, `EG ∥ AB`, `BF ⊥ FC`, `BF = 8`; area of `△AEG` | **32** = `BF²/2` | `BF² = s(s−y)` and `[AEG] = s(s−y)/2` · coordinate construction, bisecting for `y` |
| 12 | two circles, `∠ODE=15°`, `∠OBE=25°`; find `∠ACB + ∠ADO` | **125°** = `180 − 2u − v` | `∠ABC=90 ⇒ AE` a diameter ⇒ `∠ADO = 90−u`, `∠ACB = 90−u−v` · two-parameter family of figures solved by nested bisection |
| 13 | trapezoid, height 4, perpendicular diagonals, one diagonal 5; area | **50/3** = `h·d₁²/(2√(d₁²−h²))` | `sin θ = h/d₁`, `d₂ cos θ = h`, area `= d₁d₂/2` · build the trapezoid, shoelace it |
| 14 | two equal circles, inscribed isosceles triangle, small circle on a chord | **1/9** = `R²/(r+2R)²` | `sin α = r/(r+2R)`, `d = Rr/(r+2R)`, `ρ = (R−d)/2` · tangent-length construction, `ρ` bisected out of the tangency |
| 15 | `∠DCF = 2(∠ADE − ∠BAD)`; find `∠ADE` | **75°** = `45 + 90/(k+1)` | tangent–chord `θ+α=90`, `180−(θ−α)=k(θ−α)` · sweep A round the circle, measure the condition |
| 16 | regular hexagon, `AM = CN`; find `∠BND` | **120°** = `720/n` | the rotation by `2·(360/n)` maps `A→C, B→D, C→E`, so `MB̅ → ND̅` · slide N along CE̅ until `CN = AM`, then measure |
| 17 | cuboctahedron, edge 1; volume | **5√2⁄3** = `(5/3)a³√2` | cube of side `a√2` minus 8 corner tetrahedra · brute-force convex hull of the 12 vertices, summed cone by cone |
| 18 | circles r=4, r=1 on a line; two equal circles between them; find `r` | **(13−3√17)/2** ≈ 0.31534 | touch points `2√(ρ₁ρ₂)` apart ⇒ `s²+3s−2=0`, `r=s²` · place circles by distance and bisect until the two small ones touch |
| 19 | `A={1..67}`; subsets summing to 2272 | **4** | complement sums to 6, partitions into distinct parts · full subset-sum DP on the printed target |
| 20 | digits with `a < b ≤ c < d` | **330** = `C(m+2,4)` | `(a,b,c,d) ↦ (a,b,c+1,d+2)` is a bijection onto strict quadruples · brute force |
| 21 | `P(same colour) = 4/9`; blue balls in box 2 | **25** | linear in b: `b = g₂(p(g₁+b₁)−g₁)/(b₁−p(g₁+b₁))` · scan b and recompute the probability |
| 22 | `P(orange) = 1/a`; sum of possible `a` | **16** = `d(m)+σ(m)` | `a = 1 + m/k` integral ⇔ `k \| m`; m = 13 is prime · scan k, keep the unit fractions |
| 23 | three cards with replacement; `P(product divisible by 10)` | **52/243** | inclusion–exclusion `n^k−(n−F)^k−(n−E)^k+(n−F−E+T)^k` · enumerate every draw |
| 24 | 20 red on the diameter, 4 green on the arc; quadrilaterals | **1221** | `C(g,4)+C(g,3)r+C(g,2)C(r,2)` · coordinates, reject collinear triples |
| 25 | `x+2y+3z=12`; `\|B\| − \|A\|` (non-negative minus positive) | **12** | `19 − 7`; positives of N ↔ non-negatives of N−(a+b+c), both from a generating function · enumerate the triples |
| 26 | `X = {\|x−3\|+\|x−5\|+\|x−8\| : −3 ≤ x ≤ 10}`; `a+b` | **30** | convex: min at the median (5), max at the *far* end (25) · dense rational scan |
| 27 | `p²⁰x² + nx + q²⁴ = 0` all-rational; `\|A\|` | **263** = `((e+1)(f+1)+F)/2` | `n = p^i q^j + p^{e−i} q^{f−j}`, paired by swapping the factors · build the set of n, plus a discriminant scan at small exponents |
| 28 | `A={1,5,7,{1},{7},{1,5},{5,7}}`, `\|A−B\|=4`; `\|S\|` | **2¹²⁶** | only 4 elements of `A` lie in `P(A)`: `C(4,3)·2¹²⁴` · construct A and P(A), find the overlap, brute-force every B when P(A) is small |
| 29 | round robin, six constraints; points of B | **9** | flat product over 3¹⁰, unique table `A2 B9 C4 D12 E1` · pruning backtrack over the same space, written separately |
| 30 | four men, four farms, four surnames | **A มานะ/วัว, B ลือชัย/ไก่, C ปันใจ/หมู, D เบิกบาน/กุ้ง** | enumerate all 4!·4! and filter · eliminate on a candidate grid, enumerate only the remainder |

## Notes for whoever continues

* **q11–q15 turned out to generalise cleanly**, which is why each has a real
  generator: the column above records the closed form in the constants, not just
  the sheet's number. q11 in particular does not need the square's side at all.
* **q14's picture is only right when the two big circles are equal**, so its
  generator shows the crop on those draws and passes `figure=None` on the rest —
  and says both radii out loud when they differ.
* **q13 is only a "เศษส่วนอย่างต่ำ" when `d₁²−h²` is a perfect square**, so its
  solver returns `None` otherwise and the generator's pool is exactly the
  Pythagorean pairs.

* **q17's answer is not a fraction** even though the sheet says
  "เขียนคำตอบเป็นเศษส่วนอย่างต่ำ". The volume is `5√2/3`; the instruction refers
  to the rational coefficient. Its `solve` therefore returns *the coefficient of
  √2* and the generator writes the radical back on.
* **Two answers here are irrational, and `sheet.json`'s `answer` field is a
  literal `str(ANSWER)`** — a test enforces that. So q17 records `5/3` and q18
  records `0.31534156157350957`; the human-readable surd lives in each item's
  `note`, not in the answer field.
* **q28's answer is astronomically large** (`2¹²⁶`), so its generator prints
  powers of two (`_pow2_tex`) and `sheet.json` records the 39-digit integer that
  `str(ANSWER)` produces.
* **q6 has a unique solution**, so the generator has to vary the *pattern*
  (`xx44yy`) rather than the numbers, or it will emit the same item forever.
* **q24's wording is load-bearing**: "มีจุดสีแดงเท่านั้นที่อยู่บนเส้นผ่านศูนย์กลาง"
  means the points on the diameter are exactly the red ones — all 20 of them.
* **q29 and q30 have unique solutions** under their constraint sets, and most
  *other* constraint sets do not. Both solvers return `None` unless exactly one
  solution survives, and both generators draw from a pool filtered on that — for
  q29 only a handful of (A's points, C's points) pairs qualify.
* **q30's answer is two Thai words**, which a MathBlock may not carry. The
  generated version numbers the surnames and farms in the prompt and asks for the
  pair of codes; the sheet's own version asks for all four people in prose.
* **q29 has no closed form**, so both of its routes are searches. They are
  written independently (flat product vs. pruning backtrack) and the real guard
  is the uniqueness requirement — say so rather than pretending otherwise.
