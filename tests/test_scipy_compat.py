"""scipy.integrate.cumtrapz was removed in SciPy 1.14; the package must use cumulative_trapezoid."""
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1] / "pycrash"


def test_no_removed_cumtrapz_calls():
    offenders = [str(p.relative_to(PACKAGE_DIR)) for p in PACKAGE_DIR.rglob("*.py") if "cumtrapz" in p.read_text()]
    assert offenders == []

