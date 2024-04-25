"""Intended to test the interactions of the
inventory page, item pages, cart page and checkout pages.

For the unit tests for the other pages,
refer to the test files containing their names.

This is done to separate the concern of testing
the components of each webpage and the interaction
between each webpage.

filename for this test file is still tentative.

Tests that are currently implemented are interaction between
the inventory page, item pages and the cart page

Checkout interactions is still in development
"""

import pytest
from pages.cart_page import SauceDemoCartPage
from pages.inventory_page import SauceDemoInventoryPage
from pages.item_page import SauceDemoItemPage
from playwright.sync_api import expect


@pytest.mark.parametrize("other_item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_inventory_page(
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    other_item_id: int,
) -> None:
    other_item_name = inventory_page.VALID_ITEMS[other_item_id].item_name

    inventory_page.add_item_to_cart(5)
    inventory_page.add_item_to_cart(other_item_id)
    inventory_page.goto_cart()

    expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(cart_page.cart_list).to_contain_text("Sauce Labs Fleece Jacket")
    expect(cart_page.cart_list).to_contain_text(other_item_name)


@pytest.mark.parametrize("other_item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_item_page(
    inventory_page: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    other_item_id: int,
) -> None:
    other_item_name = inventory_page.VALID_ITEMS[other_item_id].item_name

    inventory_page.goto_item_page(5)
    item_page.add_item_to_cart()
    item_page.go_back_to_inventory()

    inventory_page.goto_item_page(other_item_id)
    item_page.add_item_to_cart()
    item_page.goto_cart()

    expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(cart_page.cart_list).to_contain_text("Sauce Labs Fleece Jacket")
    expect(cart_page.cart_list).to_contain_text(other_item_name)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_inventory_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove_name = inventory_page__buy_all.VALID_ITEMS[
        item_to_remove_id
    ].item_name

    # removes item first in the inventory
    # page before going to the cart page
    inventory_page__buy_all.remove_item_from_cart(item_to_remove_id)
    inventory_page__buy_all.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove_name)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_cart_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove_name = inventory_page__buy_all.VALID_ITEMS[
        item_to_remove_id
    ].item_name

    # goes to the cart page first before
    # removing the item in the cart page
    inventory_page__buy_all.goto_cart()

    expect(cart_page.cart_list).to_contain_text(item_to_remove_name)

    cart_page.remove_item_from_cart(item_to_remove_id)

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove_name)


@pytest.mark.parametrize("item_to_remove_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_item_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    item_to_remove_id: int,
) -> None:
    item_to_remove_name = inventory_page__buy_all.VALID_ITEMS[
        item_to_remove_id
    ].item_name

    # goes to the specific item page first
    # then removes the item there before
    # going to the cart page
    inventory_page__buy_all.goto_item_page(item_to_remove_id)
    item_page.remove_item_from_cart()
    item_page.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove_name)
