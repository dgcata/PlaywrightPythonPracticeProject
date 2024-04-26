import pytest
from playwright.sync_api import expect

from pages.item_page import SauceDemoItemPage


@pytest.mark.parametrize(
    "item_id, item_name",
    [
        (0, "Sauce Labs Bike Light"),
        (1, "Sauce Labs Bolt T-Shirt"),
        (2, "Sauce Labs Onesie"),
        (3, "Test.allTheThings() T-Shirt (Red)"),
        (4, "Sauce Labs Backpack"),
        (5, "Sauce Labs Fleece Jacket"),
    ],
)
def test_successful_load(
    item_page: SauceDemoItemPage, item_id: int, item_name: str
) -> None:
    item_page.goto_inventory_standard()
    item_page.goto_item_page(item_id)

    expect(item_page.page).to_have_url(
        f"https://www.saucedemo.com/inventory-item.html?id={item_id}"
    )

    expect(item_page.item_name).to_contain_text(item_name)
    expect(item_page.item_description).to_be_visible()
    expect(item_page.item_price).to_be_visible()
    expect(item_page.item_image).to_be_visible()
    expect(item_page.back_to_products_button).to_be_visible()
    expect(item_page.add_to_cart_button).to_be_visible()
    expect(item_page.remove_button).not_to_be_visible()


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
        "https://www.saucedemo.com/inventory.html"
    )


def test_can_goto_cart_from_item_page(
    fleece_jacket_item_page: SauceDemoItemPage,
) -> None:
    fleece_jacket_item_page.goto_cart()
    expect(fleece_jacket_item_page.page).to_have_url(
        "https://www.saucedemo.com/cart.html"
    )


def test_can_logout_from_item_page(fleece_jacket_item_page: SauceDemoItemPage) -> None:
    fleece_jacket_item_page.logout()
    expect(fleece_jacket_item_page.page).to_have_url("https://www.saucedemo.com/")
