from playwright.sync_api import expect
import pytest
from pages.cart_page import SauceDemoCartPage


def test_successful_load(cart_page: SauceDemoCartPage) -> None:
    cart_page.goto_inventory_standard()
    cart_page.goto_cart()

    expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(cart_page.continue_shopping_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.cart_list).to_be_visible()


def test_can_logout_from_cart_page(cart_page: SauceDemoCartPage) -> None:
    cart_page.goto_inventory_standard()
    cart_page.goto_cart()
    cart_page.logout()

    expect(cart_page.page).to_have_url("https://www.saucedemo.com/")
def test_can_checkout_from_cart_page(cart_page: SauceDemoCartPage) -> None:
    cart_page.goto_inventory_standard()
    cart_page.add_item_to_cart("Sauce Labs Backpack")
    cart_page.goto_cart()
    cart_page.checkout()

    expect(cart_page.page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )


@pytest.mark.skip("needs fixing from Sauce Labs' end")
def test_cannot_checkout_with_empty_cart(cart_page: SauceDemoCartPage) -> None:
    # this is a bug from Sauce Labs' end
    # the web application can proceed to
    # checkout even with an empty cart
    # instead of erroring out
    cart_page.goto_inventory_standard()
    cart_page.goto_cart()
    cart_page.checkout()

    # assertions for erroring out


def test_can_go_back_to_inventory(cart_page: SauceDemoCartPage) -> None:
    cart_page.goto_inventory_standard()
    cart_page.goto_cart()
    cart_page.continue_shopping()

    expect(cart_page.page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.parametrize(
    "item_name",
    [
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Backpack",
        "Sauce Labs Fleece Jacket",
    ],
)
def test_can_remove_an_item_from_cart_page(
    cart_page: SauceDemoCartPage,
    item_name: str,
):
    cart_page.goto_inventory_standard()
    cart_page.add_item_to_cart(item_name)
    cart_page.goto_cart()

    # assertion before removing item
    expect(cart_page.cart_list).to_contain_text(item_name)
    # removing item
    cart_page.remove_item_from_cart(item_name)
    # assertion after removing item
    expect(cart_page.cart_list).not_to_contain_text(item_name)