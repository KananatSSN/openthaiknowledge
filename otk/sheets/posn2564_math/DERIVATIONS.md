# posn2564_math — transcription and verified answers

ข้อสอบวิชาคณิตศาสตร์ เพื่อคัดเลือกนักเรียนเข้ารับการอบรมค่าย 1 สอวน. ปีการศึกษา 2564
(สอบวันอาทิตย์ที่ 9 มกราคม 2565, 09.00–12.00 น.)

**Source: `openthaiknowledge-bank/สอวน_math/posn1-64-math.pdf` — a pure scan.** Zero
characters in the text layer, one full-page image per page. Every stem below was
read off `extract/pages/pNN.png`; there are no `itemNN.txt` for this sheet and
there never will be. Page 1 is the cover, so **question 1 is on page 2** and the
printed page numbers run one behind the PDF page index.

Render the pages with:

```python
import fitz, pathlib
out = pathlib.Path("otk/sheets/posn2564_math/extract/pages"); out.mkdir(parents=True, exist_ok=True)
for i, p in enumerate(fitz.open("openthaiknowledge-bank/สอวน_math/posn1-64-math.pdf")):
    p.get_pixmap(dpi=220).save(str(out / f"p{i+1:02d}.png"))
```

220 dpi is enough to read this scan comfortably, including the Thai prose.

Every answer in the table was derived twice by different routes and the two
agreed. **Copy `ANSWER` from here; never re-guess it.**

| # | หัวข้อ | answer |
|---|---|---|
| 1 | อัตราส่วนจากสมการกำลังสอง | √2 |
| 2 | สมการเลขยกกำลังเศษส่วน | x = 63/5 |
| 3 | เส้นตรงและพาราโบลา | m + k + a = −5 |
| 4 | โจทย์ปัญหาอัตราส่วนและร้อยละ | 7 : 2 |
| 5 | โจทย์ปัญหาอัตราส่วน | 2340 ตารางหน่วย |
| 6 | ฟังก์ชันบนเลขโดด | 36 |
| 7 | ทฤษฎีกราฟเบื้องต้น | 3 นัด |
| 8 | โจทย์ปัญหาร้อยละ | 14 ห้อง |
| 9 | เรขาคณิตวงกลม | ∠ACD = 145° |
| 10 | เรขาคณิตวงกลม | PR = 3√7 |
| 11 | พื้นที่รูปสี่เหลี่ยมและสามเหลี่ยม | 9 ตารางหน่วย |
| 12 | การจัดรูปพีชคณิต | a + 2/a = 5 |
| 13 | พหุนามและการประมาณค่า | P(x) = 2x² − 6x + 5 |
| 14 | เลขคณิตมอดุลาร์ | 101 |
| 15 | การหารลงตัวและการนับ | 70 |
| 16 | ตรรกศาสตร์เชิงปริศนา | a² + b² = 17 |
| 17 | ตรรกศาสตร์เชิงปริศนา | 501 บาท |
| 18 | ตรรกศาสตร์เชิงปริศนา | 12 คน |
| 19 | ความน่าจะเป็น | 1/n³ |
| 20 | เรขาคณิต: เส้นแบ่งครึ่งมุม | CE = 7 หน่วย |
| 21 | เรขาคณิตวงกลม | BO : BD = 6 : 5 |
| 22 | เรขาคณิตวงกลม | รัศมี 36 หน่วย |
| 23 | โจทย์ปัญหาปริมาตร | m = 63 |
| 24 | เรขาคณิตวงกลม | AD² = 130 + 12√13 |
| 25 | ตัวดำเนินการนิยามใหม่ | 7980/443 |
| 26 | อสมการและช่วง | −3 < t < 2 |
| 27 | ตัวหารและการแยกตัวประกอบ | 2⁴² · 641⁴⁶ |
| 28 | ระบบสมการเลขยกกำลัง | (1, 1) และ (9, 3) |
| 29 | ทฤษฎีจำนวน: การนับ | 512 |
| 30 | พื้นที่รูปสี่เหลี่ยม | 36 ตารางหน่วย |

