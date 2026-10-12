"""Stage 4 — prove each solver still works when you change the constants.

The claim a generator makes is strong: *this answer is right for constants no
human has ever checked*. Nothing about a closed-form ``solve`` justifies that on
its own — a wrong exponent reproduces the sheet's answer just fine if you only
ever test the sheet's numbers.

So verification is three separate things, and a solver is only "green" when all
three hold:

* **reference** — ``solve(**PARAMS) == ANSWER``: it reproduces the sheet.
* **cross-check** — ``check(**PARAMS) == solve(**PARAMS)``: a second, independently
  written method agrees. Brute force, numeric simulation, a different identity.
* **variants** — the same agreement at every entry of ``VARIANTS``: other
  constants, where no published answer exists and the two methods are all there
  is. This is the test that actually earns the generator.

An item with no ``check`` is reported ``cross_checked=False`` rather than failing
— some answers genuinely have one derivation — but it is a standing invitation
to go find a second one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from numbers import Real
from types import ModuleType

from .spec import ItemSpec, SheetSpec, solver_modules

TOL = 1e-9


def normalize(value):
    """Compare-ready form: nested sequences flatten, exact ints stay exact."""
    if isinstance(value, (list, tuple)):
        return tuple(normalize(v) for v in value)
    if isinstance(value, set):
        return tuple(sorted((normalize(v) for v in value), key=repr))
    if isinstance(value, Fraction) and value.denominator == 1:
        return value.numerator
    if isinstance(value, bool) or not isinstance(value, Real):
        return value
    return value


def same(a, b, tol: float = TOL) -> bool:
    """Equality that tolerates float drift between two derivations."""
    a, b = normalize(a), normalize(b)
    if isinstance(a, tuple) and isinstance(b, tuple):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, Real) and isinstance(b, Real) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)))
    return a == b


@dataclass
class VerifyResult:
    number: int
    solver: str
    reference_ok: bool = False
    cross_checked: bool = False
    variants_run: int = 0
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.reference_ok and not self.problems

    def line(self) -> str:
        mark = "OK  " if self.ok else "FAIL"
        cross = "x2" if self.cross_checked else "--"
        return (f"[{mark}] q{self.number:02d} {cross} "
                f"{self.variants_run} variants"
                + ("" if self.ok else "  " + "; ".join(self.problems)))


def _kwargs_of(fn) -> set[str]:
    import inspect
    return {p.name for p in inspect.signature(fn).parameters.values()
            if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)}


def verify_item(item: ItemSpec, mod: ModuleType) -> VerifyResult:
    """Run the full contract against one solver module."""
    res = VerifyResult(number=item.number, solver=item.solver)
    params = getattr(mod, "PARAMS", None)
    solve = getattr(mod, "solve", None)
    if not isinstance(params, dict) or not callable(solve):
        res.problems.append("missing PARAMS or solve()")
        return res

    # A geometry solver whose second method is a numeric construction cannot hit
    # 1e-9; it says so by exporting TOL, rather than the harness guessing.
    tol = float(getattr(mod, "TOL", TOL))
    accepted = _kwargs_of(solve)
    if unknown := set(params) - accepted:
        res.problems.append(f"PARAMS not accepted by solve(): {sorted(unknown)}")
        return res

    try:
        got = solve(**params)
    except Exception as exc:                                  # noqa: BLE001
        res.problems.append(f"solve(**PARAMS) raised {exc!r}")
        return res

    if not hasattr(mod, "ANSWER"):
        res.problems.append("missing ANSWER")
    elif not same(got, mod.ANSWER, tol):
        res.problems.append(f"solve(**PARAMS)={got!r} != ANSWER={mod.ANSWER!r}")
    else:
        res.reference_ok = True

    check = getattr(mod, "check", None)
    if callable(check):
        res.cross_checked = True
        try:
            if not same(check(**params), got, tol):
                res.problems.append(
                    f"check(**PARAMS)={check(**params)!r} != solve()={got!r}")
        except Exception as exc:                              # noqa: BLE001
            res.problems.append(f"check(**PARAMS) raised {exc!r}")

    for i, override in enumerate(getattr(mod, "VARIANTS", []) or []):
        if stray := set(override) - set(params):
            res.problems.append(f"variant {i}: unknown params {sorted(stray)}")
            continue
        merged = {**params, **override}
        try:
            a = solve(**merged)
        except Exception as exc:                              # noqa: BLE001
            res.problems.append(f"variant {i} {override}: solve raised {exc!r}")
            continue
        res.variants_run += 1
        if callable(check):
            try:
                b = check(**merged)
            except Exception as exc:                          # noqa: BLE001
                res.problems.append(
                    f"variant {i} {override}: check raised {exc!r}")
                continue
            if not same(a, b, tol):
                res.problems.append(
                    f"variant {i} {override}: solve={a!r} != check={b!r}")
    return res


def verify_sheet(sheet: SheetSpec) -> list[VerifyResult]:
    return [verify_item(it, mod) for it, mod in solver_modules(sheet)]


def report(results: list[VerifyResult]) -> str:
    bad = [r for r in results if not r.ok]
    thin = [r for r in results if r.ok and not r.cross_checked]
    lines = [r.line() for r in results]
    lines.append(f"\n{len(results) - len(bad)}/{len(results)} solvers green, "
                 f"{sum(r.variants_run for r in results)} variant runs, "
                 f"{len(thin)} without an independent check"
                 + (f" (q{', q'.join(str(r.number) for r in thin)})"
                    if thin else ""))
    return "\n".join(lines)
