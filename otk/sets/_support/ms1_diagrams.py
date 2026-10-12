"""Drawn diagrams for ม.1 ความร้อน and ลมฟ้าอากาศ.

Fifty-one sets cover ``ว 2.1 ม.1/9-10``, ``ว 2.2 ม.1/1``, ``ว 2.3 ม.1/1-7`` and
``ว 3.2 ม.1/1-7``, and before this module not one of them showed a picture —
including three whose own display names promise one:

* ``phys.heat_quantity_foundation`` — "แปลความหมายกราฟอุณหภูมิกับเวลา", with the
  graph described in a sentence;
* ``phys.thermometer_fluency`` — "อ่านค่าอุณหภูมิจากสเกลเทอร์มอมิเตอร์", with the
  reading stated in the stem it was meant to be read from;
* ``geo.atmosphere_layers_foundation`` — "จากแบบจำลอง", with the model's four
  data points listed as prose.

Five spec families, one drawing each:

``HeatingCurveSpec``      กราฟอุณหภูมิ-เวลา with a plateau at a change of state
``ThermometerSpec``       a scale with a liquid column standing at one reading
``ATMOSPHERE``            temperature against altitude, the four layers marked
``WeatherChartSpec``      a simple pressure chart — H, L, and labelled isobars
``HeatSceneSpec``         conduction, convection or radiation, drawn as a scene

Nothing Thai is drawn into a PNG: the bundled matplotlib font (DejaVu Sans) has
no Thai glyphs. Every label here is a number, a unit in ASCII, or one of the
letters ``H``/``L`` that a pressure chart uses worldwide. The Thai lives in the
stem, the choices and the alt text — the rule ``CIRCUIT_SPECS``,
``ALL_FORCE_DIAGRAM_SPECS`` and ``circuit_symbols`` all follow.

**Alt text.** As in ``circuit_symbols``, a set whose answer *is* the reading may
not state that reading in its alt text — it would answer itself for a screen
reader and in a printed worksheet, where an image renders as its alt text alone.
Each family therefore has a ``*_alt`` that describes the drawing's shape and
axes, and stops short of the value being asked for.
"""

from __future__ import annotations

from typing import NamedTuple

# ── กราฟอุณหภูมิ-เวลา (ว 2.1 ม.1/10, ว 2.3 ม.1/1) ────────────────────────────

class HeatingCurveSpec(NamedTuple):
    """A substance heated steadily: it warms, holds still, then warms again.

    The flat stretch is the change of state — heat still goes in, temperature
    does not rise, because the energy is spent separating the particles. Every
    minute and degree here is whole so a student reads values off the grid
    rather than estimating between lines.
    """
    start: int          # อุณหภูมิเริ่มต้น (°C)
    warm_to: int        # minutes of heating before the plateau
    plateau: int        # อุณหภูมิขณะเปลี่ยนสถานะ (°C)
    hold: int           # minutes the temperature stays at ``plateau``
    end: int            # อุณหภูมิสุดท้าย (°C)
    after: int          # minutes of heating after the plateau
    change: str         # "หลอมเหลว" | "เดือด"

    @property
    def asset_id(self) -> str:
        return (f"hcurve_{self.start}_{self.warm_to}_{self.plateau}_"
                f"{self.hold}_{self.end}_{self.after}")

    @property
    def plateau_start(self) -> int:
        return self.warm_to

    @property
    def plateau_end(self) -> int:
        return self.warm_to + self.hold

    @property
    def total(self) -> int:
        return self.warm_to + self.hold + self.after


HEATING_CURVES = tuple(HeatingCurveSpec(*t) for t in (
    # Wave H: every minute count stays even, on the drawn two-minute grid, and
    # every plateau sits on a multiple of 20 °C, on the drawn temperature grid.
    (-30, 6, 0, 4, 40, 6, "หลอมเหลว"),
    (-20, 2, 0, 10, 20, 4, "หลอมเหลว"),
    (-10, 4, 0, 6, 40, 8, "หลอมเหลว"),
    (0, 4, 40, 6, 80, 6, "หลอมเหลว"),
    (10, 6, 60, 8, 100, 4, "หลอมเหลว"),
    (20, 4, 80, 8, 120, 6, "เดือด"),
    (40, 6, 100, 6, 120, 4, "เดือด"),
    (20, 10, 100, 4, 140, 8, "เดือด"),
    (-20, 8, 20, 6, 60, 6, "หลอมเหลว"),
    (40, 6, 80, 10, 120, 4, "เดือด"),
    (-20, 4, 0, 6, 40, 8, "หลอมเหลว"),
    (-10, 2, 0, 8, 50, 10, "หลอมเหลว"),
    (10, 6, 80, 4, 120, 6, "เดือด"),
    (20, 8, 100, 10, 140, 6, "เดือด"),
    (0, 5, 60, 5, 100, 10, "หลอมเหลว"),
    (30, 4, 100, 12, 130, 4, "เดือด"),
))


