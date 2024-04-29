from decimal import Decimal
from typing import Dict, List

import pytest

from utils.accounting import calculate_subtotal_tax_and_total


@pytest.mark.parametrize(
    "item_price_list, expected_results",
    [
        # rounds up
        (
            [Decimal("9.99")],
            {
                "sub_total": Decimal("9.99"),
                # instead of 0.7992
                "tax_value": Decimal("0.80"),
                # instead of 10.7892
                "total_value": Decimal("10.79"),
            },
        ),
        (
            [Decimal("9.99"), Decimal("5.49")],
            {
                "sub_total": Decimal("15.48"),
                # instead of 1.2384
                "tax_value": Decimal("1.24"),
                # instead of 16.7184
                "total_value": Decimal("16.72"),
            },
        ),
        # rounds down
        (
            [Decimal("14.24"), Decimal("10.44")],
            {
                "sub_total": Decimal("24.68"),
                # instead of 1.9744
                "tax_value": Decimal("1.97"),
                # instead of 26.6544
                "total_value": Decimal("26.65"),
            },
        ),
        (
            [Decimal("4.75"), Decimal("7.55")],
            {
                "sub_total": Decimal("12.30"),
                # instead of 0.984
                "tax_value": Decimal("0.98"),
                # instead of 13.284
                "total_value": Decimal("13.28"),
            },
        ),
    ],
)
def test_calculate_subtotal_tax_and_total(
    item_price_list: List[Decimal], expected_results: Dict[str, Decimal]
) -> None:
    tax_rate = Decimal("0.08")

    (
        sub_total,
        tax_value,
        total_value,
    ) = calculate_subtotal_tax_and_total(tax_rate, *item_price_list)

    assert sub_total == expected_results["sub_total"]
    assert tax_value == expected_results["tax_value"]
    assert total_value == expected_results["total_value"]
