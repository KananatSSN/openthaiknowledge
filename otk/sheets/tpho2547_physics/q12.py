"""Theory 3(e): with v > c, an approaching object outruns its own echoes, which pile up and overlap; a receding object is never caught by the pulses, so nothing is reflected. Returns 'overlap', 'none' or 'ordered' (v < c: echoes arrive in order)."""


def solve(wave=340, speed=400, approaching=True):
    if speed < wave:
        return "ordered"
    return "overlap" if approaching else "none"


def check(wave=340, speed=400, approaching=True, start=100.0, gap=0.1):
    # Event simulation of two pulses: does each reach the object, and do the
    # echoes stay in emission order (echo 1 behind echo 0)?
    def meeting(n):
        sent = n * gap
        closing = wave + speed if approaching else wave - speed
        if closing <= 0:
            return None
        meet = (start + wave * sent) / closing
        return meet, (start - speed * meet if approaching else start + speed * meet)

    first, second = meeting(0), meeting(1)
    if first is None:
        return "none"
    # Position of each echo at a common later time T (moving toward x = 0).
    later = max(first[0], second[0]) + 1.0
    x0 = first[1] - wave * (later - first[0])
    x1 = second[1] - wave * (later - second[0])
    return "ordered" if x1 > x0 else "overlap"


PARAMS = {"wave": 340, "speed": 400, "approaching": True}
VARIANTS = [{"approaching": False}, {"speed": 100}, {"speed": 100, "approaching": False}]
ANSWER = 'overlap'
