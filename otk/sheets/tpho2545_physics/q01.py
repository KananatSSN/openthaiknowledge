"""Theory I.1 figure: A (2.0 kg) 1.0 m from the wall, B (1.0 kg) beyond it, spring 1.5 m; released from rest on a frictionless floor. The centre of mass stays 1.5 m from the wall; when the spring is 1.2 m, A is 0.4 m from it: 1.1 m from the wall."""


def solve(near=2.0, far=1.0, gap=1.0, length=1.5, later=1.2):
    centre = gap + far * length / (near + far)
    return centre - far * later / (near + far)


def check(near=2.0, far=1.0, gap=1.0, length=1.5, later=1.2, k=50.0):
    # Simulate the two masses on the spring (natural length shorter than both).
    natural = 0.5
    xa, xb, va, vb, dt = gap, gap + length, 0.0, 0.0, 1e-6
    while xb - xa > later:
        f = k * ((xb - xa) - natural)
        va += f / near * dt
        vb -= f / far * dt
        xa += va * dt
        xb += vb * dt
    return xa


PARAMS = {"near": 2.0, "far": 1.0, "gap": 1.0, "length": 1.5, "later": 1.2}
VARIANTS = [{"near": 1.0, "far": 1.0}, {"near": 3.0, "far": 2.0, "later": 1.0}, {"gap": 2.0, "length": 2.0, "later": 0.8}]
TOL = 1e-4
ANSWER = 1.1
