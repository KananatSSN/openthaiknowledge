"""Part2,10: initial lens-screen distance45cm. Lens moves6cm away from fixed object; screen moves3cm toward object in LAB frame, so final image distance36cm. u1=30cm,f18cm. Source lab-frame convention made explicit in generator."""

from math import sqrt


def solve(image=45, lens_move=6, screen_move=3):
    final = image - lens_move - screen_move
    if final <= 0:
        raise ValueError("screen must remain behind lens")
    product = lens_move * image * final / (lens_move + screen_move)
    u = (sqrt(lens_move * lens_move + 4 * product) - lens_move) / 2
    return u * image / (u + image)


def check(image=45, lens_move=6, screen_move=3):
    final = image - lens_move - screen_move
    lo, hi = 1e-10, float(final) * (1 - 1e-10)
    for _ in range(100):
        focal = (lo + hi) / 2
        u = focal * image / (image - focal)
        second_image = focal * (u + lens_move) / (u + lens_move - focal)
        if second_image < final:
            lo = focal
        else:
            hi = focal
    return (lo + hi) / 2


PARAMS = {"image": 45, "lens_move": 6, "screen_move": 3}
VARIANTS = [
    {"image": 30, "lens_move": 4, "screen_move": 2},
    {"image": 60, "lens_move": 8, "screen_move": 4},
    {"image": 75, "lens_move": 10, "screen_move": 5},
]
ANSWER = 18.0
