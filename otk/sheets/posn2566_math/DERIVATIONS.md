# posn2566_math — transcription and verified answers

`posn1-66-math.pdf` is 9 pages: page 1 is the cover and คำชี้แจง, the questions
run pages 2–9, 30 of them, fill-in-the-blank, "a fractional answer must be in
lowest terms".

## Read this before touching the text layer

**This sheet's text layer silently drops digits.** The Thai prose extracts
perfectly, so `itemNN.txt` *looks* trustworthy — but the digits typed in prose
are set in a font with no usable ToUnicode mapping and come back missing, while
digits inside the maths spans survive. Question 2's first line reads

> ในวันที่ 1 หนูปอหยิบส้มจากลังใบนี้ไป 3/4 ของส้มทั้งหมดและหยิบเพิ่มอีก 2 ลูก

and `page_texts` returns

```
ในวันที่  หนูปอหยิบส้มจากลังใบนี้ไป 𝟑/𝟒 ของส้มทั้งหมดและหยิบเพิ่มอีก ลูก
```

— "1" and "2" gone, the fraction intact. **There are also no question numbers at
all** in the text layer, which is why `sheetpipe extract` reports `0 items` and
writes no `itemNN.txt`. Everything below was transcribed from the renders in
`extract/pages/`, which are the whole sheet at 200 dpi.

```python
import fitz
doc = fitz.open("openthaiknowledge-bank/สอวน_math/posn1-66-math.pdf")   # 9 pages
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=200).save(f"p{i:02d}.png")
```

Every answer below was derived twice by different routes and the two agreed.
`ANSWER` in a solver module must be copied from here, never re-guessed.

