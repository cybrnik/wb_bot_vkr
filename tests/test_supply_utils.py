import math
import pytest

from wb_assistance_bot.wb.supply_notifier.checking_orders import (
    normer_sales_percent_by_region,
    normer_sales_percent,
)


def test_normer_sales_percent_by_region_sum_to_100():
    res = normer_sales_percent_by_region(
        'Центральный федеральный округ',
        'Южный федеральный округ'
    )
    total = sum(percent for _, percent in res)
    assert math.isclose(total, 100.0, rel_tol=1e-9)


def test_normer_sales_percent_basic():
    assert normer_sales_percent([1, 1, 2]) == [25.0, 25.0, 50.0]
