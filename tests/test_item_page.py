from typing import Union

import pytest
from playwright.sync_api import expect

from pages.item_page import SauceDemoItemPage


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_successful_load(item_page: SauceDemoItemPage, item_id: int) -> None:
    item = item_page.VALID_ITEMS[item_id]

    item_page.goto_inventory_standard()
    item_page.goto_item_page(item_id)

    expect(item_page.page).to_have_url(item_page.URLS["item"].format(item_id))

    expect(item_page.item_name).to_contain_text(item.item_name)
    expect(item_page.item_description).to_contain_text(item.item_desc)
    expect(item_page.item_price).to_contain_text(str(item.item_price))
    expect(item_page.item_image).to_be_visible()
    expect(item_page.back_to_products_button).to_be_visible()
    expect(item_page.add_to_cart_button).to_be_visible()
    expect(item_page.remove_button).not_to_be_visible()


@pytest.mark.parametrize("item_id", [9, "9", "nan", "backpack"])
def test_item_does_not_exist(
    item_page: SauceDemoItemPage, item_id: Union[int, str]
) -> None:
    invalid_item = item_page.INVALID_ITEM

    item_page.goto_inventory_standard()
    item_page.goto_item_page(item_id)

    expect(item_page.page).to_have_url(item_page.URLS["item"].format(item_id))

    expect(item_page.item_name).to_contain_text(invalid_item.item_name)
    expect(item_page.item_description).to_contain_text(invalid_item.item_desc)
    expect(item_page.item_price).to_contain_text(str(invalid_item.item_price))
    expect(item_page.item_image).to_be_visible()
    expect(item_page.back_to_products_button).to_be_visible()
    expect(item_page.remove_button).not_to_be_visible()
    # an issue on Sauce Labs end, you shouldn't be able to add an invalid item to the cart
    # expect(item_page.add_to_cart_button).not_to_be_visible()


def test_can_add_item_from_item_page(
    fleece_jacket_item_page: SauceDemoItemPage,
) -> None:
    # assertion before adding to cart
    expect(fleece_jacket_item_page.add_to_cart_button).to_be_visible()
    expect(fleece_jacket_item_page.remove_button).not_to_be_visible()

    # adding item to cart
    fleece_jacket_item_page.add_item_to_cart()

    # assertion after adding to cart
    expect(fleece_jacket_item_page.add_to_cart_button).not_to_be_visible()
    expect(fleece_jacket_item_page.remove_button).to_be_visible()


def test_can_remove_item_from_item_page(
    fleece_jacket_item_page: SauceDemoItemPage,
) -> None:
    fleece_jacket_item_page.add_item_to_cart()
    # assertion before removing from cart
    expect(fleece_jacket_item_page.add_to_cart_button).not_to_be_visible()
    expect(fleece_jacket_item_page.remove_button).to_be_visible()

    # removing item from cart
    fleece_jacket_item_page.remove_item_from_cart()

    # assertion after removing from cart
    expect(fleece_jacket_item_page.add_to_cart_button).to_be_visible()
    expect(fleece_jacket_item_page.remove_button).not_to_be_visible()


def test_can_go_back_to_inventory_from_item_page(
    fleece_jacket_item_page: SauceDemoItemPage,
) -> None:
    fleece_jacket_item_page.go_back_to_inventory()
    expect(fleece_jacket_item_page.page).to_have_url(
        fleece_jacket_item_page.URLS["inventory"]
    )


def test_can_goto_cart_from_item_page(
    fleece_jacket_item_page: SauceDemoItemPage,
) -> None:
    fleece_jacket_item_page.goto_cart()
    expect(fleece_jacket_item_page.page).to_have_url(
        fleece_jacket_item_page.URLS["cart"]
    )


def test_can_logout_from_item_page(fleece_jacket_item_page: SauceDemoItemPage) -> None:
    fleece_jacket_item_page.logout()
    expect(fleece_jacket_item_page.page).to_have_url(fleece_jacket_item_page.MAIN_URL)
