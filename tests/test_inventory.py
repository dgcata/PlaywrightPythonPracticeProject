import pytest
from playwright.sync_api import expect
from pages.cart_page import SauceDemoCartPage
from pages.inventory_page import SauceDemoInventoryPage
from pages.item_page import SauceDemoItemPage


def test_successful_load(inventory_page: SauceDemoInventoryPage):
    expect(inventory_page.page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )
    expect(inventory_page.inventory_container).to_be_visible()
    expect(inventory_page.sidebar_button).to_be_visible()
    expect(inventory_page.shopping_cart).to_be_visible()
    expect(inventory_page.logout_button).not_to_be_visible()


def test_logout(inventory_page: SauceDemoInventoryPage):
    # assertions before logout
    expect(inventory_page.login_container).not_to_be_visible()
    expect(inventory_page.inventory_container).to_be_visible()
    expect(inventory_page.sidebar_button).to_be_visible()
    expect(inventory_page.shopping_cart).to_be_visible()

    # logout
    inventory_page.logout()

    # assertions after logout
    expect(inventory_page.page).to_have_url(
        "https://www.saucedemo.com/"
    )
    expect(inventory_page.login_container).to_be_visible()
    expect(inventory_page.inventory_container).not_to_be_visible()
    expect(inventory_page.sidebar_button).not_to_be_visible()
    expect(inventory_page.shopping_cart).not_to_be_visible()


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
    inventory_page: SauceDemoInventoryPage, item_name: str, item_id: int
) -> None:
    inventory_page.goto_item_page(item_name)
    expect(inventory_page.page).to_have_url(
        f"https://www.saucedemo.com/inventory-item.html?id={item_id}"
    )


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_inventory_page(
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    other_item_name = inventory_page.VALID_ITEMS[item_id]

    inventory_page.add_item_to_cart(
        "Sauce Labs Fleece Jacket"
    )
    inventory_page.add_item_to_cart(
        other_item_name
    )
    inventory_page.goto_cart()

    expect(cart_page.page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )
    expect(cart_page.cart_list).to_contain_text(
        "Sauce Labs Fleece Jacket"
    )
    expect(cart_page.cart_list).to_contain_text(
        other_item_name
    )


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4])
def test_adding_products_from_item_page(
    inventory_page: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    other_item_name = inventory_page.VALID_ITEMS[item_id]

    inventory_page.goto_item_page(
        "Sauce Labs Fleece Jacket"
    )
    item_page.add_item_to_cart()
    item_page.goto_inventory()

    inventory_page.goto_item_page(
        other_item_name
    )
    item_page.add_item_to_cart()
    item_page.goto_inventory()

    inventory_page.goto_cart()

    expect(cart_page.page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )
    expect(cart_page.cart_list).to_contain_text(
        "Sauce Labs Fleece Jacket"
    )
    expect(cart_page.cart_list).to_contain_text(
        other_item_name
    )


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_inventory_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    item_to_remove = inventory_page__buy_all.VALID_ITEMS[item_id]

    # removes item first in the products
    # page before going to cart cart page
    inventory_page__buy_all.remove_item_from_cart(item_to_remove)
    inventory_page__buy_all.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove)


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_cart_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    item_to_remove = inventory_page__buy_all.VALID_ITEMS[item_id]

    # goes to the cart page first before
    # removing the item in the cart page
    inventory_page__buy_all.goto_cart()

    expect(cart_page.cart_list).to_contain_text(item_to_remove)

    cart_page.remove_item_from_cart(item_to_remove)

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove)


@pytest.mark.parametrize("item_id", [0, 1, 2, 3, 4, 5])
def test_removing_product_from_item_page(
    inventory_page__buy_all: SauceDemoInventoryPage,
    item_page: SauceDemoItemPage,
    cart_page: SauceDemoCartPage,
    item_id: int,
) -> None:
    item_to_remove = inventory_page__buy_all.VALID_ITEMS[item_id]

    # goes to the specific item page first
    # then removes the item there before
    # going to the cart page
    inventory_page__buy_all.goto_item_page(item_to_remove)
    item_page.remove_item_from_cart()
    item_page.goto_cart()

    expect(cart_page.cart_list).not_to_contain_text(item_to_remove)