---

## หน้า 2 — ข้อ 1–7

**1.** กำหนดให้ `a` และ `x` เป็นจำนวนจริง โดยที่ `0 < a < x` และ `x² + a² = 6ax`
จงหาค่าของ `(x + a)/(x − a)`

> Square it: `((x+a)/(x−a))² = (x²+2ax+a²)/(x²−2ax+a²) = 8ax/4ax = 2`, using
> `x²+a² = 6ax` in both places. `x > a > 0` makes the ratio positive, so it is
> **√2**. Second route: `x = a(3 + 2√2)` explicitly, then evaluate.

**2.** จงหาจำนวนจริง `x ≠ 0` **ทั้งหมด** ที่สอดคล้องกับสมการ
`(13+x)^(2/3) + 4(13−x)^(2/3) = 5(169 − x²)^(1/3)`

> With `u = (13+x)^(1/3)`, `v = (13−x)^(1/3)` the equation is `u² − 5uv + 4v² = 0`
> `= (u − v)(u − 4v)`. `u = v` gives `x = 0`, **which is exactly what the printed
> `x ≠ 0` excludes** — the qualifier is load-bearing. `u = 4v` gives
> `13 + x = 64(13 − x)`, so `x = 819/65 = **63/5**`.

**3.** กำหนดให้ `a, m, k` เป็นจำนวนจริง ถ้าเส้นตรง `y = x − 2a` ผ่านจุด `(2m, a)`
ที่อยู่ในจตุภาคที่ 3 และเส้นตรง `y = 3x − 2k` ตัดกับพาราโบลา
`y = −2x² + x − m + k + 6` ที่จุด `(a, 2)` จงหาค่าของ `m + k + a`

> `(2m, a)` on the first line gives `3a = 2m`. `(a,2)` on the second gives
> `k = (3a−2)/2`. Substituting both into the parabola collapses to
> `2 = −2a² + a + 5`, i.e. `2a² − a − 3 = 0`, roots `a = 3/2` and `a = −1`.
> **จตุภาคที่ 3 picks `a = −1`** (the point is (−3, −1)); then `m = −3/2`,
> `k = −5/2` and `m + k + a = **−5**`.

**4.** ร้านค้าขายเมล็ดกาแฟอาราบิก้าผสมโรบัสต้า โรบัสต้ากิโลกรัมละ 100 บาท
อาราบิก้ากิโลกรัมละ 400 บาท ต้องผสมโรบัสต้าต่ออาราบิก้าเป็นอัตราส่วนเท่าใด
จึงทำให้ได้กำไร 20% เมื่อขายกาแฟผสมกิโลกรัมละ 200 บาท

> Selling at 200 with 20% profit means cost `200/1.2 = 500/3` per kg. With
> fractions `r + a = 1`: `100r + 400a = 500/3` gives `a = 2/9`, `r = 7/9`, so
> โรบัสต้า : อาราบิก้า = **7 : 2**.

**5.** บ่อเลี้ยงปลาทรงสี่เหลี่ยมมุมฉาก กว้าง `x` ยาว `y` ลึก `z` หน่วย โดยที่
`x : (y+z) = 1 : 5`, `z : (x+y) = 2 : 3` และความยาวของบ่อยาวกว่าความลึกอยู่ 6 หน่วย
จงหาพื้นที่ก้นบ่อเลี้ยงปลานี้

> `5x = y + z`, `3z = 2(x + y)`, `y = z + 6`. Eliminating gives `z = 72`,
> `y = 78`, `x = 30`. **ก้นบ่อ is the floor**, so the area is `x·y = **2340**`
> square units — not `x·z` and not the surface area.

**6.** จงหาค่าของ `B(1) + B(2) + ⋯ + B(99)` เมื่อ `B(n)` = จำนวนเลขโดดที่แตกต่างกัน
ของ `n` ถ้า 9 เป็นเลขโดดของ `n`, และ `B(n) = 0` ถ้าไม่ใช่ (เช่น `B(191) = 2`,
`B(524) = 0`)

