"""Tests of capcomo(): all plant-level models, process libraries, range handling and input checks."""
import math
import warnings

import pytest

from ecoana import capcomo
from ecoana import capcomo as _capcomo_function  # noqa: F401  (the function shadows the module name)
import sys
M = sys.modules["ecoana.capcomo"]


def _run(**kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return capcomo(**kwargs)


def _valid(r):
    return r[0] is not None and math.isfinite(r[0]) and r[0] > 0


@pytest.mark.parametrize("model, kwargs", [
    ("Hill", dict(unit_num=7, scale_tpy=1e5)),
    ("Guthrie", dict(process="Methanol", scale_tpy=5.5e4)),
    ("Timms", dict(unit_num=7, scale_tpy=1e5, Tmax_K=1233, Pmax_bar=93)),
    ("Garrett", dict(process="Methanol (steam reforming & synthesis)", scale_tpy=1.5e6)),
    ("Petley", dict(unit_num=7, scale_tpy=1e5, Tmax_K=1233, Pmax_bar=93)),
    ("Lange 1", dict(energyloss_MW=232.4)),
    ("Lange 2", dict(energytransfer_MW=300)),
])
def test_each_model_returns_cost_basis_and_type(model, kwargs):
    r = _run(model=model, **kwargs)
    assert _valid(r)
    assert r[1] == M.CE_basis_dict[model][1] and r[2] == M.CE_basis_dict[model][2]


@pytest.mark.parametrize("process", list(M.Param_Garrett))
def test_garrett_library(process):
    s_lower, s_upper, a, n, unit = M.Param_Garrett[process]
    q = (s_lower * s_upper) ** 0.5 / unit           # inside the range
    assert _run(model="Garrett", process=process, scale_tpy=q)[0] == pytest.approx(a * (q * unit) ** n * 1e6, rel=1e-6)


@pytest.mark.parametrize("process", list(M.Cbase_Guthrie))
def test_guthrie_library_reproduces_base_cost(process):
    q = M.Qbase_Guthrie[process] / M.Qunit_Guthrie[process]
    assert _run(model="Guthrie", process=process, scale_tpy=q)[0] == pytest.approx(M.Cbase_Guthrie[process] * 1e6, rel=1e-6)


def test_garrett_book_example():
    # Towler & Sinnott (2008), Example 6.1: cyclohexane 200,000 t/y -> $9.2 MM (Jan 2006)
    r = _run(model="Garrett", process="Cyclohexane (liq-phase hydrogenation of benzene)", scale_tpy=2e5)
    assert r[0] / 1e6 == pytest.approx(9.2, abs=0.05)


def test_lange_coefficients():
    assert _run(model="Lange 1", energyloss_MW=100)[0] == pytest.approx(3.0 * 100 ** 0.84 * 1e6, rel=1e-6)
    assert _run(model="Lange 2", energytransfer_MW=100)[0] == pytest.approx(2.9 * 100 ** 0.55 * 1e6, rel=1e-6)


def test_timms_coefficient_and_currency():
    r = _run(model="Timms", unit_num=7, scale_tpy=1e6, Tmax_K=1233, Pmax_bar=93)
    gbp = 3860 * 7 * 1e6 ** 0.639 * 1233 ** 0.066 * 93 ** -0.016
    assert r[0] == pytest.approx(gbp * M.GBP_TO_USD_1992, rel=1e-6)


def test_out_of_range_warnings_and_split():
    with pytest.warns(UserWarning, match="parallel trains"):
        capcomo(model="Garrett", process="Methanol (steam reforming & synthesis)", scale_tpy=3e6)
    with pytest.warns(UserWarning, match="extrapolated"):
        capcomo(model="Garrett", process="Methanol (steam reforming & synthesis)", scale_tpy=1e6)
    with pytest.warns(UserWarning, match="lower bound"):
        r = capcomo(model="Petley", unit_num=7, scale_tpy=1000, Tmax_K=500, Pmax_bar=10)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert r[0] == capcomo(model="Petley", unit_num=7, scale_tpy=2250, Tmax_K=500, Pmax_bar=10)[0]
    with pytest.warns(UserWarning, match="parallel"):
        capcomo(model="Guthrie", process="Methanol", scale_tpy=1e6)
    with pytest.warns(UserWarning, match="parallel units"):
        capcomo(model="Lange 2", energytransfer_MW=1000)


@pytest.mark.parametrize("bad", [0, -1, "100", [1, 2], float("nan"), float("inf"), True])
@pytest.mark.parametrize("model, kwargs, key", [
    ("Hill", dict(unit_num=7), "scale_tpy"),
    ("Guthrie", dict(process="Methanol"), "scale_tpy"),
    ("Garrett", dict(process="Methanol (steam reforming & synthesis)"), "scale_tpy"),
    ("Timms", dict(unit_num=7, scale_tpy=1e5, Pmax_bar=10), "Tmax_K"),
    ("Petley", dict(unit_num=7, scale_tpy=1e5, Tmax_K=500), "Pmax_bar"),
    ("Lange 1", dict(), "energyloss_MW"),
    ("Lange 2", dict(), "energytransfer_MW"),
])
def test_invalid_inputs_return_none(model, kwargs, key, bad, capsys):
    r = _run(model=model, **{key: bad}, **kwargs)
    assert r[0] is None
    assert "Error" in capsys.readouterr().out


def test_unknown_model_returns_tuple(capsys):
    assert capcomo(model="Unknown") == (None, None, None)
    assert capcomo() == (None, None, None)


def test_model_name_normalization():
    assert _run(model="lange1", energyloss_MW=10) == _run(model="Lange 1", energyloss_MW=10)
