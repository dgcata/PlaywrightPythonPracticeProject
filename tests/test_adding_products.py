import pytest
from playwright.sync_api import expect
from pages.cart_page import SauceDemoCartPage
from pages.products_page import SauceDemoProductsPage


def test_successful_load(product_page: SauceDemoProductsPage):
    expect(product_page.page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )
    expect(product_page.inventory_container).to_be_visible()
    expect(product_page.sidebar_button).to_be_visible()
    expect(product_page.shopping_cart).to_be_visible()
    expect(product_page.logout_button).not_to_be_visible()


def test_logout(product_page: SauceDemoProductsPage):
    # assertions before logout
    expect(product_page.login_container).not_to_be_visible()
    expect(product_page.inventory_container).to_be_visible()
    expect(product_page.sidebar_button).to_be_visible()
    expect(product_page.shopping_cart).to_be_visible()

    # logout
    product_page.logout()

    # assertions after logout
    expect(product_page.page).to_have_url(
        "https://www.saucedemo.com/"
    )
    expect(product_page.login_container).to_be_visible()
    expect(product_page.inventory_container).not_to_be_visible()
    expect(product_page.sidebar_button).not_to_be_visible()
    expect(product_page.shopping_cart).not_to_be_visible()


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
def test_item_link(
    product_page: SauceDemoProductsPage, item_name: str, item_id: int
) -> None:
    product_page.goto_item_page(item_name)
    expect(product_page.page).to_have_url(
        f"https://www.saucedemo.com/inventory-item.html?id={item_id}"
    )


@pytest.mark.parametrize(
    "item_id",
    [0, 1, 2, 3, 4],
)
def test_adding_products_to_cart_and_checkout(
    product_page: SauceDemoProductsPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    other_item_name = product_page.VALID_ITEMS[item_id]

    product_page.add_item_to_cart(
        "Sauce Labs Fleece Jacket"
    )
    product_page.add_item_to_cart(
        other_item_name
    )
    product_page.goto_cart()

    expect(cart_page.page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )
    expect(cart_page.cart_list).to_contain_text(
        "Sauce Labs Fleece Jacket"
    )
    expect(cart_page.cart_list).to_contain_text(
        other_item_name
    )
