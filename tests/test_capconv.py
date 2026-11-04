"""Tests of capconv(): factor sets, keyword aliases and chaining with capcomo()."""
import warnings

import pytest

from ecoana import capcomo, capconv

FACTOR_SETS = ["Peters and Timmerhaus", "Lang", "Smith"]


@pytest.mark.parametrize("model", FACTOR_SETS)
@pytest.mark.parametrize("phase", ["Fluid", "Solid"])
def test_tpec_to_tci_increases_cost(model, phase):
    tci = capconv(model=model, phase_processing=phase, cap_in="TPEC", cap_out="TCI", base_cost=1e6)
    assert tci is not None and tci > 1e6


@pytest.mark.parametrize("model", FACTOR_SETS)
def test_round_trip(model):
    tci = capconv(model=model, phase_processing="Fluid", cap_in="TPEC", cap_out="TCI", base_cost=1e6)
    back = capconv(model=model, phase_processing="Fluid", cap_in="TCI", cap_out="TPEC", base_cost=tci)
    assert back == pytest.approx(1e6)


@pytest.mark.parametrize("cap_in, cap_out", [("tpec", "tci"), ("TPEC", "TCI"), ("T.P.E.C.", "t c i"),
                                             ("Total purchased equipment cost", "Total capital investment")])
def test_aliases_with_lang(cap_in, cap_out):
    # Review comment (Code package #1, comment 8): short codes must work with the Lang factor set
    ref = capconv(model="Lang", phase_processing="Fluid", cap_in="Equipment cost",
                  cap_out="Total capital investment", base_cost=1e6)
    assert capconv(model="Lang", phase_processing="Fluid", cap_in=cap_in, cap_out=cap_out, base_cost=1e6) == pytest.approx(ref)


def test_unknown_keyword_returns_none(capsys):
    assert capconv(model="Lang", phase_processing="Fluid", cap_in="foo", cap_out="TCI", base_cost=1e6) is None
    assert "Error" in capsys.readouterr().out


def test_capcomo_output_can_be_passed_to_capconv():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for model, kw in [("Hill", dict(unit_num=7, scale_tpy=1e5)),
                          ("Petley", dict(unit_num=7, scale_tpy=1e5, Tmax_K=500, Pmax_bar=10)),
                          ("Lange 1", dict(energyloss_MW=100))]:
            cost, _, cost_type = capcomo(model=model, **kw)
            tci = capconv(model="Peters and Timmerhaus", phase_processing="Fluid",
                          cap_in=cost_type, cap_out="TCI", base_cost=cost)
            assert tci is not None and tci >= cost