| # | Question (abridged) | Answer | Both routes |
|---|---|---|---|
| 1 | `f(x) = x+10` for x < 100, else `f(f(x−11))`; find f(111) | **109** | for 100 ≤ k ≤ 110, k−11 < 100 so f(k) = f(k−1) = 109 · memoised recursion |
| 2 | crate of oranges: take 3/4 then +2, 2/3 then +2, 1/2 then +2; 1/34 left | **272** | unwind the three steps to `N/24 − 10/3 = N/34` · simulate forward for each N |
| 3 | `\|8−x\| = \|3−5x\| + \|4x+5\|`; a = max, b = min; find 5a − 4b | **8** | `(3−5x) + (4x+5) = 8−x`, so equality iff the two agree in sign · sweep x |
| 4 | `1 + 68x + 66y = xy` over ℤ; max \|x+y\| | **4624** | `(x−66)(y−68) = 67²`, walk the divisors · sweep x and solve for y |
| 5 | a = b(a+1), a,b ≠ 0; all values of `a/b² − b/a² − ab` | **3** | over a(a+1): `(a+1)³ − 1 − a³ = 3a(a+1)` · evaluate at many random a |
| 6 | isosceles AC = BC, AB = 16, area 48; find the altitude AE to BC | **48/5** | CD = 6 from the area, so BC = 10 and AE = 2·48/10 · coordinates and measure |
| 7 | pentagon ABCDE from four printed angles and AB = 4 | **8** | the area does not depend on BC at all — it is ½·AB² · build it at several BC and measure |
| 8 | n points red/black on a circle, `N_m = N_{m+1} = 90` | **19** | `k(n−k)` equal at m and m+1 forces n = 2m+1, then m(m+1) = 90 · scan (n, m) |
| 9 | two boxes, move one ball each way; P(both ratios change) | **13/30** | the ratios survive iff the two balls match, so 3/5·1/2 + 2/5·1/3 · enumerate every path |
| 10 | (a,b) with a > b in 0…9 and `x² − ax + b` with distinct positive integer roots | **7** | one root must be 1, so (a,b) = (k+1, k) for k = 2…8 · test all 100 pairs |
| 11 | rectangle 9×8, two inscribed circles in opposite corners, tangent | **5** | `(9−s)² + (s−8)² = s²` with s = r₁+r₂; the other root 29 is impossible · bisect on r₁ |
| 12 | rational (x, y) with `1+x+xy = x²` and `x²((1+y)(x+y)+1) = 1` | **(1/2, −5/2), (1, −1), (−1, −1)** | eliminating y gives `x(2x−1)(x−1)(x+1) = 0` · scan rationals with small denominators |
| 13 | ordered (A,B,C) with `A∪B∪C = {1..15}` and `A∩B∩C = ∅` | **6¹⁵ = 470184984576** | each element picks one of 6 patterns · brute force over a smaller universe |
| 14 | 4 people, 10 beds; AB adjacent, CD adjacent, AC not | **210** | 56 disjoint block placements ×4, minus the 14 touching cases · enumerate all 5040 placements |
| 15 | 33A, 5B6, 6C3, D11 average 500; largest 4-digit arrangement of A,B,C,D | **9640** | A = 0 and B+C+10D = 55, so D ∈ {4,5} · brute force over all (A,B,C,D) |
| 16 | roots of `x³ − 2023x² = 1` shifted by 1; find \|p(1) + p(−1)\| | **8102** | `p(x) = q(x−1)`, so p(1) = −1 and p(−1) = −8101 · numeric roots and a product |
| 17 | `(6a+b)² − (a+6b)² = 4900` over ℤ; least non-negative ab | **24** | it is `a² − b² = 140`, so ab = m² − n² with mn = 35 · sweep b and solve for a |
| 18 | `x⁵ + mx − 65` and `x⁵ + nx − 66` share a root | **(64, 65) and (−66, −67)** | subtracting gives x = 1/(n−m), and k⁴ \| 1 · sweep m, n and test for a common root |
| 19 | quadratic with p(4) = p(−4) = 4, p(5) > 0, p(1) ∈ ℤ; max p(1) | **10** | even, so p(1) = 4 − 15a with a > −4/9 · sweep a on a fine grid |
| 20 | least m with `2^(2^m) − 1` divisible by `2^1024 + 1` | **11** | `2^(2^m) − 1 = ∏_{j<m} F_j` and 2¹⁰²⁴+1 = F₁₀ · exact big-integer division |
| 21 | three circles, r₁ = 3, r₂ = 5, C₃ through O₂ with centre on C₂; find AF | **14** | power of A wrt C₃ is AB·AO₂ = 66 and AE = 33/7 · coordinates, intersect, measure |
| 22 | perpendiculars to all three sides; FG = 2, GD = 8, AD = 4, MD = 5 | **8** | MD is the median to the hypotenuse ⟹ AB = 10, and EFG ~ CAB at 1 : 5 · build the three lines and measure |
| 23 | A the centre of the small circle, AB = 3, BC = CD = 2, GD ⊥ CF | **21/5** | GC = GF puts D at the midpoint of CF; then `cos∠AED = BC/2AB` · solve the configuration numerically |
| 24 | quiz out of 3, mean a, modes a and b, total 23; max not scoring 3 | **22** | n·a = 23 forces a = 1, n = 23; c₀ = c₂ + 2c₃ · enumerate every count vector |
| 25 | six unit circles through the centre; shaded area | **3π − 3√3** | shaded = (inside exactly 1) + (inside exactly 3) = π + (2π − 3√3) · Monte-Carlo the same regions |
| 26 | five unit cubes glued, fitting a 2×2×2 box, up to rotation and reflection | **2** | 48 of the 56 five-subsets are connected, in two orbits · Burnside over the 48 symmetries |
| 27 | segments of integer length between lattice points of {0..5}² | **204** | 90 + 90 horizontal/vertical plus 24 of the (3,4) kind · enumerate all 630 pairs |
| 28 | integer a with every root of `ax² − (3a−4)x + 2(a−2) = 0` an integer | **−4, −2, −1, 0, 1, 2, 4** | x = 1 is always a root, the other is `2 − 4/a` · test each a by factorising the quadratic |
| 29 | six squares in a staircase; XY halves the area; find XY² | **157** | the unknown side satisfies the halving at s = 2 and s = 4, and "area > 4" kills s = 2 · integrate the area below XY |
| 30 | `f^16 = (F,F,F)`; find `f^23` | **P₂ true, Q₂ false, R₂ false** | f swaps (F,F,F) ↔ (T,F,F), and 23 is odd · iterate the truth table |

## Notes for whoever continues

