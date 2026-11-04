"""Tests of eqpcomo(): every supported model/equipment/type combination and known regression cases."""
import csv
import math
import os
import warnings

import pytest

from ecoana import eqpcomo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, "docs", "ECO-ANA_supported_equipment.csv")

# Generic inputs inside the range of most correlations.
BASE = dict(T_K=400, P_bar=10, Pout_bar=20, vol_cum=10, area_sqm=100, height_m=10, diameter_m=2,
            thickness_m=0.02, volflow_cumph=50, massflow_kgph=5000, power_kW=100, num=20,
            packsize_in=1, pumphead_m=50, length_m=10)
# Combinations whose correlation range does not include the generic inputs.
OVERRIDES = {("Seider", "Centrifuge"): dict(diameter_m=1.0)}


def _rows():
    with open(TABLE, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _case(row):
    mats = row["Accepted materials"]
    material = "Carbon steel" if mats.startswith("—") else mats.split(", ")[0]
    driver = row["Driver options"].split(", ")[0] if row["Driver options"] else None
    eqptype = row["Type (eqptype)"] or None
    inputs = dict(BASE)
    inputs.update(OVERRIDES.get((row["Model"], row["Equipment"]), {}))
    return dict(model=row["Model"], equipment=row["Equipment"], eqptype=eqptype,
                material=material, driver=driver, **inputs)


ROWS = _rows()


def _cost(**kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return eqpcomo(**kwargs)


def _is_valid(result):
    return (isinstance(result, tuple) and result[0] is not None
            and math.isfinite(float(result[0])) and float(result[0]) > 0)


def test_table_lists_all_combinations():
    assert len(ROWS) >= 400


@pytest.mark.parametrize("row", ROWS, ids=lambda r: f"{r['Model']}|{r['Equipment']}|{r['Type (eqptype)']}")
def test_every_combination_returns_positive_cost(row):
    result = _cost(**_case(row))
    assert _is_valid(result), result


@pytest.mark.parametrize("row", ROWS[::7], ids=lambda r: f"{r['Model']}|{r['Equipment']}|{r['Type (eqptype)']}")
@pytest.mark.parametrize("factor", [0.5, 2.0, 5.0])
def test_scaled_inputs_do_not_raise(row, factor):
    case = _case(row)
    for key in ("vol_cum", "area_sqm", "volflow_cumph", "massflow_kgph", "power_kW"):
        case[key] = case[key] * factor
    _cost(**case)   # may print an out-of-range message, but must not raise


# Calls reported in the review (Code package #1, comments 3-6) -------------------------------------------
REVIEW_CASES = [
    dict(model="Towler", equipment="Compressor", eqptype="Centrifugal", T_K=400, P_bar=10,
         material="Carbon steel", power_kW=1000),
    dict(model="Peters", equipment="Compressor", eqptype="Centrifugal", T_K=400, P_bar=10,
         material="Carbon steel", power_kW=1000, driver="Steam turbine"),
    dict(model="Guthrie", equipment="Compressor", eqptype="Centrifugal", T_K=400, P_bar=10,
         material="Carbon steel", power_kW=1000, driver="Steam turbine"),
    dict(model="Turton", equipment="Heat exchanger (shell and tube)", eqptype="Floating head",
         material="CS shell/CS tube", area_sqm=100, P_bar=10),
    dict(model="Seider", equipment="Filters", eqptype="Plate and frame", area_sqm=50),
    dict(model="Seider", equipment="Vessel/Tower", eqptype="Vertical vessel", material="Stainless steel",
         diameter_m=2, height_m=10, P_bar=5, T_K=350),
]


@pytest.mark.parametrize("case", REVIEW_CASES, ids=lambda c: f"{c['model']}|{c['equipment']}")
def test_review_cases(case):
    assert _is_valid(_cost(**case))


@pytest.mark.parametrize("eqptype", ["Plate and frame", "Leaf", "Disc and drum", "Pan"])
def test_seider_filters(eqptype):
    assert _is_valid(_cost(model="Seider", equipment="Filters", eqptype=eqptype, area_sqm=50))


def test_seider_pump_accepts_pumphead():
    r = _cost(model="Seider", equipment="Pumps", eqptype="Centrifugal", material="Carbon steel",
              volflow_cumph=50, pumphead_m=50, power_kW=10, driver="Electric-open/drip proof")
    assert _is_valid(r)


def test_invalid_model_name_gives_message_not_exception(capsys):
    assert eqpcomo(model="Unknown", equipment="Pumps") == (None, None)
    assert "not available" in capsys.readouterr().out


def test_missing_required_input_gives_message(capsys):
    r = _cost(model="Turton", equipment="Pumps", material="Carbon steel", power_kW=10)   # eqptype missing
    assert r == (None, "2001 year basis")
    assert "Error" in capsys.readouterr().out


# Values checked against the source publications ----------------------------------------------------------
def test_towler_trays_bubble_cap_is_twice_sieve():
    # Towler & Sinnott (2008), Table 6.6: sieve 100 + 120 D^2, bubble cap 200 + 240 D^2 (per tray)
    sieve = _cost(model="Towler", equipment="Trays", eqptype="Sieve", material="Carbon steel", diameter_m=2, num=20)
    bubble = _cost(model="Towler", equipment="Trays", eqptype="Bubble cap", material="Carbon steel", diameter_m=2, num=20)
    assert sieve[0] == pytest.approx(20 * (100 + 120 * 2 ** 2))
    assert bubble[0] == pytest.approx(20 * (200 + 240 * 2 ** 2))


def test_turton_fan_flow_unit():
    # Turton Table A.1: fan capacity in m3/s; eqpcomo input in m3/h (3600 m3/h = 1 m3/s)
    small = _cost(model="Turton", equipment="Fans", eqptype="Centrifugal straight-radial",
                  material="Carbon steel", volflow_cumph=3600, P_bar=1.013, Pout_bar=1.1)
    large = _cost(model="Turton", equipment="Fans", eqptype="Centrifugal straight-radial",
                  material="Carbon steel", volflow_cumph=36000, P_bar=1.013, Pout_bar=1.1)
    assert _is_valid(small) and _is_valid(large)
    assert large[0] > small[0]


# Out-of-range sizes (lower limit / parallel units / extrapolation) -----------------------------------------
# Correlations without a size range in the source (cost proportional to the amount of packing, adsorbent or
# membrane area, and the height of structured packing) are not checked.
UNBOUNDED = {"Adsorbent", "Membrane", "Packing", "Packing (Structured)"}
SIZE_KEYS = ["vol_cum", "area_sqm", "volflow_cumph", "massflow_kgph", "power_kW", "length_m", "diameter_m", "height_m"]


def _size_key(row):
    sizes = [s.strip() for s in row["Size / capacity input(s)"].split(",")]
    return next((s for s in sizes if s in SIZE_KEYS), None)


RANGE_ROWS = [r for r in ROWS if r["Equipment"] not in UNBOUNDED and _size_key(r)
              and not (r["Model"] == "Seider" and r["Equipment"] == "Vessel/Tower" and _size_key(r) == "height_m")]


@pytest.mark.parametrize("row", RANGE_ROWS, ids=lambda r: f"{r['Model']}|{r['Equipment']}|{r['Type (eqptype)']}")
@pytest.mark.parametrize("factor", [1e-6, 1e5])
def test_out_of_range_size_issues_warning(row, factor):
    case = _case(row)
    key = _size_key(row)
    case[key] = case[key] * factor
    with pytest.warns(UserWarning):
        result = eqpcomo(**case)
    assert _is_valid(result), result


def test_seider_trays_large_diameter_is_finite():
    with pytest.warns(UserWarning, match="upper limit"):
        r = eqpcomo(model="Seider", equipment="Trays", eqptype="Sieve", material="Carbon steel", diameter_m=4000, num=20)
    assert _is_valid(r)


@pytest.mark.parametrize("eqptype", ["Auto batch separator (vertical)", "Auto batch separator (horizontal)",
                                     "Batch top-drive basket", "Batch bottom-drive basket"])
@pytest.mark.parametrize("diameter", [0.1, 5.0])
def test_seider_centrifuge_out_of_range(eqptype, diameter):
    with pytest.warns(UserWarning):
        r = eqpcomo(model="Seider", equipment="Centrifuge", eqptype=eqptype, material="Carbon steel", diameter_m=diameter)
    assert _is_valid(r)


def test_error_text_is_never_returned_as_cost(capsys):
    r = _cost(model="Turton", equipment="Packing", eqptype="Pall rings", material="Stainless steel", vol_cum=1)
    assert r == (None, "2001 year basis")
    assert "Error" in capsys.readouterr().out
    r = _cost(model="Turton", equipment="Packing", eqptype="Pall rings", material="Ceramic", vol_cum=0.001)
    assert _is_valid(r)
