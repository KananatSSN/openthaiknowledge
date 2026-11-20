"""MC13 figure: heating curve at constant pressure, temperature against time: A-B rises (solid), B-C flat at the lower temperature (melting), C-D rises (liquid), D-E flat at the higher temperature (boiling), E-F rises (vapour). Melting is BC (answer 4). Returns the segment for a named process."""

SEGMENTS = ("AB", "BC", "CD", "DE", "EF")
PROCESSES = ("solid_warming", "melting", "liquid_warming", "boiling", "vapour_warming")


def solve(process="melting"):
    return SEGMENTS[PROCESSES.index(process)]


def check(process="melting"):
    # Rebuild the curve as (start, end) temperatures; flat segments are phase
    # changes, the lower flat one melts and the higher one boils; a rising
    # segment's phase follows from which flats it lies between.
    curve = {"AB": (-20, 0), "BC": (0, 0), "CD": (0, 100), "DE": (100, 100), "EF": (100, 130)}
    flats = sorted((t0, name) for name, (t0, t1) in curve.items() if t0 == t1)
    melt, boil = flats[0][1], flats[1][1]
    if process == "melting":
        return melt
    if process == "boiling":
        return boil
    lo_melt, lo_boil = curve[melt][0], curve[boil][0]
    for name, (t0, t1) in curve.items():
        if t0 == t1:
            continue
        if process == "solid_warming" and t1 <= lo_melt:
            return name
        if process == "liquid_warming" and t0 >= lo_melt and t1 <= lo_boil:
            return name
        if process == "vapour_warming" and t0 >= lo_boil:
            return name
    raise ValueError(process)


PARAMS = {"process": "melting"}
VARIANTS = [{"process": "boiling"}, {"process": "liquid_warming"}, {"process": "solid_warming"}]
ANSWER = 'BC'