* **q1 is McCarthy's function in disguise.** For 100 ≤ k ≤ 110 the inner
  argument k−11 lands in 89…99, which is below the threshold, so
  f(k) = f(f(k−11)) = f(k−1): the whole plateau collapses to f(99) = 109. Then
  f(111) = f(f(100)) = f(109) = 109. Iterating blindly from 111 without memoising
  is what makes this look hard.
* **q3's right-hand side is the triangle inequality wearing a disguise.**
  `(3−5x) + (4x+5) = 8−x` identically, so `|8−x| ≤ |3−5x| + |4x+5|` always, with
  equality exactly when the two summands share a sign. The solution set is
  therefore the interval `[−5/4, 3/5]` and nothing has to be solved.
* **q5 is constant.** Substituting b = a/(a+1) and putting everything over
  a(a+1) leaves `(a+1)³ − 1 − a³ = 3a² + 3a`, which cancels the denominator
  exactly. Every admissible (a, b) gives 3 — "all possible values" is a set with
  one element, which is the point of the question.
* **q7's answer does not depend on BC.** The stem gives `AB = 4` and four angles
  and then says only that `BC ≤ 4`; building the pentagon at BC = 1, 2, 3 and 4
  gives area 8 every time. The inequality is there to say the picture closes, not
  to pin a length. Reading it as a missing constant is the trap.
* **q11's quadratic has a second root that has to be thrown away.** `s² − 34s +
  145 = 0` gives s = 5 and s = 29; a rectangle 9 by 8 cannot hold circles whose
  radii sum to 29.
* **q15's S is a set over *all* valid (A,B,C,D).** A = 0 always (the units digit
  has to absorb a multiple of ten) and B + C + 10D = 55, which allows D = 4 with
  B+C = 15 and D = 5 with B+C = 5. The largest arrangement is 9640, from
  {0, 9, 6, 4}; the D = 5 branch tops out at 5500.
* **q20 is the Fermat-number factorisation.** `2^(2^m) − 1` factors as the
  product of `F_0 … F_{m−1}`, and `2^1024 + 1` is `F_10`, so m ≥ 11.
* **q22's MD is a median to a hypotenuse.** GD ⊥ AB makes GDB right-angled at D,
  and M is the midpoint of GB, so GB = 2·MD = 10, DB = 6 and AB = AD + DB = 10.
  Three lines each perpendicular to one side of a triangle bound a triangle
  *similar* to it, with F ↔ A, G ↔ B, E ↔ C — so FG : AB = 2 : 10 and the
  perimeter scales by 1/5.
* **q23's D is the midpoint of CF, and that is not given.** AB = AC (both radii
  of the small circle) makes ABC isosceles; chasing that angle around the big
  circle gives ∠GCF = ∠GFC, so GC = GF and the foot of the perpendicular from G
  lands at the midpoint. Hence DF = CD = 2, AD = 5, and the power of D is 10.
  Then `cos∠AED = cos∠ABC = BC/(2·AB)` finishes it.
* **q24: 23 is prime, and that is the whole first step.** The mean a must be one
  of the scores 0…3 and n·a = 23, so a = 1 and n = 23. Then c₀ = c₂ + 2c₃ and
  c₃ = 0 is impossible (it would force c₀ = c₂, giving either one mode or three).
* **q25's shading is "inside an odd number of circles".** Reading the crop as
  data: every region inside exactly one of the six unit circles is grey, every
  region inside exactly two is white, every region inside exactly three is grey —
  confirmed at 99.9% pixel agreement against a fitted model. The three areas are
  π, 3√3 and 2π − 3√3, summing to the big disc's 3π, so the shaded part is
  `π + (2π − 3√3) = 3π − 3√3`. The big circle's radius is √3, because two
  adjacent unit circles meet at the centre *and* at a point √3 away.
* **q29's "area more than 4 square units" is the disambiguating condition.**
  The halving equation has *two* roots, s = 2 and s = 4 — a rare exact
  coincidence — and the printed inequality is what discards s = 2. Read the
  layout as: the unknown square is bottom-aligned with the 3-square to its left,
  and the hanging 2-square keeps its own position, so only the unknown square's
  top edge moves with s.
* **q30's f has period 2 from the second step on.** f(F,F,F) = (T,F,F) and
  f(T,F,F) = (F,F,F), so once the orbit reaches (F,F,F) at n = 16 it alternates;
  23 − 16 = 7 is odd, so f²³ = (T,F,F).
