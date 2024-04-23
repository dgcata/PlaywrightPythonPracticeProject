from playwright.sync_api import Page, expect
import pytest

from pages.product_page import SauceDemoProductPage


@pytest.mark.parametrize(
    "item_name, item_id",
    [
        ("Sauce Labs Bike Light", 0),
        ("Sauce Labs Bolt T-Shirt", 1),
        ("Sauce Labs Onesie", 2),
        ("Test.allTheThings() T-Shirt (Red)", 3),
        ("Sauce Labs Backpack", 4),
        ("Sauce Labs Fleece Jacket", 5),
    ]
)
def test_link(page: Page, item_name: str, item_id: int):
    product_page = SauceDemoProductPage(page)
    product_page.navigate_to_inventory_standard()
    product_page.goto_item_page(item_name)
    expect(product_page.page).to_have_url(
        f"https://www.saucedemo.com/inventory-item.html?id={item_id}"
    )


@pytest.mark.parametrize(
    "item_name",
    [
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Backpack",
        "Sauce Labs Fleece Jacket",
    ]
)
def test_add_to_cart(page: Page, item_name: str):
    product_page = SauceDemoProductPage(page)
    product_page.navigate_to_inventory_standard()
    remove_button = (
        product_page._SauceDemoProductPage__get_item_remove_from_cart_button(
            item_name
        )
    )

    expect(remove_button).not_to_be_visible()

    product_page.add_item_to_cart(item_name)

    expect(remove_button).to_be_visible()