> Only the numbers containing a 9 contribute: `9` → 1; the eight numbers
> `19, 29, …, 89` → 2 each = 16; `90…98` → 2 each = 18, and `99` → 1. Total
> **36**. Confirmed by direct enumeration over 1–99.

**7.** การแข่งขันฟุตบอลแบบพบกันหมด 7 ทีม (A–G) ทีม A แข่งไปแล้ว 6 นัด, B 5 นัด,
C 4 นัด, D 3 นัด, E 2 นัด, F 1 นัด จงหาว่าทีม G แข่งไปแล้วกี่นัด

> A has played everyone and F has played only A; peeling that pair off repeatedly
> forces the rest. **G = 3.** Verified by brute force over all 2²¹ graphs on 7
> vertices: the degree sequence `(6,5,4,3,2,1,g)` is realisable **only** for
> `g = 3`, so the answer is unique rather than merely consistent.

---

## หน้า 3 — ข้อ 8–10

**8.** โรงเรียนมีนักเรียน ม.3 จำนวนเท่ากันในทุกห้อง ต้องจัดห้องเรียนเพิ่มอีก 6 ห้อง
และพบว่าจำนวนนักเรียนต่อห้องลดลงจากเดิม 30% พอดี จงหาว่าเดิมมีกี่ห้อง

> `N/(r+6) = 0.7 · N/r` gives `0.3r = 4.2`, so `r = **14** ห้อง`. The head count
> `N` cancels and is never needed.

**9.** [รูป] `A, B, C` อยู่บนวงกลมที่มี `O` เป็นจุดศูนย์กลาง เส้นตรง `AO` ตัดกับ
`BC` และวงกลม ที่จุด `D` และ `E` ตามลำดับ ถ้า `∠BAC = 30°` และ `∠CDE = 10°`
แล้ว `∠ACD` มีขนาดเท่าไร

> `AE` is a **diameter** (it runs through `O`), so `∠ACE = 90°`. Writing
> `γ = ∠ACB`: triangle `CED` gives `∠DEC = 80° + γ`, hence `∠AEC = 100° − γ`;
> `ABCE` cyclic with `B`, `E` on opposite sides of `AC` gives `∠ABC = 80° + γ`;
> and the angle sum of `ABC` gives `30 + (80+γ) + γ = 180`, so `γ = 35°` and
> `∠ACD = 180° − γ = **145°**`.
> Verified by sweeping an explicit unit-circle construction until `∠CDE = 10°`:
> it returns `∠ACD = 144.995°`, `∠ACB = 35.005°`.

**10.** [รูป] เส้นตรง `ℓ` สัมผัสวงกลมสองวงที่มีจุดศูนย์กลาง `O₁`, `O₂` ที่จุด `P`
และ `Q` ตามลำดับ `O₁O₂` ตัดกับ `PQ` ที่จุด `R` ถ้า `PR : RQ = 3 : 4`,
`QO₂ = 12` หน่วย และ `O₁O₂ = 28` หน่วย แล้วจงหาความยาว `PR`

> `ℓ` is the **internal** tangent (it crosses between the circles), so
> `△O₁PR ~ △O₂QR` with ratio `3 : 4`. Then `O₁P = 9`, `O₁R = 12`, `O₂R = 16`,
> and `PR = √(12² − 9²) = √63 = **3√7**`. Cross-check: `QR = √(16² − 12²) = 4√7`
> and `PR : QR = 3 : 4` as printed.

---

## หน้า 4 — ข้อ 11–16

**11.** [รูป] รูปสี่เหลี่ยมผืนผ้า `ABCD` มีพื้นที่ 105 ตารางหน่วย `E`, `F` อยู่บน
`AB`, `BC` ถ้า `AE : EB = 4 : 3` และ `BF : FC = 2 : 3` จงหาพื้นที่ของ `△EBF`

