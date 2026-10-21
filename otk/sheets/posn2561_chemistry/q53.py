"""Source p12, MC53: network solid versus molecular attraction."""

NETWORK = {"SiO₂", "SiC", "เพชร", "BN (ลูกบาศก์)"}


def solve(network="SiO₂"):
    assert network in NETWORK
    return 3  # high melting follows extended covalent bonds, not molecular dipoles


def check(network="SiO₂"):
    statements = (
        True,  # metallic tungsten conducts in the solid state
        True,  # acetylene is gaseous near room temperature
        True,  # aqueous CsI contains mobile ions
        network not in NETWORK,  # claimed dipole–dipole origin of high melting
    )
    return statements.index(False)


PARAMS = {"network": "SiO₂"}
VARIANTS = [{"network": "SiC"}, {"network": "เพชร"}, {"network": "BN (ลูกบาศก์)"}]
ANSWER = 3
