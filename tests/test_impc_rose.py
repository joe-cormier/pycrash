"""Impulse momentum (Carpenter) model against the Rose 2006 (SAE 2006-01-0908) crash tests."""
import numpy as np
import pytest

from pycrash.model_calcs.carpenter_momentum import IMPC
from pycrash.vehicle import Vehicle

VEHICLES = {"4363": ("HondaAccord", "ChevyBlazer"),
            "4364": ("HondaAccord", "ChevyTrailblazer"),
            "4438": ("HondaAccord4438", "MitsubishiMontero")}

# reference delta-V (mph) from this model on the tire-fix commit (94ba40b), cof = 0.1
REFERENCE_DV = {"4364": (34.97, 23.24), "4438": (34.99, 24.48)}


def run_impc(test_num, vehicle_data, test_data):
    """Positions both vehicles as in 'Validation - impact momentum no motion.ipynb' and runs IMPC."""
    inputs = test_data[test_num]
    veh1 = Vehicle("veh1", vehicle_data[VEHICLES[test_num][0]])
    veh2 = Vehicle("veh2", vehicle_data[VEHICLES[test_num][1]])
    for veh, prefix in ((veh1, "v1"), (veh2, "v2")):
        veh.head_angle = -1 * inputs[f"{prefix}_head_angle"]
        dx = np.cos(-1 * inputs[f"{prefix}_theta_cg_ic"] * np.pi / 180) * inputs[f"{prefix}_cg_ic"]
        dy = np.sin(-1 * inputs[f"{prefix}_theta_cg_ic"] * np.pi / 180) * inputs[f"{prefix}_cg_ic"]
        hangle_rad = veh.head_angle * np.pi / 180
        veh.init_x_pos = -1 * (dx * np.cos(hangle_rad) - dy * np.sin(hangle_rad))
        veh.init_y_pos = -1 * (dx * np.sin(hangle_rad) + dy * np.cos(hangle_rad))
        veh.vx_initial = inputs[f"{prefix}_vx"]
        if prefix == "v1":
            veh.pimpact_x = dx
            veh.pimpact_y = dy
            veh.impact_norm_rad = -1 * inputs["impact_norm_deg"] * np.pi / 180
    sim_inputs = {"cor": inputs["cor"], "cof": 0.1, "impact_norm_deg": -1 * inputs["impact_norm_deg"]}
    return veh1, veh2, IMPC(test_num, veh1, veh2, sim_inputs)


@pytest.mark.parametrize("test_num", sorted(VEHICLES))
def test_impulse_is_equal_and_opposite(test_num, rose_vehicle_data, rose_test_data):
    veh1, veh2, run = run_impc(test_num, rose_vehicle_data, rose_test_data)
    assert run.v1_result["dv"] * veh1.weight == pytest.approx(run.v2_result["dv"] * veh2.weight, rel=1e-6)


@pytest.mark.parametrize("test_num", sorted(REFERENCE_DV))
def test_delta_v_regression(test_num, rose_vehicle_data, rose_test_data):
    _, _, run = run_impc(test_num, rose_vehicle_data, rose_test_data)
    assert (run.v1_result["dv"], run.v2_result["dv"]) == pytest.approx(REFERENCE_DV[test_num], abs=0.01)
