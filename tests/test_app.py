"""Intended to test the interactions of the
inventory page, item pages, cart page and checkout pages.

For the unit tests for the other pages,
refer to the test files containing their names.

This is done to separate the concern of testing
the components of each webpage and the interaction
between each webpage.

(Optional) test changes in the interactions
when not logged in as `standard_user` (if applicable)
"""

import pytest
from playwright.sync_api import expect

from pages.cart_page import SauceDemoCartPage
from pages.checkout_pages import SauceDemoCheckoutPages
from pages.inventory_page import SauceDemoInventoryPage
from pages.item_page import SauceDemoItemPage
from utils.accounting import calculate_subtotal_tax_and_total


@pytest.mark.parametrize("other_item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_inventory_page(
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    other_item_id: int,
) -> None:
    other_item = inventory_page.VALID_ITEMS[other_item_id]

    inventory_page.add_item_to_cart(5)
    inventory_page.add_item_to_cart(other_item_id)
    inventory_page.goto_cart()

    expect(cart_page.page).to_have_url(inventory_page.URLS["cart"])
    expect(cart_page.cart_list).to_contain_text("Sauce Labs Fleece Jacket")
    expect(cart_page.cart_list).to_contain_text(other_item.item_name)
    expect(
        cart_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(2)


@pytest.mark.parametrize("other_item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_item_page(
    inventory_page: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    other_item_id: int,
) -> None:
    other_item = inventory_page.VALID_ITEMS[other_item_id]

    inventory_page.goto_item_page(5)
    item_page.add_item_to_cart()
    item_page.go_back_to_inventory()

    inventory_page.goto_item_page(other_item_id)
    item_page.add_item_to_cart()
    item_page.goto_cart()

    expect(cart_page.page).to_have_url(inventory_page.URLS["cart"])
    expect(cart_page.cart_list).to_contain_text("Sauce Labs Fleece Jacket")
    expect(cart_page.cart_list).to_contain_text(other_item.item_name)
    expect(
        cart_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(2)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_inventory_page(
    buy_all_items_from_inventory: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove = buy_all_items_from_inventory.VALID_ITEMS[item_to_remove_id]

    # removes item first in the inventory
    # page before going to the cart page
    buy_all_items_from_inventory.remove_item_from_cart(item_to_remove_id)
    buy_all_items_from_inventory.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove.item_name)
    expect(
        cart_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(5)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_cart_page(
    buy_all_items_from_inventory: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove = buy_all_items_from_inventory.VALID_ITEMS[item_to_remove_id]

    # goes to the cart page first before
    # removing the item in the cart page
    buy_all_items_from_inventory.goto_cart()

    expect(cart_page.cart_list).to_contain_text(item_to_remove.item_name)

    cart_page.remove_item_from_cart(item_to_remove_id)

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove.item_name)
    expect(
        cart_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(5)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_item_page(
    buy_all_items_from_inventory: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove = buy_all_items_from_inventory.VALID_ITEMS[item_to_remove_id]

    # goes to the specific item page first
    # then removes the item there before
    # going to the cart page
    buy_all_items_from_inventory.goto_item_page(item_to_remove_id)
    item_page.remove_item_from_cart()
    item_page.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove.item_name)
    expect(
        cart_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(5)


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_checkout_with_one_item(
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    checkout_pages: SauceDemoCheckoutPages,
    item_id: int,
) -> None:
    item = inventory_page.VALID_ITEMS[item_id]
    (
        sub_total,
        tax_value,
        total_value,
    ) = calculate_subtotal_tax_and_total(inventory_page.TAX_RATE, item.item_price)

    inventory_page.add_item_to_cart(item_id)
    expect(
        inventory_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(1)
    inventory_page.goto_cart()

    cart_page.checkout()

    checkout_pages.enter_customer_details("John", "Doe", "6000")

    expect(checkout_pages.cart_list).to_contain_text(item.item_name)
    expect(checkout_pages.subtotal_label).to_contain_text(str(sub_total))
    expect(checkout_pages.tax_label).to_contain_text(str(tax_value))
    expect(checkout_pages.total_label).to_contain_text(str(total_value))

    checkout_pages.finish_checkout()
    expect(checkout_pages.complete_checkout_container).to_contain_text(
        "Thank you for your order!"
    )

    checkout_pages.go_back_to_inventory()
    expect(
        inventory_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(0)


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4])
def test_checkout_with_two_items(
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    checkout_pages: SauceDemoCheckoutPages,
    item_id: int,
) -> None:
    fleece_jacket = inventory_page.VALID_ITEMS[5]
    other_item = inventory_page.VALID_ITEMS[item_id]

    (
        sub_total,
        tax_value,
        total_value,
    ) = calculate_subtotal_tax_and_total(
        inventory_page.TAX_RATE, fleece_jacket.item_price, other_item.item_price
    )

    inventory_page.add_item_to_cart(5)
    inventory_page.add_item_to_cart(item_id)
    expect(
        inventory_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(2)
    inventory_page.goto_cart()

    cart_page.checkout()

    checkout_pages.enter_customer_details("John", "Doe", "6000")

    expect(checkout_pages.cart_list).to_contain_text(fleece_jacket.item_name)
    expect(checkout_pages.cart_list).to_contain_text(other_item.item_name)
    expect(checkout_pages.subtotal_label).to_contain_text(str(sub_total))
    expect(checkout_pages.tax_label).to_contain_text(str(tax_value))
    expect(checkout_pages.total_label).to_contain_text(str(total_value))

    checkout_pages.finish_checkout()
    expect(checkout_pages.complete_checkout_container).to_contain_text(
        "Thank you for your order!"
    )

    checkout_pages.go_back_to_inventory()
    expect(
        inventory_page.page.get_by_role("button").filter(has_text="Remove")
    ).to_have_count(0)


def test_checkout_with_all_items(
    buy_all_items_from_inventory: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    checkout_pages: SauceDemoCheckoutPages,
) -> None:
    item_price_list = [
        item.item_price for item in buy_all_items_from_inventory.VALID_ITEMS.values()
    ]

    (
        sub_total,
        tax_value,
        total_value,
    ) = calculate_subtotal_tax_and_total(
        buy_all_items_from_inventory.TAX_RATE,
        *item_price_list,
    )

    expect(
        buy_all_items_from_inventory.page.get_by_role("button").filter(
            has_text="Remove"
        )
    ).to_have_count(6)
    buy_all_items_from_inventory.goto_cart()

    cart_page.checkout()

    checkout_pages.enter_customer_details("John", "Doe", "6000")

    expect(checkout_pages.subtotal_label).to_contain_text(str(sub_total))
    expect(checkout_pages.tax_label).to_contain_text(str(tax_value))
    expect(checkout_pages.total_label).to_contain_text(str(total_value))

    checkout_pages.finish_checkout()
    expect(checkout_pages.complete_checkout_container).to_contain_text(
        "Thank you for your order!"
    )

    checkout_pages.go_back_to_inventory()
    expect(
        buy_all_items_from_inventory.page.get_by_role("button").filter(
            has_text="Remove"
        )
    ).to_have_count(0)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_checkout_without_one_item(
    buy_all_items_from_inventory: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    checkout_pages: SauceDemoCheckoutPages,
    item_to_remove_id: int,
) -> None:
    item_price_list = [
        item.item_price
        for item_id, item in buy_all_items_from_inventory.VALID_ITEMS.items()
        if item_id != item_to_remove_id
    ]
    item_to_remove = buy_all_items_from_inventory.VALID_ITEMS[item_to_remove_id]

    (
        sub_total,
        tax_value,
        total_value,
    ) = calculate_subtotal_tax_and_total(
        buy_all_items_from_inventory.TAX_RATE,
        *item_price_list,
    )

    buy_all_items_from_inventory.remove_item_from_cart(item_to_remove_id)
    expect(
        buy_all_items_from_inventory.page.get_by_role("button").filter(
            has_text="Remove"
        )
    ).to_have_count(5)
    buy_all_items_from_inventory.goto_cart()

    cart_page.checkout()

    checkout_pages.enter_customer_details("John", "Doe", "6000")

    # sauce demo's behaviour is unpredictable
    # sometimes the price displayed on the website #only have two decimal points
    # and sometimes it is non-terminating, this is an issue on sauce lab's end
    # adding this block to avoid flakiness in the subtotal_label, remove when Sauce Labs fixes this ui issue
    subtotal_label = calculate_subtotal_tax_and_total(
        buy_all_items_from_inventory.TAX_RATE,
        # text_content() -> str("Item total: $[:float]"), i.e. float starts at the 13th index
        checkout_pages.subtotal_label.text_content()[13:],  # type:ignore[index]
    )[0]
    assert subtotal_label == sub_total

    # TODO: uncomment this assertion and remove the code above this when the UI issue in Sauce Demo has been fixed
    # expect(checkout_pages.subtotal_label).to_contain_text(str(sub_total))
    expect(checkout_pages.tax_label).to_contain_text(str(tax_value))
    expect(checkout_pages.total_label).to_contain_text(str(total_value))
    expect(checkout_pages.cart_list).not_to_contain_text(item_to_remove.item_name)

    checkout_pages.finish_checkout()
    expect(checkout_pages.complete_checkout_container).to_contain_text(
        "Thank you for your order!"
    )

    checkout_pages.go_back_to_inventory()
    expect(
        buy_all_items_from_inventory.page.get_by_role("button").filter(
            has_text="Remove"
        )
    ).to_have_count(0)
