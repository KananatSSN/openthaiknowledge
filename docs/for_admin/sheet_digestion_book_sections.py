"""Claim every 🍰 book section for a knowledge unit (existing or new)."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\acer\Desktop\tutorrank\.claude\worktrees\sheet-digestion")
K = ROOT / "otk/knowledge/math"
DIG = ROOT / "openthaiknowledge-bank/_digest/rathcenter"

books = {}
for js in DIG.glob("*/🍰*.json"):
    d = json.loads(js.read_text("utf-8"))
    books[d["source"]] = sorted({it.get("section", "").rsplit(" ", 1)[0] for it in d["items"]})


def book(fragment):
    hits = [p for p in books if fragment in p]
    assert len(hits) == 1, (fragment, hits)
    return hits[0]


# New units: id → (file, kind, title, statement, extra fields, covered_by)
NEW = {
    "math.set.basics": ("sets.json", "fact-list", "ความหมาย สมาชิก และสับเซต",
                        "เซตกำหนดด้วยสมาชิก; a ∈ A คือ a เป็นสมาชิก; A ⊂ B เมื่อสมาชิกทุกตัวของ A อยู่ใน B; เซตที่มีสมาชิก n ตัวมีสับเซต 2ⁿ เซต และเพาเวอร์เซต P(A) มีสมาชิก 2ⁿ ตัว",
                        {"facts": {"สมาชิก": ["a ∈ A", "เซตว่าง ∅ ไม่มีสมาชิก", "สมาชิกของเซตอาจเป็นเซต"],
                                   "สับเซต": ["A ⊂ B", "∅ ⊂ A เสมอ", "จำนวนสับเซต 2ⁿ"]}},
                        ["math.set_cardinality", "math.count_subsets", "math.set_operations"]),
    "math.vector.basics": ("vectors.json", "fact-list", "เวกเตอร์ในระบบพิกัดฉาก ขนาด และเวกเตอร์หนึ่งหน่วย",
                           "เวกเตอร์มีขนาดและทิศทาง; ในพิกัดฉาก u = (a, b, c) มีขนาด √(a² + b² + c²); เวกเตอร์หนึ่งหน่วยในทิศ u คือ u/|u|; บวกลบและคูณสเกลาร์ทีละองค์ประกอบ",
                           {"facts": {"ขนาด": ["|u| = √(a² + b² + c²)"], "หนึ่งหน่วย": ["u/|u|"],
                                      "การดำเนินการ": ["u + v ทีละองค์ประกอบ", "ku คูณทุกองค์ประกอบ"]}},
                           ["math.vector_add", "math.vector_magnitude", "math.vectors", "math.vector_grid_picture_m5"]),
    "math.complex.arithmetic": ("complex.json", "procedure", "บวก ลบ คูณ หาร และสังยุคของจำนวนเชิงซ้อน",
                                "(a + bi)(c + di) = (ac − bd) + (ad + bc)i; หารโดยคูณเศษและส่วนด้วยสังยุคของตัวส่วน; รากที่สองของ a + bi หาได้จากระบบ x² − y² = a, 2xy = b",
                                {"steps": ["กระจายและแทน i² = −1", "หารโดยคูณสังยุคของตัวส่วน", "เทียบส่วนจริงและส่วนจินตภาพ"]},
                                ["math.complex_add_conjugate", "math.complex_multiply", "math.complex_equation_parts_m5"]),
    "math.counting.stars-bars": ("counting.json", "formula", "การแบ่งของเหมือนกันให้กลุ่มที่ต่างกัน (สตาร์แอนด์บาร์)",
                                 "จำนวนวิธีแจกของเหมือนกัน n ชิ้นให้ k กลุ่ม (กลุ่มว่างได้) คือ C(n + k − 1, k − 1); ถ้าทุกกลุ่มต้องได้อย่างน้อย 1 ชิ้น คือ C(n − 1, k − 1); เท่ากับจำนวนคำตอบจำนวนเต็มไม่เป็นลบของ x₁ + ⋯ + x_k = n",
                                 {"variables": [{"name": "n", "meaning": "จำนวนของ (เหมือนกัน)"},
                                                {"name": "k", "meaning": "จำนวนกลุ่ม"}]},
                                 []),
    "math.counting.binomial-theorem": ("counting.json", "formula", "ทฤษฎีบททวินาม",
                                       "(a + b)ⁿ = Σ C(n, r) aⁿ⁻ʳ bʳ; พจน์ที่ r + 1 คือ C(n, r) aⁿ⁻ʳ bʳ",
                                       {"variables": [{"name": "n", "meaning": "เลขชี้กำลัง"},
                                                      {"name": "r", "meaning": "ลำดับพจน์ลบหนึ่ง"}], "level": "ม.5"},
                                       ["math.binomial_term", "math.binomial_coefficient", "math.binomial_middle_coefficient",
                                        "math.binomial_apply_m5"]),
    "math.series.sigma": ("series.json", "fact-list", "สัญลักษณ์ซิกมาและสูตรผลบวก",
                          "Σ(a_k ± b_k) = Σa_k ± Σb_k, Σc·a_k = cΣa_k, Σc = nc; Σk = n(n + 1)/2, Σk² = n(n + 1)(2n + 1)/6, Σk³ = [n(n + 1)/2]²",
                          {"facts": {"สมบัติ": ["Σ(a ± b) = Σa ± Σb", "Σca = cΣa", "Σ_{k=1}^{n} c = nc"],
                                     "สูตร": ["Σk = n(n+1)/2", "Σk² = n(n+1)(2n+1)/6", "Σk³ = (n(n+1)/2)²"]}},
                          []),
    "math.derivative.rules": ("derivative.json", "fact-list", "อัตราการเปลี่ยนแปลงและสูตรอนุพันธ์",
                              "อัตราการเปลี่ยนแปลงเฉลี่ย (f(b) − f(a))/(b − a); อนุพันธ์ f′(x) = lim (f(x + h) − f(x))/h; d/dx xⁿ = nxⁿ⁻¹, กฎผลคูณ ผลหาร และอนุพันธ์อันดับสูง; ความเร็ว = s′, ความเร่ง = s″",
                              {"facts": {"นิยาม": ["เฉลี่ย (f(b) − f(a))/(b − a)", "ขณะใด ๆ lim_{h→0}"],
                                         "สูตร": ["xⁿ → nxⁿ⁻¹", "(uv)′ = u′v + uv′", "(u/v)′ = (u′v − uv′)/v²"],
                                         "การเคลื่อนที่": ["v = s′", "a = v′ = s″"]}},
                              ["math.derivative_poly", "math.derivative_evaluate_point", "math.derivative_negative_power",
                               "math.motion_derivative_m6"]),
    "math.calculus.extrema-basics": ("calculus-extrema.json", "procedure", "ฟังก์ชันเพิ่ม ฟังก์ชันลด และค่าสูงสุดต่ำสุด",
                                     "f เพิ่มเมื่อ f′ > 0 ลดเมื่อ f′ < 0; ค่าวิกฤตคือ x ที่ f′(x) = 0; ใช้ f″ หรือเครื่องหมายของ f′ บอกชนิดของจุด; ค่าสูงสุดสัมบูรณ์บนช่วงปิดดูที่ค่าวิกฤตและปลายช่วง",
                                     {"steps": ["หา f′ และค่าวิกฤต", "ตรวจเครื่องหมายของ f′ หรือ f″", "เปรียบเทียบค่าที่ค่าวิกฤตและปลายช่วง"]},
                                     ["math.extrema", "math.turning_point_m5", "math.derivative_sign_picture_m6",
                                      "math.optimization_word_m6"]),
    "math.real.field-properties": ("real-numbers.json", "fact-list", "ชนิดของจำนวนและสมบัติของการบวกการคูณ",
                                   "จำนวนจริงแบ่งเป็นตรรกยะ (จำนวนเต็ม เศษส่วน ทศนิยมซ้ำ) และอตรรกยะ; สมบัติปิด การสลับที่ การเปลี่ยนกลุ่ม การแจกแจง เอกลักษณ์ และตัวผกผัน; ตัวดำเนินการที่นิยามใหม่ (เช่น a * b = a + b − ab) ตรวจสมบัติเหล่านี้ได้เช่นเดียวกัน",
                                   {"facts": {"ชนิดของจำนวน": ["ตรรกยะ", "อตรรกยะ", "จำนวนเต็ม"],
                                              "สมบัติ": ["ปิด", "สลับที่", "เปลี่ยนกลุ่ม", "เอกลักษณ์", "ตัวผกผัน"]}},
                                   ["math.classify_real_number", "math.pick_irrational"]),
    "math.real.factoring": ("real-numbers.json", "procedure", "พหุนามและการแยกตัวประกอบ",
                            "แยกตัวประกอบด้วยการดึงตัวร่วม จัดกลุ่ม ผลต่างกำลังสอง กำลังสามสมบูรณ์ และผลบวก/ผลต่างกำลังสาม",
                            {"steps": ["ดึงตัวร่วม", "ลองจัดกลุ่มหรือสูตรพิเศษ", "ตรวจโดยกระจายกลับ"]},
                            ["math.factor_advanced", "math.factor_by_grouping", "math.factor_cubes"]),
    "math.real.equations": ("real-numbers.json", "procedure", "สมการตัวแปรเดียว",
                            "จัดสมการให้ข้างหนึ่งเป็นศูนย์ แยกตัวประกอบหรือใช้สูตร แล้วตรวจคำตอบ; สมการกำลังสองใช้ดิสคริมิแนนต์บอกจำนวนคำตอบ",
                            {"steps": ["ย้ายข้างให้เป็นศูนย์", "แยกตัวประกอบหรือใช้สูตร", "ตรวจคำตอบ"]},
                            ["math.polynomial_equation_m4", "math.discriminant", "math.vieta"]),
    "math.real.rational-expressions": ("real-numbers.json", "procedure", "เศษส่วนของพหุนามและสมการเศษส่วน",
                                       "ตัดทอนโดยแยกตัวประกอบ; สมการเศษส่วนคูณด้วยตัวส่วนร่วม แล้วตัดคำตอบที่ทำให้ตัวส่วนเป็นศูนย์",
                                       {"steps": ["แยกตัวประกอบตัวเศษและตัวส่วน", "คูณด้วยตัวส่วนร่วม", "ตัดคำตอบแปลกปลอม"]},
                                       ["math.rational_equation_m4", "math.rational_equation_extraneous_m4",
                                        "math.rational_inequality_m4"]),
    "math.real.intervals-inequalities": ("real-numbers.json", "procedure", "ช่วงและอสมการตัวแปรเดียว",
                                         "เขียนเซตคำตอบเป็นช่วง; อสมการพหุนามหาค่าวิกฤตแล้วตรวจเครื่องหมายทีละช่วง; คูณหรือหารด้วยจำนวนลบกลับเครื่องหมาย",
                                         {"steps": ["ย้ายข้างให้เป็นศูนย์และแยกตัวประกอบ", "ตรวจเครื่องหมายทีละช่วง", "เขียนคำตอบเป็นช่วง"]},
                                         ["math.quadratic_inequality", "math.quadratic_inequality_interval",
                                          "math.polynomial_inequality_m4"]),
    "math.radical.equations": ("radicals.json", "procedure", "สมการติดรูทและรูทไม่รู้จบ",
                               "ยกกำลังสองทั้งสองข้างเพื่อกำจัดรูท แล้วตรวจคำตอบกับสมการเดิม (ยกกำลังสองอาจเพิ่มคำตอบแปลกปลอม); รูทไม่รู้จบ x = √(a + √(a + ⋯)) ให้ x = √(a + x) แล้วเลือกคำตอบที่ไม่เป็นลบ",
                               {"steps": ["แยกรูทไว้ข้างเดียว", "ยกกำลังสองแล้วแก้สมการ", "ตรวจคำตอบกับสมการเดิม"]},
                               []),
    "math.circle.basics": ("circles.json", "formula", "สมการวงกลม",
                           "(x − h)² + (y − k)² = r²; รูปทั่วไป x² + y² + Dx + Ey + F = 0 มีจุดศูนย์กลาง (−D/2, −E/2)",
                           {"variables": [{"name": "(h, k)", "meaning": "จุดศูนย์กลาง"}, {"name": "r", "meaning": "รัศมี"}]},
                           ["math.circle_centre_radius", "math.circle_equation", "math.circle_from_centre_point"]),
    "math.conic.standard-forms": ("conics.json", "fact-list", "รูปมาตรฐานของพาราโบลา วงรี และไฮเพอร์โบลา",
                                  "พาราโบลา (x − h)² = 4c(y − k); วงรี x²/a² + y²/b² = 1 (c² = a² − b²); ไฮเพอร์โบลา x²/a² − y²/b² = 1 (c² = a² + b²)",
                                  {"facts": {"พาราโบลา": ["(x − h)² = 4c(y − k)", "เลตัสเรกตัมยาว |4c|"],
                                             "วงรี": ["c² = a² − b²"], "ไฮเพอร์โบลา": ["c² = a² + b²", "เส้นกำกับ y = ±(b/a)x"]}},
                                  ["math.parabola_conic_m4", "math.ellipse_m4", "math.hyperbola_m4"]),
    "math.line.distance-midpoint": ("lines.json", "formula", "ระยะระหว่างจุดและจุดกึ่งกลาง",
                                    "ระยะ √((x₂ − x₁)² + (y₂ − y₁)²); จุดกึ่งกลาง ((x₁ + x₂)/2, (y₁ + y₂)/2)",
                                    {"variables": [{"name": "(x₁, y₁), (x₂, y₂)", "meaning": "จุดปลาย"}]},
                                    ["math.distance_between_points", "math.midpoint", "math.distance_from_origin"]),
    "math.line.slope-equation": ("lines.json", "procedure", "ความชันและสมการเส้นตรง",
                                 "ความชัน m = (y₂ − y₁)/(x₂ − x₁); เส้นขนานความชันเท่ากัน ตั้งฉากผลคูณเป็น −1; สมการ y − y₁ = m(x − x₁)",
                                 {"steps": ["หาความชัน", "ใช้จุดหนึ่งจุดเขียนสมการ", "จัดรูปตามที่ต้องการ"]},
                                 ["math.slope_between_points", "math.slope_from_equation", "math.line_equation",
                                  "math.parallel_perpendicular_slope"]),
    "math.line.point-distance": ("lines.json", "formula", "ระยะจากจุดถึงเส้นตรงและระหว่างเส้นขนาน",
                                 "ระยะจาก (x₀, y₀) ถึง Ax + By + C = 0 คือ |Ax₀ + By₀ + C|/√(A² + B²); เส้นขนาน Ax + By + C₁ = 0, Ax + By + C₂ = 0 ห่างกัน |C₁ − C₂|/√(A² + B²)",
                                 {"variables": [{"name": "A, B, C", "meaning": "สัมประสิทธิ์ของเส้นตรง"}]},
                                 ["math.point_line_distance_m4"]),
    "math.matrix.arithmetic": ("matrices.json", "procedure", "การบวก คูณ และทรานสโพสของเมทริกซ์",
                               "บวกลบทีละตัว; AB มีสมาชิกแถว i หลัก j เป็นผลคูณเชิงสเกลาร์ของแถว i ของ A กับหลัก j ของ B; (AB)ᵗ = BᵗAᵗ",
                               {"steps": ["ตรวจมิติ", "คูณแถวกับหลัก", "จัดผลเป็นเมทริกซ์"]},
                               ["math.matrix_add_scalar", "math.matrix_multiply_2x2", "math.matrix_transpose_m5",
                                "math.determinant_2x2", "math.determinant_3x3_m5", "math.matrix_inverse_m5"]),
}

MAP = {
    "เซต พื้นฐาน": {"ความหมายของเซต": "set.basics", "เซตที่สมาชิกเป็นเซต": "set.basics", "สมาชิกของเซต": "set.basics",
                    "สับเซต": "set.basics", "แผนภาพเวนน์": "set.venn-read", "การปฏิบัติการทางเซต": "set.operations",
                    "สูตรการปฏิบัติการทางเซต": "set.identities", "จำนวนสมาชิกในส่วนต่างๆ": "set.union-formula"},
    "🍰 เวกเตอร์": {"ปริมาณเวกเตอร์": "vector.basics", "เวกเตอร์ในระบบพิกัดฉาก": "vector.basics",
                   "เวกเตอร์หนึ่งหน่วย": "vector.basics", "ผลคูณเชิงสเกลาร์": "vector.dot-angle",
                   "ผลคูณเชิงเวกเตอร์": "vector.cross-product", "พื้นที่และปริมาตร": "vector.triple-product"},
    "🍰 จำนวนเชิงซ้อน": {"จำนวนเชิงซ้อน": "complex.arithmetic", "สังยุค และการหาร": "complex.arithmetic",
                        "รากที่สอง": "complex.arithmetic", "ค่าสัมบูรณ์": "complex.modulus-rules",
                        "กราฟของจำนวนเชิงซ้อน": "complex.modulus-rules", "รูปเชิงขั้ว": "complex.polar-roots",
                        "รากที่ 𝑛": "complex.polar-roots", "สมการพหุนาม": "complex.conjugate-root"},
    "หลักการนับ เบื้องต้น": {"กฎการคูณ": "counting.multiplication", "กฎการบวก": "counting.addition-cases",
                            "แฟคทอเรียล": "counting.permutation", "การเรียงสับเปลี่ยน": "counting.permutation",
                            "เรียงให้บางชิ้นติดกัน": "counting.adjacency", "นับแบบตรงข้าม": "counting.complement",
                            "การจัดหมู่": "counting.combination"},
    "หลักการนับ เพิ่มเติม": {"ทบทวนความรู้พื้นฐาน": "counting.multiplication", "เรียงของซ้ำ": "counting.permutation",
                            "เรียงของเป็นวงกลม": "counting.permutation", "สตาร์ แอนด์ บาร์": "counting.stars-bars",
                            "ทฤษฏีบททวินาม": "counting.binomial-theorem"},
    "ความน่าจะเป็น พื้นฐาน": {"การทดลองสุ่มและเหตุการณ์": "probability.classical", "ความน่าจะเป็น": "probability.classical"},
    "ความน่าจะเป็น เพิ่มเติม": {"ทบทวนพื้นฐาน": "probability.classical"},
    "ลำดับและอนุกรม พื้นฐาน": {"ลำดับ": "sequence.patterns", "ลำดับเลขคณิต": "sequence.arithmetic",
                               "ลำดับเรขาคณิต": "sequence.geometric", "อนุกรม": "sequence.arithmetic",
                               "อนุกรมเลขคณิต": "sequence.arithmetic", "อนุกรมเรขาคณิต": "sequence.geometric",
                               "ดอกเบี้ยทบต้นแบบปีละหลายครั้ง": "finance.compounding-periods",
                               "มูลค่าเงิน": "finance.compound", "ค่างวด": "finance.compound"},
    "ลำดับและอนุกรม เพิ่มเติม": {"ทบทวนลำดับเลขคณิต": "sequence.arithmetic", "ทบทวนลำดับเรขาคณิต": "sequence.geometric",
                                 "ลำดับเวียนเกิด": "sequence.patterns", "ลิมิตของลำดับ": "series.sequence-limit",
                                 "การหาลิมิตในรูปเศษส่วน": "series.sequence-limit", "สัญลักษณ์ซิกมา": "series.sigma",
                                 "การหาผลบวกอนุกรมด้วยซิกมา": "series.sigma", "ทบทวนอนุกรมเลขคณิต": "sequence.arithmetic",
                                 "ทบทวนอนุกรมเรขาคณิต": "sequence.geometric",
                                 "อนุกรมเรขาคณิตดัดแปลง": "series.telescoping", "อนุกรมเทเลสโคปิค": "series.telescoping"},
    "🍰 แคลคูลัส": {"ลิมิตของฟังก์ชัน": "calculus.limits-continuity", "ลิมิตซ้าย – ลิมิตขวา": "calculus.limits-continuity",
                   "การหาลิมิตจากกราฟ": "calculus.limits-continuity", "ความต่อเนื่องของฟังก์ชัน": "calculus.limits-continuity",
                   "อัตราการเปลี่ยนแปลงเฉลี่ย": "derivative.rules", "อัตราการเปลี่ยนแปลงขณะใดๆ": "derivative.rules",
                   "อนุพันธ์ของฟังก์ชัน": "derivative.rules", "กฎลูกโซ่": "derivative.composite",
                   "อนุพันธ์ของฟังก์ชันแฝง": "derivative.composite", "อนุพันธ์อันดับสูง": "derivative.rules",
                   "ระยะทาง ความเร็ว ความเร่ง": "derivative.rules", "กฎของโลปิตาล": "calculus.limits-continuity",
                   "ความชันเส้นโค้ง": "calculus.tangent-conditions",
                   "ฟังก์ชันเพิ่ม – ฟังก์ชันลด": "calculus.extrema-basics", "ค่าสูงสุด ต่ำสุด": "calculus.extrema-basics",
                   "ปฏิยานุพันธ์": "calculus.accumulation", "อินทิกรัลจำกัดเขต": "calculus.accumulation",
                   "พื้นที่ที่ปิดล้อมด้วยเส้นโค้ง": "calculus.area-between", "พื้นที่ระหว่างเส้นโค้ง": "calculus.area-between"},
    "สถิติ พื้นฐาน": {"สถิติภาคบรรยาย": "stats.presentation", "ตารางแจกแจงความถี่": "stats.presentation",
                      "ฮิสโทแกรม": "stats.presentation", "แผนภาพลำต้นและใบ": "stats.presentation",
                      "ค่าเฉลี่ยเลขคณิต": "stats.central", "ค่าเฉลี่ยถ่วงน้ำหนัก": "stats.central", "มัธยฐาน": "stats.central",
                      "ฐานนิยม": "stats.central", "เปรียบเทียบค่ากลางแต่ละชนิด": "stats.central",
                      "การวัดตำแหน่งข้อมูล": "stats.position", "พิสัย": "stats.spread", "พิสัยระหว่างควอไทล์": "stats.position",
                      "ส่วนเบี่ยงเบนมาตรฐาน": "stats.spread", "สมบัติของส่วนเบี่ยงเบนมาตรฐาน": "stats.transform-sums",
                      "การวัดการกระจายสัมพัทธ์": "stats.spread", "แผนภาพกล่อง": "stats.position"},
    "🍰 ตัวแปรสุ่ม": {"ตัวแปรสุ่ม": "random.expected-value", "การแจกแจงทวินาม": "random.binomial",
                     "การแจกแจงปกติมาตรฐาน": "random.normal-table", "การแจกแจงปกติ": "random.normal-table"},
    "ตรรกศาสตร์ พื้นฐาน": {"ประพจน์": "logic.connectives", "การเชื่อมประพจน์": "logic.connectives"},
    "ตรรกศาสตร์ เพิ่มเติม": {"ทบทวนพื้นฐาน": "logic.connectives", "ตารางค่าความจริง": "logic.evaluate-compound",
                            "สมมูล": "logic.equivalence", "การทำประพจน์เป็นรูปอย่างง่าย": "logic.equivalence",
                            "สัจนิรันดร์": "logic.tautology", "การอ้างเหตุผล": "logic.tautology",
                            "ตัวบ่งปริมาณ": "logic.quantifier-finite", "นิเสธของตัวบ่งปริมาณ": "logic.negation"},
    "🍰 จำนวนจริง": {"จำนวนชนิดต่างๆ": "real.field-properties", "สมบัติการเท่ากัน": "real.field-properties",
                    "สมบัติการบวกและคูณ": "real.field-properties", "การสร้างเครื่องหมายใหม่": "real.field-properties",
                    "พหุนาม": "real.factoring", "การแยกตัวประกอบพหุนาม": "real.factoring",
                    "การหารสังเคราะห์": "poly.remainder-theorem", "ทฤษฎีเศษ": "poly.remainder-theorem",
                    "การแยกตัวประกอบด้วยทฤษฎีเศษ": "poly.rational-roots", "สมการตัวแปรเดียว": "real.equations",
                    "สมการดีกรีสูง": "poly.rational-roots", "เศษส่วนของพหุนาม": "real.rational-expressions",
                    "สมการเศษส่วนของพหุนาม": "real.rational-expressions", "สมบัติการไม่เท่ากัน": "real.order-properties",
                    "ช่วง": "real.intervals-inequalities", "อสมการตัวแปรเดียว": "real.intervals-inequalities",
                    "ค่าสัมบูรณ์": "abs.definition", "สมการ อสมการ ค่าสัมบูรณ์": "abs.piecewise-equation",
                    "การแบ่งกรณีค่าสัมบูรณ์": "abs.piecewise-equation"},
    "ความสัมพันธ์และฟังก์ชัน พื้นฐาน": {"คู่อันดับ": "function.relation-pairs", "ผลคูณคาร์ทีเซียน": "function.relation-pairs",
                                         "ความสัมพันธ์": "function.relation-pairs", "กราฟของความสัมพันธ์": "function.graph-inequality",
                                         "รูปกราฟที่ควรจำ": "function.graph-inequality", "กราฟของอสมการ": "function.graph-inequality",
                                         "โดเมน และ เรนจ์": "function.domain-range", "โดเมนและเรนจ์ จากกราฟ": "function.domain-range",
                                         "ฟังก์ชัน": "function.is-function", "สัญลักษณ์แทนฟังก์ชัน": "function.is-function",
                                         "ฟังก์ชันกำลังสอง": "quadratic.max-min", "ฟังก์ชันเอกซ์โพเนนเชียล": "function.exponential-models"},
    "ความสัมพันธ์และฟังก์ชัน เพิ่มเติม": {"ทบทวนความสัมพันธ์": "function.relation-pairs",
                                           "โดเมนและเรนจ์ จากการพิจารณาช่วงค่า": "function.domain-range",
                                           "การเลื่อนกราฟ": "function.transformations", "อินเวอร์ส": "function.composition-inverse",
                                           "กราฟของอินเวอร์ส": "function.composition-inverse", "ทบทวนฟังก์ชัน": "function.is-function",
                                           "ประเภทของฟังก์ชัน": "function.is-function", "ฟังก์ชันเพิ่ม - ลด": "function.is-function",
                                           "ฟังก์ชันอินเวอร์ส": "function.composition-inverse",
                                           "บวก ลบ คูณ หาร ฟังก์ชัน": "function.composition-inverse",
                                           "ฟังก์ชันประกอบ": "function.composition-inverse",
                                           "ฟังก์ชันที่วนกลับไปหาตัวเอง": "function.composition-inverse"},
    "🍰 เลขยกกำลัง": {"รากที่ 𝑛": "power.root-signs", "ค่าหลักรากที่ 𝑛": "power.root-signs",
                     "การ บวก ลบ คูณ หาร รูท": "radical.simplify", "รูทสองของจำนวนที่ติดรูท": "radical.denest",
                     "เลขยกกำลัง": "power.laws", "สมการเลขชี้กำลัง": "expeq.same-base", "ดอกเบี้ยทบต้น": "finance.compound"},
    "Expo Log": {"สมการติดรูท": "radical.equations", "รูทไม่รู้จบ": "radical.equations", "เลขยกกำลัง": "power.laws",
                 "ฟังก์ชันเอกซ์โพเนนเชียล": "function.exponential-models", "สมการ อสมการ เอกซ์โพเนนเชียล": "expeq.advanced",
                 "ลอการิทึม": "log.basics", "ฟังก์ชันลอการิทึม": "log.basics", "การหาค่าลอการิทึม": "log.basics",
                 "แอนติลอก": "log.basics", "สมการลอการิทึม": "log.equation-advanced", "อสมการลอการิทึม": "log.inequality"},
    "🍰 ภาคตัดกรวย": {"วงกลม": "circle.basics", "พาราโบลา": "conic.standard-forms", "วงรี": "conic.standard-forms",
                   "ไฮเพอร์โบลา": "conic.standard-forms", "รูปทั่วไปของภาคตัดกรวย": "conic.general-form"},
    "เรขาคณิตวิเคราะห์ 📝": {"ระยะระหว่างจุด": "line.distance-midpoint", "จุดกึ่งกลาง": "line.distance-midpoint",
                             "ความชัน": "line.slope-equation", "สมการกราฟเส้นตรง": "line.slope-equation",
                             "ระยะระหว่างจุดกับเส้นตรง": "line.point-distance", "ระยะระหว่างเส้นขนาน": "line.point-distance"},
    "🍰 เมทริกซ์": {"เมทริกซ์": "matrix.arithmetic", "เมทริกซ์คูณเมทริกซ์": "matrix.arithmetic",
                   "ดีเทอร์มิแนนต์": "matrix.det-properties", "อินเวอร์สการคูณ": "matrix.matrix-equation",
                   "สมการเมทริกซ์": "matrix.matrix-equation", "เมทริกซ์แต่งเติม": "matrix.row-operations",
                   "ระบบสมการเชิงเส้น": "matrix.cramer"},
}
# Existing units that gain covered_by keys because the books show their basics too.
EXTRA_COVER = {
    "math.counting.permutation": ["math.circular_permutation_m5", "math.permutation_identical_m5"],
    "math.probability.classical": ["math.sample_space_m4", "math.event_probability_m4"],
    "math.calculus.area-between": ["math.area_under_curve", "math.area_between_curve_and_line"],
    "math.stats.presentation": ["math.classify_data_type", "math.data_type_classify"],
    "math.random.expected-value": ["math.expected_value", "math.expected_value_table"],
    "math.function.composition-inverse": ["math.function_arithmetic_m4"],
    "math.matrix.det-properties": ["math.determinant_2x2", "math.determinant_3x3_m5"],
    "math.matrix.matrix-equation": ["math.matrix_inverse_m5"],
}

files = {}


def load(name):
    if name not in files:
        files[name] = json.loads((K / name).read_text("utf-8"))
    return files[name]


index = {}
for p in K.glob("*.json"):
    for u in json.loads(p.read_text("utf-8"))["units"]:
        index[u["id"]] = p.name
for uid, (fname, kind, title, statement, extra, cover) in NEW.items():
    d = load(fname)
    if any(u["id"] == uid for u in d["units"]):
        continue
    d["units"].append({"id": uid, "kind": kind, "title": title, "statement": statement, **extra,
                       "sources": [], "covered_by": cover})
    index[uid] = fname

unmapped = []
for frag, sections in MAP.items():
    path = book(frag)
    for title in books[path]:
        if title not in sections:
            unmapped.append((path, title))
    for title, short in sections.items():
        uid = "math." + short
        d = load(index[uid])
        u = next(u for u in d["units"] if u["id"] == uid)
        src = {"sheet": path, "section": title}
        if src not in u["sources"]:
            u["sources"].append(src)
for uid, keys in EXTRA_COVER.items():
    d = load(index[uid])
    u = next(u for u in d["units"] if u["id"] == uid)
    u["covered_by"] += [k for k in keys if k not in u["covered_by"]]
for name, d in files.items():
    (K / name).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
missing = [p for p in books if not any(f in p for f in MAP)]
print("unmapped sections:", unmapped)
print("books without a map:", missing)
