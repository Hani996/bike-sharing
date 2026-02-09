"""
Unit tests for OOP models and algorithms.

Run with:
    pytest tests/ -v

Students should add at least 10 test functions covering:
    - Model validation (happy path + edge cases)
    - Algorithm correctness (sorting, searching)
"""

import pytest
from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    Entity,
    Station,
)


# ---------------------------------------------------------------------------
# Entity / Bike tests (provided as examples)
# ---------------------------------------------------------------------------

class TestBike:
    """Tests for the Bike class hierarchy."""

    def test_classic_bike_creation(self) -> None:
        bike = ClassicBike(bike_id="BK001", gear_count=7)
        assert bike.id == "BK001"
        assert bike.bike_type == "classic"
        assert bike.gear_count == 7
        assert bike.status == "available"

    def test_classic_bike_rejects_zero_gears(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK002", gear_count=0)

    def test_bike_rejects_invalid_status(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK003", gear_count=5, status="broken")

    def test_bike_status_setter(self) -> None:
        bike = ClassicBike(bike_id="BK004")
        bike.status = "in_use"
        assert bike.status == "in_use"

    def test_entity_rejects_empty_id(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="", gear_count=5)


# ---------------------------------------------------------------------------
# TODO: add tests for ElectricBike, Station, User, Trip, etc.
# ---------------------------------------------------------------------------

# class TestElectricBike:
#     def test_electric_bike_creation(self):
#         ...
#     def test_electric_bike_rejects_negative_battery(self):
#         ...


# ---------------------------------------------------------------------------
# TODO: add tests for sorting and searching algorithms
# ---------------------------------------------------------------------------

# class TestAlgorithms:
#     def test_merge_sort_empty_list(self):
#         ...
#     def test_merge_sort_sorted_input(self):
#         ...
#     def test_binary_search_found(self):
#         ...
#     def test_binary_search_not_found(self):
#         ...
