"""Generated diagrams (math and science), drawn the first time they are asked for.

Each family pairs a tuple of specs from the problem sets with the function
in ``otk.pictures`` that draws one. Nothing is committed: a spec's PNG is
drawn into ``otk.pictures._output.output_dir()`` on first request and served
from there afterwards (and from Cloudflare's cache in front of it).

Only ids in this registry are ever drawn, so the set of drawable pictures is
finite and known in advance — a request cannot make the server draw anything
new. To grow a family, grow its spec tuple; nothing else changes.
"""

from __future__ import annotations

import importlib
import threading
from functools import lru_cache
from pathlib import Path

from typing import NamedTuple

from otk.sets._support import math_diagrams as md
from otk.sets._support import math_diagrams_geo as geo
from otk.sets._support import math_diagrams_hi as mhi
from otk.sets.math.p5 import types_of_quadrilaterals as mf
from otk.sets.math.m3 import trigonometric_ratios as mfh
from otk.sets.math.m2.congruence import CONGRUENT_PAIRS
from otk.sets.math.m1.prime_factorisation import FACTOR_TREES
from otk.sets._support import math_measure_pictures as mm
from otk.sets._support import math_pictures as mp
from otk.sets._support import math_pictures_extra as mx
from otk.sets._support import math_pictures_hi as mph
from otk.sets._support import math_pictures_add as ma
from otk.sets._support import math_pictures_p2 as mp2
from otk.sets._support import ms1_diagrams as ms1
from otk.sets._support.circuit_symbols import P6_CIRCUIT_SPECS, SYMBOL_CARDS
from otk.sets.physics.m3.series_and_parallel_circuits import CIRCUIT_SPECS
from otk.sets._support.force_diagrams import ALL_FORCE_DIAGRAM_SPECS
from otk.sets.physics.m3.waves import WAVE_SPECS
from otk.sets._support.science_skills import EXPERIMENT_CHARTS
from otk.sets._support.block_programs import BLOCK_PROGRAM_SPECS
from otk.sets._support.flowcharts import FLOWCHART_SPECS
from otk.sets.chemistry.m2.separating_solutions import APPARATUS_SPECS, CHROMA_SPECS

from ._output import output_dir

_DRAW = "otk.pictures."


class Single(NamedTuple):
    """A one-off drawing with no parameters (the skeleton, the atmosphere profile)."""
    asset_id: str


