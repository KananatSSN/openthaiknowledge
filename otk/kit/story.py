"""Shared material for Thai โจทย์ปัญหา: people, things and how to count them.

A word-problem set that owns one sentence teaches the sentence, not the
operation: after a few items a learner answers "แก้วมีลูกอม … แม่ให้เพิ่มอีก …"
by pattern. The สสวท. books vary three things — the *situation* (giving,
buying, birds landing), the *structure* (result, change or start unknown;
comparison) and the *things counted* — and these helpers let a set vary all
three without each module re-inventing its own list of names and classifiers.

Nothing here registers a type. Everything takes the caller's ``rng``, so a
worksheet stays reproducible from its seed.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

# Nicknames, not formal names: the books use short given names, and none of
# these reads as a single gender in a way a sentence below depends on.
NAMES = (
    "ต้นกล้า", "ใบเตย", "ภูผา", "น้ำฝน", "ข้าวปั้น", "มะปราง", "ก้องภพ",
    "แพรวา", "ธันวา", "ขวัญข้าว", "ปลายฟ้า", "ภูมิ", "นะโม", "ใบบัว",
    "ตะวัน", "ชมพู่", "ปันปัน", "กะทิ",
)

# Who hands something over in a "ได้เพิ่ม" story.
GIVERS = ("แม่", "พ่อ", "คุณยาย", "คุณตา", "คุณครู", "พี่ชาย", "พี่สาว", "ลุง", "ป้า")


class Thing(NamedTuple):
    """Something a child owns and counts, with its ลักษณนาม."""
    noun: str
    cl: str


THINGS = (
    Thing("ลูกอม", "เม็ด"), Thing("ลูกแก้ว", "ลูก"), Thing("ดินสอ", "แท่ง"),
    Thing("สมุด", "เล่ม"), Thing("หนังสือนิทาน", "เล่ม"), Thing("สติกเกอร์", "แผ่น"),
    Thing("ดอกไม้", "ดอก"), Thing("ลูกโป่ง", "ลูก"), Thing("รถของเล่น", "คัน"),
    Thing("ตุ๊กตา", "ตัว"), Thing("คุกกี้", "ชิ้น"), Thing("ยางลบ", "ก้อน"),
    Thing("ปากกา", "ด้าม"), Thing("กระดาษสี", "แผ่น"), Thing("แสตมป์", "ดวง"),
    Thing("การ์ดสะสม", "ใบ"), Thing("ส้ม", "ผล"), Thing("มะม่วง", "ผล"),
    Thing("ไข่ไก่", "ฟอง"), Thing("ขนมปัง", "ชิ้น"),
)

# Things that get used up, each with the verb that uses it: "กินไป", "ใช้ไป".
CONSUMABLES = (
    (Thing("ลูกอม", "เม็ด"), "กินไป"), (Thing("คุกกี้", "ชิ้น"), "กินไป"),
    (Thing("ขนมปัง", "ชิ้น"), "กินไป"), (Thing("ส้ม", "ผล"), "กินไป"),
    (Thing("กล้วย", "ผล"), "กินไป"), (Thing("กระดาษสี", "แผ่น"), "ใช้ไป"),
    (Thing("สติกเกอร์", "แผ่น"), "ใช้ติดสมุดไป"), (Thing("ดินสอสี", "แท่ง"), "ทำหายไป"),
)

# Things a shop sells by the piece.
STOCK = (
    Thing("ไข่ไก่", "ฟอง"), Thing("ขนมครก", "ถ้วย"), Thing("ส้ม", "ผล"),
    Thing("สมุด", "เล่ม"), Thing("ดินสอ", "แท่ง"), Thing("ลูกโป่ง", "ลูก"),
    Thing("ขนมปัง", "ก้อน"), Thing("แก้วน้ำ", "ใบ"), Thing("ต้นกล้า", "ต้น"),
)

# Coloured pairs for "สีแดงกับสีฟ้ารวมกัน" part–whole stories.
COLOURS = ("สีแดง", "สีฟ้า", "สีเขียว", "สีเหลือง", "สีชมพู", "สีม่วง", "สีส้ม")


class Scene(NamedTuple):
    """Animals somewhere, arriving and leaving: "บนต้นไม้มีนก …"."""
    place: str
    animal: str
    arrive: str
    leave: str


SCENES = (
    Scene("บนต้นไม้", "นก", "บินมาเกาะเพิ่มอีก", "บินจากไป"),
    Scene("ในบ่อ", "เป็ด", "เดินลงมาเล่นน้ำเพิ่มอีก", "เดินขึ้นจากบ่อไป"),
    Scene("ในเล้า", "ไก่", "เดินเข้ามาเพิ่มอีก", "เดินออกไป"),
    Scene("ในสวน", "ผีเสื้อ", "บินมาเพิ่มอีก", "บินหนีไป"),
    Scene("บนสนามหญ้า", "นกพิราบ", "บินลงมาเพิ่มอีก", "บินขึ้นไป"),
    Scene("บนใบบัว", "กบ", "กระโดดขึ้นมาเพิ่มอีก", "กระโดดลงน้ำไป"),
)

# Small things a child might buy, priced low enough for ป.1–ป.2.
SNACKS = ("ขนม", "นม", "ไอศกรีม", "น้ำผลไม้", "ขนมปัง", "ผลไม้")
TOYS = ("ตุ๊กตา", "รถของเล่น", "ลูกบอล", "ว่าว", "หุ่นยนต์ของเล่น", "จักรยาน")

THAI_DIGITS = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")

_DIGIT_WORDS = ("ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า")
_PLACE_WORDS = ("", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน")


def names(rng: Random, k: int = 2) -> list[str]:
    """``k`` distinct names."""
    return rng.sample(NAMES, k)


def thai_numeral(n: int) -> str:
    """12 -> ๑๒."""
    return str(n).translate(THAI_DIGITS)


def _below_million(n: int, *, has_higher: bool) -> str:
    out = ""
    digits = str(n)
    for i, ch in enumerate(digits):
        d, pos = int(ch), len(digits) - 1 - i
        if d == 0:
            continue
        if pos == 1:
            out += "สิบ" if d == 1 else "ยี่สิบ" if d == 2 else _DIGIT_WORDS[d] + "สิบ"
        elif pos == 0:
            # เอ็ด whenever a higher place is filled: สิบเอ็ด, หนึ่งร้อยเอ็ด.
            out += "เอ็ด" if d == 1 and (has_higher or n >= 10) else _DIGIT_WORDS[d]
        else:
            out += _DIGIT_WORDS[d] + _PLACE_WORDS[pos]
    return out


def thai_words(n: int) -> str:
    """How a whole number is read in Thai: 21 -> ยี่สิบเอ็ด, 1005 -> หนึ่งพันห้า."""
    if n < 0:
        raise ValueError("negative numbers are not read by this helper")
    if n == 0:
        return "ศูนย์"
    if n >= 1_000_000:
        high, low = divmod(n, 1_000_000)
        return thai_words(high) + "ล้าน" + (_below_million(low, has_higher=True) if low else "")
    return _below_million(n, has_higher=False)


def keep(*values: int, answer: int | None = None, lo: int = 0,
         hi: int | None = None) -> list[str]:
    """Distractor strings: drop duplicates, the answer, and anything outside
    ``lo``..``hi``.

    Hand-picked mistakes are listed most diagnostic first — the staged
    foundation set keeps only the first one.
    """
    out: list[str] = []
    for v in values:
        if v < lo or (hi is not None and v > hi) or v == answer or str(v) in out:
            continue
        out.append(str(v))
    return out


# ── Pictographs (แผนภูมิรูปภาพ) ──────────────────────────────────────────────

class Chart(NamedTuple):
    """One pictograph theme. ``label`` names a row's amount in a question
    ("นักเรียนที่ชอบ{c}"); ``most`` asks which row is largest or smallest."""
    title: str
    rows: tuple[str, ...]
    symbol_means: str
    unit: str
    label: str
    most: str


_CHARTS = (
    Chart("ผลไม้ที่นักเรียนชอบ", ("ส้ม", "มะม่วง", "กล้วย", "แตงโม", "ทุเรียน"),
          "นักเรียน", "คน", "นักเรียนที่ชอบ{c}", "ผลไม้ใดมีนักเรียนชอบ{most}"),
    Chart("สัตว์เลี้ยงของนักเรียนห้องหนึ่ง", ("สุนัข", "แมว", "ปลา", "กระต่าย", "นก"),
          "สัตว์เลี้ยง", "ตัว", "{c}", "สัตว์เลี้ยงชนิดใดมีจำนวน{most}"),
    Chart("จำนวนหนังสือที่ห้องสมุดให้ยืมในแต่ละวัน",
          ("วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์"),
          "หนังสือ", "เล่ม", "หนังสือที่ให้ยืม{c}", "วันใดห้องสมุดให้ยืมหนังสือ{most}"),
    Chart("กีฬาที่นักเรียนชอบ", ("ฟุตบอล", "ว่ายน้ำ", "แบดมินตัน", "วิ่ง", "ปิงปอง"),
          "นักเรียน", "คน", "นักเรียนที่ชอบ{c}", "กีฬาใดมีนักเรียนชอบ{most}"),
    Chart("จำนวนต้นไม้ดอกที่ปลูกในสวน",
          ("กุหลาบ", "มะลิ", "ดาวเรือง", "ทานตะวัน", "ชบา"),
          "ต้นไม้ดอก", "ต้น", "ต้น{c}", "ต้นไม้ดอกชนิดใดปลูกไว้{most}"),
    Chart("สีที่นักเรียนชอบ", ("สีแดง", "สีฟ้า", "สีเขียว", "สีเหลือง", "สีชมพู"),
          "นักเรียน", "คน", "นักเรียนที่ชอบ{c}", "สีใดมีนักเรียนชอบ{most}"),
)


class Pictograph(NamedTuple):
    text: str
    data: dict
    chart: Chart

    def label(self, row: str) -> str:
        return self.chart.label.format(c=row)


def pictograph(rng: Random, key: int = 1, lo: int = 1, hi: int = 9,
               rows: int = 4) -> Pictograph:
    """A text pictograph where each ● stands for ``key`` of the unit.

    Each row draws ``amount // key`` symbols, so every amount is a multiple of
    ``key`` and no row needs a part symbol.
    """
    chart = rng.choice(_CHARTS)
    picked = set(rng.sample(chart.rows, rows))
    chosen = [r for r in chart.rows if r in picked]      # keep the chart's order
    counts = rng.sample(range(lo, hi + 1), rows)
    data = {c: n * key for c, n in zip(chosen, counts)}
    lines = [f"แผนภูมิรูปภาพแสดง{chart.title}"]
    lines += [f"{c}:  " + " ".join("●" * (n // key)) for c, n in data.items()]
    lines.append(f"กำหนดให้ ● แทน{chart.symbol_means} {key} {chart.unit}")
    return Pictograph("\n".join(lines), data, chart)


def bar_chart(rng: Random, scale: int = 10, lo: int = 2, hi: int = 12,
              rows: int = 4) -> Pictograph:
    """A text bar chart: each row a bar of ■ cells, one cell per ``scale``.

    Same themes and shape as :func:`pictograph`; the bars are drawn solid and
    the scale is stated the way a แผนภูมิแท่ง's axis would give it.
    """
    chart = rng.choice(_CHARTS)
    picked = set(rng.sample(chart.rows, rows))
    chosen = [r for r in chart.rows if r in picked]
    counts = rng.sample(range(lo, hi + 1), rows)
    data = {c: n * scale for c, n in zip(chosen, counts)}
    lines = [f"แผนภูมิแท่งแสดง{chart.title}"]
    lines += [f"{c}:  " + "■" * (n // scale) for c, n in data.items()]
    lines.append(f"ความยาวของแท่ง 1 ช่อง ■ แทน{chart.symbol_means} {scale} {chart.unit}")
    return Pictograph("\n".join(lines), data, chart)


# ── ตารางทางเดียว ─────────────────────────────────────────────────────────────

class Table(NamedTuple):
    """One one-way table theme: its title, the row heading, the rows, the
    count's heading and unit, how a question asks which row is largest, and
    how a question names one row ("ห้อง {r}")."""
    title: str
    heading: str
    rows: tuple[str, ...]
    count: str
    unit: str
    most: str
    label: str = "{r}"


TABLES = (
    Table("จำนวนนักเรียนที่เลือกเข้าชมรม", "ชมรม",
          ("ดนตรี", "กีฬา", "ศิลปะ", "วิทยาศาสตร์", "หุ่นยนต์"), "จำนวนนักเรียน", "คน",
          "ชมรมใดมีนักเรียน{most}", "ชมรม{r}"),
    Table("จำนวนขวดพลาสติกที่แต่ละห้องเก็บได้", "ห้อง",
          ("ป.3/1", "ป.3/2", "ป.3/3", "ป.3/4", "ป.3/5"), "จำนวนขวด", "ใบ",
          "ห้องใดเก็บขวดได้{most}", "ห้อง {r} "),
    Table("ผลไม้ที่ร้านค้าขายได้ในหนึ่งวัน", "ผลไม้",
          ("มังคุด", "เงาะ", "ลำไย", "มะม่วง", "ส้มโอ"), "น้ำหนัก", "กิโลกรัม",
          "ผลไม้ใดขายได้{most}"),
    Table("จำนวนผู้เข้าชมพิพิธภัณฑ์", "วัน",
          ("วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์"), "จำนวนผู้เข้าชม",
          "คน", "วันใดมีผู้เข้าชม{most}"),
    Table("จำนวนต้นไม้ที่ปลูกในโครงการรักษ์โลก", "หมู่บ้าน",
          ("หมู่ 1", "หมู่ 2", "หมู่ 3", "หมู่ 4", "หมู่ 5"), "จำนวนต้นไม้", "ต้น",
          "หมู่บ้านใดปลูกต้นไม้{most}", "{r} "),
)


class OneWayTable(NamedTuple):
    text: str
    data: dict
    table: Table


def one_way_table(rng: Random, lo: int = 12, hi: int = 250, rows: int = 4) -> OneWayTable:
    """A ตารางทางเดียว as text rows, distinct counts, in the theme's order."""
    table = rng.choice(TABLES)
    picked = set(rng.sample(table.rows, rows))
    chosen = [r for r in table.rows if r in picked]
    data = dict(zip(chosen, rng.sample(range(lo, hi + 1), rows)))
    lines = [f"ตารางแสดง{table.title}",
             f"{table.heading} | {table.count} ({table.unit})"]
    lines += [f"{r} | {n}" for r, n in data.items()]
    return OneWayTable("\n".join(lines), data, table)