> `[EBF] = ½ · (3/7)AB · (2/5)BC = (3/35) · 105 = **9**`. The rectangle's shape
> never enters — only its area.

**12.** กำหนดให้ `a` เป็นจำนวนจริงบวกที่สอดคล้องกับ `(a³ + 8/a³)² = 9025`
จงหาค่าของ `a + 2/a`

> `a³ + 8/a³ = 95` (positive root). With `t = a + 2/a`, `t³ = a³ + 8/a³ + 6t`,
> so `t³ − 6t − 95 = 0`, whose only real root is `t = **5**`.

**13.** จงหาพหุนาม `P(x)` ที่มีดีกรีน้อยที่สุด ซึ่ง `P(1) = P(2) = 1` และ `P(3) = 5`

> Three conditions, so degree ≤ 2; degree 1 is impossible because `P(1) = P(2)`
> would force a constant. `P(x) = **2x² − 6x + 5**`.

**14.** จงหาผลรวมของจำนวนเต็มบวก `n` **ทั้งหมด** โดยที่ `10 ≤ n ≤ 99` และ `nᵏ` มี
เลขสองหลักสุดท้ายเหมือนกับ `n` สำหรับทุกจำนวนเต็มบวก `k`

> The condition is `n² ≡ n (mod 100)`, i.e. `n ≡ 0 or 1` mod 4 and mod 25. The
> four combinations give `0, 1, 25, 76`; the two-digit ones are `25` and `76`,
> summing to **101**. Confirmed by testing `k = 1…40` for every two-digit `n`.

**15.** จงหาจำนวนของสามสิ่งอันดับ `(a,b,c)` **ทั้งหมด** ที่ `a,b,c ∈ {1,2,3,4,5}`
และ `(a+3)^(b^c)` หารด้วย 4 ลงตัว

> `a = 1` → `4^m`, always divisible (25 triples). `a = 5` → `8^m`, always (25).
> `a = 3` → `6^m`, divisible by 4 only when `m ≥ 2`, i.e. `b ≠ 1` (20).
> `a = 2, 4` → odd base, never. Total **70**, confirmed by enumeration.

**16.** สลาก 1,2,3,4 อย่างละหนึ่งใบในกล่องทึบสองกล่อง คุณครูสุ่มหยิบกล่องละ 1 ใบ
เด็กชาย A ทราบผลรวม เด็กหญิง B ทราบผลคูณ
A: เธอรู้ไหมว่าคุณครูหยิบได้เลขอะไรบ้าง /
B: พยายามคิดแล้วแต่ตัวเลขที่ได้ยินมันยังบอกไม่ได้ว่าคุณครูหยิบได้เลขอะไรบ้าง แล้วเธอล่ะ /
A: ตอนแรกก็ไม่รู้ แต่ตอนนี้รู้แล้วแหละ **ฉันได้ยินคนละเลขกับเธอนะ** /
B: อ๋อ ตอนนี้ฉันก็รู้แล้ว
ให้ `a, b` เป็นเลขที่คุณครูหยิบได้ แล้วค่าของ `a² + b²` เป็นเท่าใด

> B not knowing forces the product to be **4** (`{1,4}` or `{2,2}` — every other
> product determines its pair). A's "at first I didn't know" narrows the sum to
> an ambiguous one, and "now I know" leaves both `{1,4}` (sum 5) and `{2,2}`
> (sum 4) alive — so **the last clause is what finishes it**: `ฉันได้ยินคนละเลข`
> says A's number differs from B's, and `{2,2}` has sum = product = 4. Hence
> `{1,4}` and `a² + b² = **17**`. Verified by exhaustive elimination.

---

## หน้า 5 — ข้อ 17–18

