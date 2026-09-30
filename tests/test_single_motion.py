"""Straight-line braking with SingleMotion (2015 Honda CR-V from the single vehicle validation notebook)."""
import numpy as np
import pytest

from pycrash.kinematics import SingleMotion
from pycrash.vehicle import Vehicle

VEHDICT = {"year": 2015, "make": "Honda", "model": "CR-V", "weight": 3368.2, "vin": "3CZRM3H5*FG******",
           "brake": 0, "steer_ratio": 15.9, "init_x_pos": 0, "init_y_pos": 0, "head_angle": 0,
           "width": 5.97, "length": 14.96, "hcg": 2.16, "lcgf": 4.22, "lcgr": 4.37, "wb": 8.6,
           "track": 5.18, "f_hang": 3.02, "r_hang": 3.35, "tire_d": 1.42, "tire_w": 0.74,
           "izz": 2199.17, "fwd": 1, "rwd": 0, "awd": 0, "A": 381, "B": 137, "k": 1000, "L": 0, "c": 0,
           "vx_initial": 44, "vy_initial": 0, "omega_z": 0}
SIM_DEFAULTS = {"dt_motion": 0.01, "mu_max": 0.8, "alpha_max": 0.174533}


@pytest.fixture(scope="module")
def braking_model():
    veh = Vehicle("veh1", dict(VEHDICT))
    t = np.linspace(0, 3, 4)
    veh.time_inputs(t, [0] * 4, [0, 1, 1, 1], [0] * 4, show_plot=False)
    return SingleMotion("braking", veh, SIM_DEFAULTS).veh.model


def test_model_has_no_nans(braking_model):
    assert not braking_model[["t", "Vx", "Vy", "Dx", "Dy", "theta_deg"]].isna().any().any()


def test_initial_speed_converted_to_fps(braking_model):
    assert braking_model.Vx.iloc[0] == pytest.approx(44 * 1.46667, rel=1e-4)


def test_full_braking_deceleration_matches_friction(braking_model):
    # brake is fully applied from t = 1 s; deceleration should be close to mu * g
    v = braking_model.set_index("t").Vx
    decel_g = (v.loc[1.0] - v.loc[2.0]) / 32.2
    assert decel_g == pytest.approx(SIM_DEFAULTS["mu_max"], abs=0.02)


def test_straight_line_stays_straight(braking_model):
    assert braking_model.Dy.abs().max() == pytest.approx(0, abs=1e-9)
    assert braking_model.theta_deg.abs().max() == pytest.approx(0, abs=1e-9)


def test_stopping_distance_regression(braking_model):
    # reference value from this model on the tire-fix commit (94ba40b)
    assert braking_model.Dx.iloc[-1] == pytest.approx(112.12, rel=5e-3)
