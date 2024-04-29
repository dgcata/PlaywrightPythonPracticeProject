from decimal import Decimal
from typing import Tuple, cast


def calculate_subtotal_tax_and_total(
    tax_rate: Decimal,
    *item_prices: Decimal,
) -> Tuple[Decimal, Decimal, Decimal]:
    item_prices_list = list(item_prices)

    sub_total: Decimal = cast(Decimal, sum(item_prices_list))

    raw_tax = sub_total * tax_rate
    tax_value = raw_tax.quantize(Decimal("0.01"))

    total_value = sub_total + tax_value

    return sub_total, tax_value, total_value