**17.** นักเรียน 5 คน (A–E) ได้รับเหรียญคนละ 1 เหรียญ (50 สตางค์, 1, 2, 5, 10 บาท)
และธนบัตรคนละ 1 ใบ (20, 50, 100, 500, 1000 บาท) โดย
• B, ผู้ได้ธนบัตร 20, ผู้ได้ธนบัตร 50, ผู้ได้เหรียญ 2 บาท และผู้ได้เหรียญ 50 สตางค์
เป็นคนละคนกัน • D ไม่ได้ธนบัตร 20 • ผู้ได้เหรียญ 50 สตางค์ คือ A
• ธนบัตรที่ C ได้มีมูลค่า 100 • D ได้เหรียญ 5 บาท • E ไม่ได้เหรียญ 1 บาท
• ผู้ได้เหรียญ 1 บาทไม่ได้ธนบัตร 1000 — นักเรียน B ได้รับเงินรวมกี่บาท

> The first bullet names **five pairwise-distinct people out of five**, so
> `{ธนบัตร 20, ธนบัตร 50, เหรียญ 2 บาท} = {C, D, E}`. C holds the 100 note, so C
> takes the 2-baht coin; D is barred from the 20, so D takes the 50 note and E
> the 20. E refuses the 1-baht coin, so B holds it, and the last bullet keeps the
> 1000 away from B. **B = 1 บาท + 500 บาท = 501 บาท.** A full search over the
> `120 × 120` assignments returns exactly one solution.

**18.** ห้องเรียนมีนักเรียน 24 คน คนที่ 1 พูดว่า "ไม่มีใครในห้องนี้พูดจริงเลย",
คนที่ `k` พูดว่า "ในห้องนี้มีคนพูดจริงอย่างมาก `k−1` คน" จงหาว่ามีคนพูดจริงกี่คน

> If exactly `t` tell the truth, statement `k` is true precisely when `k ≥ t+1`,
> so `24 − t` statements are true — and the truth-tellers *are* those statements'
> speakers, so `t = 24 − t` and `t = **12**`.

---

## หน้า 6 — ข้อ 19–23

**19.** กำหนดให้ `n ≥ 2` เป็นจำนวนนับ สุ่มเลือกจำนวนนับ `a, b ∈ {1,2,…,n²}`
จงหาความน่าจะเป็นที่สมการ `x² + ax + b = 0` จะมีคำตอบเดียว

> One root means `a² = 4b`, so `a = 2m` and `b = m²` with `m² ≤ n²`, i.e.
> `m ≤ n` — exactly `n` favourable pairs out of `n⁴`. Probability `**1/n³**`,
> confirmed by counting for `n = 2,3,4,5`.

**20.** `ABC` เป็นรูปสามเหลี่ยม เส้นแบ่งครึ่งมุมภายในของ `∠ABC` ตัดกับ
เส้นแบ่งครึ่งมุมภายนอกของ `∠ACB` ที่จุด `D` เส้นตรงที่ขนานกับ `BC` ผ่าน `D`
ตัด `AC` ที่ `E` และตัด `AB` ที่ `F` ถ้า `EF = 9` และ `BF = 16` แล้ว `CE` เท่าใด

> `FD ∥ BC` makes `∠FDB = ∠DBC = ∠DBF`, so `FD = FB = 16`; the external bisector
> at `C` makes `△EDC` isosceles the same way, so `CE = ED`. With `F, E, D` in
> that order, `CE = ED = FD − FE = 16 − 9 = **7**`.
> Verified on three unrelated triangles: `FD = BF` and `CE = BF − EF` in each.

**21.** วงกลมแนบในรูปสามเหลี่ยม `ABC` มีจุดศูนย์กลาง `O` และสัมผัส `AB` ที่ `D`
ลากเส้นจาก `B` ผ่าน `O` ไปตัดวงกลมล้อมรอบที่จุด `P` ถ้า `AC = 15` หน่วย และ
`AP = 9` หน่วย แล้วอัตราส่วน `BO : BD` มีค่าเท่าใด

