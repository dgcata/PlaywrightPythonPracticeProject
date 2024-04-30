from decimal import Decimal, InvalidOperation
from typing import Tuple, Union, cast


def calculate_subtotal_tax_and_total(
    tax_rate: Union[Decimal, str, float, int],
    *item_prices: Union[Decimal, str, float, int],
) -> Tuple[Decimal, Decimal, Decimal]:
    try:
        tax_rate = Decimal(tax_rate)
        item_prices_list = [Decimal(item_price) for item_price in item_prices]
    except InvalidOperation:
        raise ValueError(f"invalid values found in args: {tax_rate, *item_prices}")

    raw_subtotal: Decimal = cast(Decimal, sum(item_prices_list))
    sub_total = raw_subtotal.quantize(Decimal("0.01"))

    raw_tax = sub_total * tax_rate
    tax_value = raw_tax.quantize(Decimal("0.01"))

    raw_total = sub_total + tax_value
    total_value = raw_total.quantize(Decimal("0.01"))

    return sub_total, tax_value, total_value
