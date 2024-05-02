import pytest
from playwright.sync_api import expect

from pages.cart_page import SauceDemoCartPage


def test_successful_load(cart_with_one_item: SauceDemoCartPage) -> None:
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["cart"])
    expect(cart_with_one_item.continue_shopping_button).to_be_visible()
    expect(cart_with_one_item.checkout_button).to_be_visible()
    expect(cart_with_one_item.cart_list).to_be_visible()


def test_can_logout_from_cart_page(cart_with_one_item: SauceDemoCartPage) -> None:
    # assertions before logout
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["cart"])

    # logout
    cart_with_one_item.logout()

    # assertions after logout
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.MAIN_URL)


def test_can_checkout_from_cart_page(cart_with_one_item: SauceDemoCartPage) -> None:
    # assertions before checkout
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["cart"])

    # checkout
    cart_with_one_item.checkout()

    # assertions after checkout
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["checkout_one"])


@pytest.mark.skip("needs fixing from Sauce Labs' end")
def test_cannot_checkout_with_empty_cart(cart_with_one_item: SauceDemoCartPage) -> None:
    # this is a bug from Sauce Labs' end
    # the web application can proceed to
    # checkout even with an empty cart
    # instead of erroring out
    cart_with_one_item.checkout()

    # assertions for erroring out


def test_can_go_back_to_inventory(cart_with_one_item: SauceDemoCartPage) -> None:
    # assertions before going back to inventory
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["cart"])

    # going back to inventory
    cart_with_one_item.continue_shopping()

    # assertions after going back to inventory
    expect(cart_with_one_item.page).to_have_url(cart_with_one_item.URLS["inventory"])


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_can_remove_an_item_from_cart_page(
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    item = cart_page.VALID_ITEMS[item_id]

    cart_page.goto_inventory_standard()
    cart_page.add_item_to_cart(item_id)
    cart_page.goto_cart()

    # assertion before removing item
    expect(cart_page.cart_list).to_contain_text(item.item_name)
    # removing item
    cart_page.remove_item_from_cart(item_id)
    # assertion after removing item
    expect(cart_page.cart_list).not_to_contain_text(item.item_name)