> `BD = r·cot(B/2)` and `BO = r/sin(B/2)`, so `BO : BD = 1 : cos(B/2)`. `AP` and
> `AC` are chords of the circumcircle subtending `B/2` and `B`, so
> `AC/AP = sin B / sin(B/2) = 2cos(B/2)`. Hence `BO : BD = 2AP : AC = 18 : 15 =
> **6 : 5**`. Verified on three triangles: `BO/BD = 2·AP/AC` to 6 places.

**22.** [รูป] `O` เป็นจุดศูนย์กลางของวงกลมซึ่งมีคอร์ด `AB` และ `CD` ตั้งฉากและ
ตัดกันที่จุด `X` ถ้า `AB = 56`, `CD = 64` และ `OX = 28` หน่วย แล้วรัศมียาวกี่หน่วย

> The distances from `O` to the two chords are the legs of a right triangle with
> hypotenuse `OX`, so `OX² = (r²−28²) + (r²−32²)`, giving `2r² = 2592` and
> `r = **36**`.

**23.** ลูกบาศก์ทรงตันสองชนิด: กว้าง 3 ซม. หนัก 200 กรัม 100 ลูก และกว้าง 2 ซม.
หนัก 400 กรัม 100 ลูก ถังน้ำ `A` เต็มพอดี หย่อนลูกบาศก์รวม `m` ลูกลงไปจนจมมิด
น้ำล้นออกมาไม่เกิน 1,000 ลูกบาศก์เซนติเมตร ถ้าน้ำหนักรวมของลูกบาศก์เท่ากับ 20
กิโลกรัม แล้ว `m` มีค่ามากที่สุดเท่ากับเท่าใด

> With `i` big and `j` small cubes: `200i + 400j = 20000` → `i + 2j = 100`, and
> the overflow is the submerged volume `27i + 8j = 2700 − 46j ≤ 1000` → `j ≥ 37`.
> Since `m = i + j = 100 − j`, **maximising `m` means minimising `j`**: `j = 37`,
> `i = 26`, `m = **63**` (overflow 998 cm³).

---

## หน้า 7 — ข้อ 24–28

**24.** [รูป] วงกลมมี `AD` เป็นเส้นผ่านศูนย์กลาง และ `AC` ตัดกับ `BD` ที่จุด `E`
ถ้า `AE = √13`, `BE = 2` และ `CD − CE = 3` หน่วย แล้วจงหาค่าของ `AD²`

> `AD` diameter gives right angles at `B` and `C`. From `△ABE`: `AB = 3`. Writing
> `CE = c`, `CD = c+3`, the power of `E` gives `√13·c = 2·ED` and Pythagoras in
> `△ECD` gives `ED² = c² + (c+3)²`; together `5c² − 24c − 36 = 0`, so `c = 6`.
> Then `AD² = AC² + CD² = (√13+6)² + 81 = **130 + 12√13**` — checked a second way
> as `AB² + BD² = 9 + (2 + 3√13)²`, same value.

**25.** สำหรับจำนวนจริงบวก `x, y` กำหนด `x ⊕ y = xy/(x+y)` (เปลี่ยนกลุ่มได้)
จงหาค่าของ `(1·2·3·4) ⊕ (2·3·4·5) ⊕ ⋯ ⊕ (18·19·20·21)`
(ตอบเป็นเศษส่วนของจำนวนเต็ม โดยไม่จำเป็นต้องเป็นเศษส่วนอย่างต่ำ)

> `⊕` is the harmonic mean operation: `1/(x⊕y) = 1/x + 1/y`, so the answer is the
> reciprocal of `Σ 1/(k(k+1)(k+2)(k+3))` for `k = 1…18`. Telescoping,
> `Σ = ⅓(1/6 − 1/7980) = 1329/23940`, so the value is `23940/1329 = **7980/443**`
> (443 is prime). The stem's "ไม่จำเป็นต้องเป็นเศษส่วนอย่างต่ำ" is why 23940/1329
> is equally acceptable.

**26.** จงหาจำนวนจริง `t` **ทั้งหมด** ที่ทำให้อสมการ
`−2 < (2x² + tx − 3)/(x² + x + 2) < 3` เป็นจริงสำหรับทุกจำนวนจริง `x`

