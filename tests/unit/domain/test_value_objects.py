import pytest
from datetime import date

from domain.value_objects.email import Email
from domain.value_objects.money import Money
from domain.value_objects.date_range import DateRange
from domain.exceptions.base import DomainException


class TestDateRange:
    def test_valid_range(self):
        dr = DateRange(start=date(2026, 1, 1), end=date(2026, 12, 31))
        assert dr.contains(date(2026, 6, 15))
        assert not dr.contains(date(2025, 6, 15))

    def test_invalid_range(self):
        with pytest.raises(DomainException, match="posterior"):
            DateRange(start=date(2026, 12, 1), end=date(2026, 1, 1))

    def test_same_day_range(self):
        dr = DateRange(start=date(2026, 5, 1), end=date(2026, 5, 1))
        assert dr.contains(date(2026, 5, 1))