# (specs, "module:function") — the module under otk.pictures that draws them.
FAMILIES: tuple[tuple[tuple, str], ...] = (
    (md.SHAPES_2D, "math_diagrams:make_shape_2d"),
    (md.SOLIDS, "math_diagrams:make_solid"),
    (md.NETS, "math_diagrams:make_net"),
    (md.CLOCKS, "math_diagrams:make_clock"),
    (md.PROTRACTOR_ANGLES, "math_diagrams:make_protractor"),
    (md.KIND_ANGLES, "math_diagrams:make_angle_kind"),
    (md.FRACTION_PICTURES, "math_diagrams:make_fraction"),
    (md.RECT_FIGURES + md.QUAD_FIGURES + md.TRIANGLE_FIGURES + md.L_FIGURES
     + md.RIGHT_TRIANGLE_FIGURES, "math_diagrams:make_figure"),
    (md.BAR_CHARTS, "math_diagrams:make_bar_chart"),
    (md.LINE_GRAPHS, "math_diagrams:make_line_graph"),
    (md.NUMBER_LINES, "math_diagrams:make_number_line"),
    (md.LINE_FNS, "math_diagrams:make_line_fn"),
    (md.PARABOLAS, "math_diagrams:make_parabola"),
    (mhi.VENNS, "math_diagrams:make_venn"),
    (mhi.SINE_GRAPHS, "math_diagrams:make_sine"),
    (mhi.BOX_PLOTS, "math_diagrams:make_box"),
    (mhi.SCATTERS, "math_diagrams:make_scatter"),
    (mhi.NORMALS, "math_diagrams:make_normal"),
    (geo.LINE_FIGURES, "math_diagrams:make_line_ray"),
    (geo.PARALLEL_FIND + geo.PARALLEL_NAME + geo.PARALLEL_TWO, "math_diagrams:make_parallel"),
    (geo.TRI_ANGLES + geo.TRI_SIDES, "math_diagrams:make_marked_triangle"),
    (geo.PIE_CHARTS, "math_diagrams:make_pie"),
    (geo.TRANSFORMS, "math_diagrams:make_transform"),
    (geo.CIRCLE_ANGLES, "math_diagrams:make_circle_angle"),
    (geo.SIMILAR_PAIRS, "math_diagrams:make_similar"),
    (geo.SYMMETRY_SHAPES, "math_diagrams:make_symmetry"),
    (geo.TANGENTS, "math_diagrams:make_tangent"),
    (geo.CONIC_GRAPHS, "math_diagrams:make_conic"),
    (geo.RIGHT_TRIANGLES, "math_diagrams:make_right_triangle"),
    (mp.ALL_SCENES, "counting_pictures:make_scene"),
    (mp.CROSSED, "counting_pictures:make_crossed"),
    (mp.JOINED, "counting_pictures:make_joined"),
    (mp.HIDDEN, "counting_pictures:make_hidden"),
    (mp.TWO_ROWS, "counting_pictures:make_two_rows"),
    (mp.BUNDLES, "counting_pictures:make_bundles"),
    (mp2.ARRAYS, "counting_pictures:make_array"),
    (mp2.GROUPS, "counting_pictures:make_groups"),
    (mp2.MONEY, "counting_pictures:make_money"),
    (mp2.BLOCKS, "counting_pictures:make_blocks"),
    (mp2.SHADED, "counting_pictures:make_shaded"),
    (mp2.GROWING, "counting_pictures:make_growing"),
    (mm.RULERS, "measure_pictures:make_ruler"),
    (mm.PICTOGRAPHS_P1 + mm.PICTOGRAPHS_P2, "measure_pictures:make_pictograph"),
    (mm.SCALES, "measure_pictures:make_scale"),
    (mm.JUGS, "measure_pictures:make_jug"),
    (mm.CUBES, "measure_pictures:make_cubes"),
    (mx.POLYGON_PICS, "extra_pictures:make_polygon"),
    (mx.BARS, "extra_pictures:make_bars"),
    (mx.GRIDS, "extra_pictures:make_grid"),
    (mx.SPINNERS, "extra_pictures:make_spinner"),
    (mph.AREA_MODELS, "hi_pictures:make_area_model"),
    (mph.BALANCES, "hi_pictures:make_balance"),
    (mph.FRAC_LINES, "hi_pictures:make_frac_line"),
    (mph.DOUBLE_BARS, "hi_pictures:make_double_bars"),
    (mph.DOT_PLOTS, "hi_pictures:make_dot_plot"),
    (mph.HISTOGRAMS, "hi_pictures:make_histogram"),
    (mf.QUAD_PICTURES, "format_pictures:make_quad"),
    (FACTOR_TREES, "format_pictures:make_factor_tree"),
    (CONGRUENT_PAIRS, "format_pictures:make_congruent"),
    (mfh.SPECIAL_TRIANGLES, "format_pictures:make_special_triangle"),
    (ma.QUAD_INEQS, "add_pictures:make_quad_ineq"),
    (ma.ABS_GRAPHS, "add_pictures:make_abs"),
    (ma.CIRCLE_GRIDS, "add_pictures:make_circle"),
    (ma.EXP_LOG_GRAPHS, "add_pictures:make_exp_log"),
    (ma.VECTOR_GRIDS, "add_pictures:make_vectors"),
    (ma.UNIT_POINTS, "add_pictures:make_unit"),
    (ma.COS_TRIANGLES, "add_pictures:make_cos_triangle"),
    (ma.LIMIT_GRAPHS, "add_pictures:make_limit"),
    (ma.DERIV_CURVES, "add_pictures:make_deriv"),
    (ma.AREA_REGIONS, "add_pictures:make_area"),
    # Science: otk/pictures/generate.py
    ((Single("skeleton"),), "generate:make_skeleton"),
    ((Single(ms1.ATMOSPHERE_ASSET),), "generate:make_atmosphere_profile"),
    (tuple(WAVE_SPECS), "generate:make_wave"),
    (tuple(CIRCUIT_SPECS), "generate:make_circuit"),
    (tuple(SYMBOL_CARDS), "generate:make_p6_symbol_card"),
    (tuple(P6_CIRCUIT_SPECS), "generate:make_p6_circuit"),
    (ms1.HEATING_CURVES, "generate:make_heating_curve"),
    (ms1.THERMOMETERS, "generate:make_thermometer"),
    (ms1.WEATHER_CHARTS, "generate:make_weather_chart"),
    (ms1.HEAT_SCENES, "generate:make_heat_scene"),
    (EXPERIMENT_CHARTS, "generate:make_experiment_chart"),
    (tuple(CHROMA_SPECS), "generate:make_chromatogram"),
    (tuple(APPARATUS_SPECS), "generate:make_apparatus"),
    (tuple(ALL_FORCE_DIAGRAM_SPECS), "generate:make_force_diagram"),
    # Technology: วิทยาการคำนวณ block programs (Phase 7 wave T3)
    (BLOCK_PROGRAM_SPECS, "generate:make_block_program"),
    (FLOWCHART_SPECS, "generate:make_flowchart"),
)

# pyplot keeps global state; one drawing at a time. Drawing is rare — each
# picture is drawn once per container — so this never becomes a queue.
_LOCK = threading.Lock()


@lru_cache(maxsize=1)
def registry() -> dict[str, tuple[object, str]]:
    """asset id -> (spec, "module:function")."""
    out: dict[str, tuple[object, str]] = {}
    for specs, drawer in FAMILIES:
        for spec in specs:
            out.setdefault(spec.asset_id, (spec, drawer))
    return out


def knows(asset_id: str) -> bool:
    return asset_id in registry()


def diagram_path(asset_id: str) -> Path | None:
    """The PNG for a generated diagram, drawing it first if needed; None if unknown."""
    entry = registry().get(asset_id)
    if entry is None:
        return None
    path = output_dir() / f"{asset_id}.png"
    if path.is_file():
        return path
    spec, drawer = entry
    module, func = drawer.split(":")
    draw = getattr(importlib.import_module(_DRAW + module), func)
    with _LOCK:
        if not path.is_file():
            draw(spec)
    return path
