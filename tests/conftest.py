import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
IMPACT_VALIDATION_SRC = REPO_ROOT / "projects" / "validation impact momentum" / "src"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def rose_vehicle_data():
    return _load_module("vehicle_data_collection", IMPACT_VALIDATION_SRC / "vehicle_data_collection.py").vehicle_data


@pytest.fixture(scope="session")
def rose_test_data():
    return _load_module("test_inputs_rose", IMPACT_VALIDATION_SRC / "test_inputs_rose.py").test_data
