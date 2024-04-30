import pytest
from playwright.sync_api import expect

from pages.inventory_page import SauceDemoInventoryPage


def test_successful_load(inventory_page: SauceDemoInventoryPage) -> None:
    expect(inventory_page.page).to_have_url(inventory_page.URLS["inventory"])
    expect(inventory_page.inventory_container).to_be_visible()
    expect(inventory_page.sidebar_button).to_be_visible()
    expect(inventory_page.shopping_cart).to_be_visible()
    expect(inventory_page.logout_button).not_to_be_visible()


def test_logout(inventory_page: SauceDemoInventoryPage) -> None:
    # assertions before logout
    expect(inventory_page.login_container).not_to_be_visible()
    expect(inventory_page.inventory_container).to_be_visible()
    expect(inventory_page.sidebar_button).to_be_visible()
    expect(inventory_page.shopping_cart).to_be_visible()

    # logout
    inventory_page.logout()

    # assertions after logout
    expect(inventory_page.page).to_have_url(inventory_page.MAIN_URL)
    expect(inventory_page.login_container).to_be_visible()
    expect(inventory_page.inventory_container).not_to_be_visible()
    expect(inventory_page.sidebar_button).not_to_be_visible()
    expect(inventory_page.shopping_cart).not_to_be_visible()


@pytest.mark.parametrize(
    "item_id, expected_item_name",
    [
        (0, "Sauce Labs Bike Light"),
        (1, "Sauce Labs Bolt T-Shirt"),
        (2, "Sauce Labs Onesie"),
        (3, "Test.allTheThings() T-Shirt (Red)"),
        (4, "Sauce Labs Backpack"),
        (5, "Sauce Labs Fleece Jacket"),
    ],
)
def test_item_link(
    inventory_page: SauceDemoInventoryPage, item_id: int, expected_item_name: str
) -> None:
    inventory_page.goto_item_page(item_id)

    expect(inventory_page.page).to_have_url(inventory_page.URLS["item"].format(item_id))

    item_name = inventory_page.page.locator('[data-test="inventory-item-name"]')
    expect(item_name).to_contain_text(expected_item_name)


def test_goto_cart(inventory_page: SauceDemoInventoryPage) -> None:
    inventory_page.goto_cart()
    expect(inventory_page.page).to_have_url(inventory_page.URLS["cart"])
