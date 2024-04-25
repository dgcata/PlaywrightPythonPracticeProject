from playwright.sync_api import expect
from pages.cart_page import SauceDemoCartPage


def test_successful_load(
    cart_page: SauceDemoCartPage
) -> None:
    cart_page.goto_inventory_standard()
    cart_page.goto_cart()

    expect(cart_page.continue_shopping_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.cart_list).to_be_visible()