def heating_curve_alt(spec: HeatingCurveSpec) -> str:
    """Names the axes and that there is a flat stretch, never what it means."""
    return ("กราฟเส้นแสดงอุณหภูมิ (องศาเซลเซียส) บนแกนตั้ง กับเวลา (นาที) บนแกนนอน "
            "ขณะให้ความร้อนแก่สารอย่างต่อเนื่อง เส้นกราฟไต่ขึ้น แล้วราบไปช่วงหนึ่ง "
            "จากนั้นไต่ขึ้นต่อ")


# ── เทอร์มอมิเตอร์ (ว 2.3 ม.1/2) ─────────────────────────────────────────────

class ThermometerSpec(NamedTuple):
    """A liquid column standing at one reading on a numbered Celsius scale.

    ``step`` is the value of one small division. It varies on purpose: a student
    who has only ever read a scale of ones will count divisions instead of
    reading them, and get a scale of twos or fives wrong every time.
    """
    reading: int
    lo: int
    hi: int
    step: int           # องศาต่อหนึ่งขีดเล็ก
    label_every: int    # ขีดที่มีตัวเลขกำกับ

    @property
    def asset_id(self) -> str:
        return f"thermo_{self.reading}_{self.lo}_{self.hi}_{self.step}"


THERMOMETERS = tuple(ThermometerSpec(*t) for t in (
    (24, 0, 50, 1, 10),
    (37, 0, 50, 1, 10),
    (46, 0, 50, 1, 10),
    (68, 0, 100, 2, 20),
    (84, 0, 100, 2, 20),
    (36, 0, 100, 2, 20),
    (55, -20, 120, 5, 20),
    (90, -20, 120, 5, 20),
    (-10, -20, 120, 5, 20),
    (15, -20, 120, 5, 20),
    # Wave H: more readings on the same scales, and a scale of twos labelled every ten.
    (12, 0, 50, 1, 10),
    (29, 0, 50, 1, 10),
    (33, 0, 50, 1, 10),
    (41, 0, 50, 1, 10),
    (18, 0, 50, 1, 10),
    (22, 0, 100, 2, 20),
    (48, 0, 100, 2, 20),
    (56, 0, 100, 2, 20),
    (74, 0, 100, 2, 20),
    (92, 0, 100, 2, 20),
    (25, -20, 120, 5, 20),
    (40, -20, 120, 5, 20),
    (65, -20, 120, 5, 20),
    (105, -20, 120, 5, 20),
    (-5, -20, 120, 5, 20),
    (4, -10, 110, 2, 10),
    (26, -10, 110, 2, 10),
    (58, -10, 110, 2, 10),
    (96, -10, 110, 2, 10),
    (-6, -10, 110, 2, 10),
))


# The drawing is 4 inches tall at 100 dpi, and the scale takes about 360 px of
# that once the bulb is below it. Two choices closer than this on the drawing
# cannot be told apart on a phone, so no two options may be nearer than it.
SCALE_PX = 360
MIN_OPTION_PX = 15


