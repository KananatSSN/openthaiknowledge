"""Shared parcel-by-parcel simulation for problem 2: gas at pressure P = mg/a and temperature T_A leaves cylinder A and enters the spring cylinder B (spring constant k, area a, empty at first). Each parcel brings its enthalpy gamma/(gamma - 1) R T_A per mole into B while B's gas pushes the spring; flow stops when B's pressure reaches P."""

R = 8.314


def transfer(mass, area, spring, gamma, temp, g=9.8, parcels=20000):
    """Return (moles moved, V_B, T_B, work on A's gas, work on B's piston, internal energy change)."""
    P = mass * g / area
    # moles needed are not known in advance; step in volume of B instead
    x_end = mass * g / spring
    n = U = work_b = 0.0
    x = 0.0
    dx = x_end / parcels
    for _ in range(parcels):
        # B's pressure rises with the spring: P_B = k x / a. Energy balance for
        # B over the step: dU = h dn - P_B dV with U = P_B V/(gamma - 1).
        x_new = x + dx
        p_old, p_new = spring * x / area, spring * x_new / area
        dV = area * dx
        work = (p_old + p_new) / 2 * dV
        U_new = p_new * area * x_new / (gamma - 1)
        dn = (U_new - U + work) / (gamma / (gamma - 1) * R * temp)
        n += dn
        U = U_new
        work_b += work
        x = x_new
    V_B = area * x
    T_B = P * V_B / (n * R)
    work_a = n * R * temp            # P times the volume the moved gas filled in A
    change = U - n * R * temp / (gamma - 1)
    return n, V_B, T_B, work_a, work_b, change
