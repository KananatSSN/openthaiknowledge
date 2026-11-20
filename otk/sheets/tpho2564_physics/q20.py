"""Theory 3.2 b): a source u < f in front of the bilens forms virtual images at |v| = uf/(f - u). Adapted: u and f (cm) vary; returns cm."""


def solve(source=15.0, focal=20.0):
    return source * focal / (focal - source)


def check(source=15.0, focal=20.0):
    # two paraxial rays from the axis point: refraction y' = slope - y/f,
    # then extend them backwards to where they meet
    def ray(height):
        slope_in = height / source
        return height, slope_in - height / focal

    (y1, s1), (y2, s2) = ray(0.1), ray(0.2)
    return (y2 - y1) / (s2 - s1)


PARAMS = {"source": 15.0, "focal": 20.0}
VARIANTS = [{"source": 10.0}, {"focal": 30.0}, {"source": 19.0}]
ANSWER = 60.0
TOL = 1e-9