def min_option_gap(spec: ThermometerSpec) -> int:
    """The smallest gap in degrees two choices may have: at least 15 px apart, whole divisions."""
    px_per_degree = SCALE_PX / ((spec.hi - spec.lo) * 1.1)
    degrees = -(-MIN_OPTION_PX // px_per_degree)
    return int(-(-degrees // spec.step) * spec.step)


def thermometer_wrongs(spec: ThermometerSpec) -> tuple[int, ...]:
    """Three wrong readings, each a real slip, all far enough apart to see.

    The named mistakes come first — counting divisions as degrees, stopping at
    the labelled tick below, reading the tick above — and are kept only when
    they sit at least ``min_option_gap`` from the answer and from each other.
    The rest are whole gaps above and below the column, inside the scale.
    """
    gap = min_option_gap(spec)
    below = spec.reading - spec.reading % spec.label_every
    candidates = [below + (spec.reading - below) // spec.step, below, below + spec.label_every]
    candidates += [spec.reading + sign * gap * k for k in range(1, 6) for sign in (1, -1)]
    chosen: list[int] = []
    for value in candidates:
        if not spec.lo <= value <= spec.hi:
            continue
        if all(abs(value - other) >= gap for other in (spec.reading, *chosen)):
            chosen.append(value)
        if len(chosen) == 3:
            break
    return tuple(chosen)


def thermometer_alt(spec: ThermometerSpec) -> str:
    """Describes the instrument and its scale, never where the column stands."""
    return (f"ภาพเทอร์มอมิเตอร์แบบของเหลวในหลอดแก้ว มีสเกลองศาเซลเซียสตั้งแต่ "
            f"{spec.lo} ถึง {spec.hi} ขีดเล็กหนึ่งขีดเท่ากับ {spec.step} องศาเซลเซียส "
            f"และมีตัวเลขกำกับทุก {spec.label_every} องศาเซลเซียส "
            f"ของเหลวสีแดงในหลอดสูงขึ้นมาถึงระดับหนึ่ง")


# ── ชั้นบรรยากาศ (ว 3.2 ม.1/1) ───────────────────────────────────────────────

class AtmosphereLayer(NamedTuple):
    name: str           # ชื่อชั้นบรรยากาศ
    base_km: int
    top_km: int
    base_c: int
    top_c: int
    trend: str          # "ลดลง" | "เพิ่มขึ้น"


# The real profile, so there is one drawing rather than a pool: these altitudes
# and temperatures are physical facts, not constants a generator may redraw.
ATMOSPHERE = (
    AtmosphereLayer("โทรโพสเฟียร์", 0, 10, 15, -55, "ลดลง"),
    AtmosphereLayer("สตราโตสเฟียร์", 10, 50, -55, 0, "เพิ่มขึ้น"),
    AtmosphereLayer("มีโซสเฟียร์", 50, 80, 0, -90, "ลดลง"),
    AtmosphereLayer("เทอร์โมสเฟียร์", 80, 500, -90, 1000, "เพิ่มขึ้น"),
)

ATMOSPHERE_ASSET = "atmosphere_profile"

ATMOSPHERE_ALT = (
    "กราฟแสดงอุณหภูมิ (องศาเซลเซียส) บนแกนนอน กับความสูงจากผิวโลก (กิโลเมตร) บนแกนตั้ง "
    "เส้นกราฟหักกลับไปมาสี่ช่วง และมีเส้นประขวางคั่นระหว่างช่วงที่ความสูง 10, 50 และ 80 "
    "กิโลเมตร โดยกำกับชั้นบรรยากาศไว้ที่ขอบขวาเป็นเลข 1 ถึง 4 จากล่างขึ้นบน"
)

#: The numbers drawn beside each layer, so a question can name a layer without
#: printing Thai into the picture.
LAYER_NUMBERS = {layer.name: index + 1 for index, layer in enumerate(ATMOSPHERE)}


# ── แผนที่อากาศอย่างง่าย (ว 3.2 ม.1/4) ────────────────────────────────────────

class WeatherChartSpec(NamedTuple):
    """A pressure chart: one high, one low, and isobars labelled in hPa.

    ``high_side`` says which side of the chart the H sits on, so the direction
    the wind blows (always from H towards L) is not the same answer every time.
    """
    high_hpa: int
    low_hpa: int
    high_side: str      # "left" | "right"

    @property
    def asset_id(self) -> str:
        return f"wxchart_{self.high_hpa}_{self.low_hpa}_{self.high_side[0]}"

    @property
    def low_side(self) -> str:
        return "right" if self.high_side == "left" else "left"

    @property
    def difference(self) -> int:
        return self.high_hpa - self.low_hpa


WEATHER_CHARTS = tuple(WeatherChartSpec(*t) for t in (
    (1020, 1004, "left"),
    (1024, 1008, "right"),
    (1016, 1000, "left"),
    (1028, 1012, "right"),
    (1020, 996, "right"),
    (1012, 1000, "left"),
))

SIDE_WORDS = {"left": "ซ้าย", "right": "ขวา"}


def weather_chart_alt(spec: WeatherChartSpec) -> str:
    """Names the chart's parts without saying which centre is which."""
    return ("แผนที่อากาศอย่างง่าย แสดงศูนย์กลางความกดอากาศสองแห่ง "
            "แห่งหนึ่งกำกับด้วยอักษร H อีกแห่งกำกับด้วยอักษร L "
            "ล้อมรอบด้วยเส้นความกดอากาศเท่าที่มีตัวเลขหน่วยเฮกโตพาสคัลกำกับ")


# ── การถ่ายโอนความร้อน (ว 2.3 ม.1/6) ──────────────────────────────────────────

class HeatSceneSpec(NamedTuple):
    """One drawn scene showing heat moving one of the three ways.

    ``through`` is what the heat crosses, and it is what separates the three:
    a solid that stays put (การนำ), a fluid that circulates (การพา), or nothing
    at all (การแผ่รังสี).
    """
    mode: str           # "conduction" | "convection" | "radiation"
    scene: str          # "bar" | "pot" | "room" | "spoon" | "fire" | "sun"

    @property
    def asset_id(self) -> str:
        return f"heatmode_{self.scene}"

    @property
    def thai_mode(self) -> str:
        return {"conduction": "การนำความร้อน",
                "convection": "การพาความร้อน",
                "radiation": "การแผ่รังสีความร้อน"}[self.mode]

    @property
    def because(self) -> str:
        return {
            "conduction": "ความร้อนถ่ายโอนผ่านการสั่นและชนกันของอนุภาคในของแข็ง โดยอนุภาคไม่เคลื่อนย้ายตำแหน่ง",
            "convection": "อนุภาคของของไหลที่ได้รับความร้อนเคลื่อนที่พาความร้อนไปด้วย เกิดเป็นการหมุนเวียน",
            "radiation": "ความร้อนถ่ายโอนออกมาเป็นรังสีโดยไม่ต้องอาศัยตัวกลาง",
        }[self.mode]


HEAT_SCENES = tuple(HeatSceneSpec(*t) for t in (
    ("conduction", "bar"),      # a rod in a flame, heat creeping along it
    ("conduction", "spoon"),    # a spoon standing in a hot drink
    ("convection", "pot"),      # water circulating in a pan on a hob
    ("convection", "room"),     # warm air rising from a heater, cool air back
    ("radiation", "fire"),      # a person beside a fire, nothing in between
    ("radiation", "sun"),       # the sun warming the ground across empty space
    ("conduction", "pan"),      # a frying pan on a flame, heat along the handle
    ("convection", "tank"),     # water circulating in a tank heated at one corner
    ("radiation", "lamp"),      # a heat lamp warming a tray below, nothing between
))

MODE_LABELS = ("การนำความร้อน", "การพาความร้อน", "การแผ่รังสีความร้อน")


def heat_scene_alt(spec: HeatSceneSpec) -> str:
    """Describes what is drawn, never which of the three modes it is."""
    return {
        "bar": "ภาพแท่งโลหะตัน ปลายซ้ายอยู่ในเปลวไฟ มีลูกศรเรียงไปตามเนื้อแท่งโลหะจากปลายที่ร้อนไปยังปลายที่มือจับ",
        "spoon": "ภาพช้อนโลหะตั้งอยู่ในแก้วเครื่องดื่มร้อน มีลูกศรเรียงขึ้นไปตามด้ามช้อนจากส่วนที่จมอยู่ไปยังส่วนที่โผล่พ้นขอบแก้ว",
        "pot": "ภาพหม้อน้ำบนเตา มีลูกศรวนเป็นวงในเนื้อน้ำ ขึ้นตรงกลางเหนือเปลวไฟและลงที่ข้างหม้อ",
        "room": "ภาพห้องที่มีเครื่องทำความร้อนอยู่ริมผนัง มีลูกศรวนเป็นวงในอากาศ ลอยขึ้นเหนือเครื่องและวกกลับลงมาที่ผนังตรงข้าม",
        "fire": "ภาพคนยืนห่างจากกองไฟ ระหว่างคนกับกองไฟไม่มีสิ่งใดคั่น มีลูกศรพุ่งเป็นเส้นตรงจากกองไฟออกไปทุกทิศรวมทั้งทางคนผู้นั้น",
        "sun": "ภาพดวงอาทิตย์กับผิวโลก ระหว่างทั้งสองเป็นอวกาศที่ว่างเปล่า มีลูกศรพุ่งเป็นเส้นตรงจากดวงอาทิตย์มายังผิวโลก",
        "pan": "ภาพกระทะโลหะวางบนเปลวไฟ มีลูกศรเรียงไปตามด้ามกระทะจากตัวกระทะไปยังปลายด้าม",
        "tank": "ภาพถังน้ำที่มีขดลวดร้อนอยู่มุมล่าง มีลูกศรวนเป็นวงในเนื้อน้ำ ขึ้นเหนือขดลวดและวกลงที่ผนังอีกด้าน",
        "lamp": "ภาพโคมไฟดวงหนึ่งแขวนอยู่เหนือถาด ระหว่างโคมกับถาดไม่มีสิ่งใดคั่น มีลูกศรพุ่งเป็นเส้นตรงจากโคมลงมายังถาด",
    }[spec.scene]


# ── shared ───────────────────────────────────────────────────────────────────

ALL_MS1_SPECS = (*HEATING_CURVES, *THERMOMETERS, *WEATHER_CHARTS, *HEAT_SCENES)


def diagram_question(asset_id: str, alt: str, *, stem: str, correct: str,
                     wrongs: tuple[str, ...], hint: str, topic: str):
    """A question whose stem *shows* the drawing, then asks in Thai."""
    from otk.core.content import image, text
    from otk.core.distractors import label_pool
    from otk.core.question import GeneratedQuestion

    return GeneratedQuestion(
        stem=[image(asset_id, alt=alt), text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )
