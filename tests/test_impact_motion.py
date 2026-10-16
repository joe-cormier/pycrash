"""Full Impact simulation (motion + IMPC) for the scenario in 'validation - impact momentum motion.ipynb'."""
import numpy as np
import pytest

from pycrash.impact_main import Impact
from pycrash.vehicle import Vehicle

# reference values from master d5bb525 on pandas 2.3
REFERENCE_DV = (11.2271, 10.7290)  # ft/s
REFERENCE_IMPACT_INDEX = 73


@pytest.fixture(scope="module")
def impact(project_vehicle_data):
    vehicle_data = project_vehicle_data
    veh1 = Vehicle("Striking", vehicle_data["ChevroletMalibu2004"])
    veh2 = Vehicle("Struck", vehicle_data["HondaAccord"])
    veh1.striking, veh2.striking = True, False
    veh1.isTrailer = veh2.isTrailer = False
    t = [0, 1, 2, 3, 4, 5]
    veh1.time_inputs(t, [0] * 6, [0, 0, 0.5, 0.5, 0.5, 0.5], [0, 0, 20, 20, 0, 0], show_plot=False)
    veh2.time_inputs(t, [0] * 6, [0] * 6, [0] * 6, show_plot=False)
    veh1.vx_initial, veh2.vx_initial = 30, 0
    veh1.impact_points = [(veh1.lcgf + veh1.f_hang - 1, (-1 * veh1.width / 2) + 1, -16.5)]
    veh2.edgeimpact = [3]
    veh2.edgeimpact_points = [(-1 * veh2.lcgr - veh2.r_hang, -1 * veh2.width / 2,
                               veh2.lcgf + veh2.f_hang, -1 * veh2.width / 2)]
    veh1.init_x_pos, veh1.init_y_pos, veh1.head_angle = 0, 0, 0
    veh2.init_x_pos, veh2.init_y_pos, veh2.head_angle = 40, -10, -90
    imp = Impact("Scenario1", 3, "IMPC", [veh1, veh2], [[0, 1]], {0: {"vehicle_mu": 0.45, "cor": 0.1}})
    imp.simulate(show_results=False)
    return imp


def test_impact_detected_at_reference_step(impact):
    assert list(impact._impactIndex) == [REFERENCE_IMPACT_INDEX]


def test_delta_v_matches_reference(impact):
    dv = (impact.impc_results[0]["veh1_impc_result"]["dv"], impact.impc_results[0]["veh2_impc_result"]["dv"])
    assert dv == pytest.approx(REFERENCE_DV, abs=1e-3)


def test_models_are_filled(impact):
    for veh in impact.vehicles:
        assert not veh.model[["t", "Vx", "Vy", "Dx", "Dy", "theta_deg"]].isna().any().any()


def test_struck_vehicle_moves_after_impact(impact):
    struck = impact.vehicles[1].model
    before = np.hypot(struck.Vx.iloc[REFERENCE_IMPACT_INDEX - 1], struck.Vy.iloc[REFERENCE_IMPACT_INDEX - 1])
    after = np.hypot(struck.Vx.iloc[REFERENCE_IMPACT_INDEX], struck.Vy.iloc[REFERENCE_IMPACT_INDEX])
    assert before == pytest.approx(0, abs=1e-9)
    assert after == pytest.approx(REFERENCE_DV[1], abs=1e-3)