> The denominator is always positive (disc `1 − 8 < 0`), so each side becomes a
> quadratic that must be positive definite: `4x² + (t+2)x + 1 > 0` needs
> `−6 < t < 2`, and `x² + (3−t)x + 9 > 0` needs `−3 < t < 9`. Intersection:
> `**−3 < t < 2**`. Spot-checked at `t = ±` either side of both endpoints.

**27.** จงหาจำนวนเต็มบวกมากสุดซึ่งมี 2564 เป็นตัวประกอบ และมีจำนวนตัวหารบวกอยู่
ทั้งหมด 2021 จำนวนพอดี (หมายเหตุ: 43, 47 และ 641 เป็นจำนวนเฉพาะ)

> `2564 = 2²·641` and `2021 = 43·47`, so the number is `2^a·641^b` with
> `(a+1)(b+1) = 2021` and `a ≥ 2`, `b ≥ 1` — either `(42, 46)` or `(46, 42)`.
> The larger puts the **larger exponent on the larger prime**:
> `**2⁴² · 641⁴⁶**`.

**28.** จงหาคู่อันดับ `(x,y)` ของจำนวนเต็มบวก **ทั้งหมด** ที่สอดคล้องกับระบบสมการ
`(√x)^(x+y) = y¹²` และ `(√y)^(x+y) = x³`

> Clearing the roots: `x^(x+y) = y²⁴` and `y^(x+y) = x⁶`. For `x, y > 1`, taking
> logs and multiplying gives `((x+y)/2)² = 36`, so `x + y = 12` and `x = y²`,
> hence `y = 3`, `x = 9`. **`(1,1)` also satisfies both equations** and is easy
> to lose, since the log argument divides by `ln x · ln y`. Answer:
> `**(1,1) และ (9,3)**`, confirmed by exact integer search to 400.

---

## หน้า 8 — ข้อ 29–30

**29.** ให้ `A` เป็นเซตของจำนวนตรรกยะ `r = a/b` ทั้งหมดที่อยู่ระหว่าง 0 และ 1 โดย
`a, b` เป็นจำนวนเต็มบวกซึ่ง ห.ร.ม. ของ `a` และ `b` เท่ากับ 1 และ
`ab = 30·29·28⋯3·2·1` จงหาจำนวนสมาชิกของ `A`

> Coprimality means each prime of `30!` goes wholly to `a` or wholly to `b`, so
> the coprime factorisations are `2^10` (there are **10 primes ≤ 30**), and
> `0 < r < 1` keeps exactly half: `2⁹ = **512**`. The multiplicities in `30!`
> never matter — only how many distinct primes it has.

**30.** [รูป] รูปสี่เหลี่ยมมุมฉากหมายเลข ①–⑤ มีพื้นที่ 13, 26, 20, 25 และ 27
ตารางหน่วย ตามลำดับ จงหาว่ารูปสี่เหลี่ยมมุมฉากที่แรเงามีพื้นที่เท่าใด

> **The layout is the data.** Reading the crop: the outer rectangle spans
> `x ∈ [0, X]`, with verticals at `a` (right edge of ① and ③) and `b` (right edge
> of ④). Horizontals at `y₁` (below row 1) and `y₂` (below row 2). ① `= a·u`,
> ② `= (X−a)·u`, ③ `= a·v`, ④ `= (b−a)·v`, ⑤ `= (X−b)(v+w)` — **⑤ runs from the
> row-1 line all the way to the bottom** — and the shaded rectangle is `b·w`
> under ③ and ④ together.
>
> ①:② = 13:26 gives `X = 3a`; ③:④ = 20:25 gives `b = 9a/4`; then ⑤ = 27 gives
> `(3a/4)(v+w) = 27`, so `a·w = 36 − a·v = 36 − 20 = 16`, and the shaded area is
> `b·w = (9/4)(a·w) = **36**`. Note the individual lengths are never determined —
> only the products are, which is why the answer exists at all.
