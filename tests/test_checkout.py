import pytest
from playwright.sync_api import expect

from pages.checkout_pages import SauceDemoCheckoutPages


def test_successful_load(checkout_pages: SauceDemoCheckoutPages) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()

    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    expect(checkout_pages.cancel_button).to_be_visible()
    expect(checkout_pages.continue_button).to_be_visible()
    expect(checkout_pages.checkout_info).to_be_visible()

    expect(checkout_pages.cart_list).not_to_be_visible()
    expect(checkout_pages.subtotal_label).not_to_be_visible()
    expect(checkout_pages.tax_label).not_to_be_visible()
    expect(checkout_pages.total_label).not_to_be_visible()
    expect(checkout_pages.finish_button).not_to_be_visible()
    expect(checkout_pages.back_to_home_button).not_to_be_visible()
    expect(checkout_pages.complete_checkout_container).not_to_be_visible()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code",
    [
        ("John", "Doe", "6000"),
        ("Jane", "Doe", "7000"),
        ("standard", "user", "8000"),
    ],
)
def test_customer_details__succeeds(
    checkout_pages: SauceDemoCheckoutPages,
    first_name: str,
    last_name: str,
    postal_code: str,
) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()

    checkout_pages.enter_customer_details(first_name, last_name, postal_code)

    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    expect(checkout_pages.cancel_button).to_be_visible()
    expect(checkout_pages.cart_list).to_be_visible()
    expect(checkout_pages.subtotal_label).to_be_visible()
    expect(checkout_pages.tax_label).to_be_visible()
    expect(checkout_pages.total_label).to_be_visible()
    expect(checkout_pages.finish_button).to_be_visible()

    expect(checkout_pages.error_container).not_to_be_visible()
    expect(checkout_pages.continue_button).not_to_be_visible()
    expect(checkout_pages.checkout_info).not_to_be_visible()
    expect(checkout_pages.back_to_home_button).not_to_be_visible()
    expect(checkout_pages.complete_checkout_container).not_to_be_visible()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, error_msg",
    [
        ("", "", "", "First Name is required"),
        ("", "Doe", "", "First Name is required"),
        ("", "", "6000", "First Name is required"),
        ("", "Doe", "6000", "First Name is required"),
        ("John", "", "", "Last Name is required"),
        ("John", "", "6000", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)
def test_customer_details__fails(
    checkout_pages: SauceDemoCheckoutPages,
    first_name: str,
    last_name: str,
    postal_code: str,
    error_msg: str,
) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()

    # assertions before entering erroneous customer details
    expect(checkout_pages.error_container).not_to_be_visible()

    # entering erroneous customer details
    checkout_pages.enter_customer_details(first_name, last_name, postal_code)

    # assertions after entering erroneous customer details
    expect(checkout_pages.error_container).to_be_visible()
    expect(checkout_pages.error_container).to_contain_text(error_msg)


def test_complete_checkout(checkout_pages: SauceDemoCheckoutPages) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()
    checkout_pages.enter_customer_details("John", "Doe", "6000")
    checkout_pages.finish_checkout()

    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-complete.html"
    )

    expect(checkout_pages.back_to_home_button).to_be_visible()
    expect(checkout_pages.complete_checkout_container).to_be_visible()

    expect(checkout_pages.cart_list).not_to_be_visible()
    expect(checkout_pages.subtotal_label).not_to_be_visible()
    expect(checkout_pages.tax_label).not_to_be_visible()
    expect(checkout_pages.total_label).not_to_be_visible()
    expect(checkout_pages.finish_button).not_to_be_visible()
    expect(checkout_pages.continue_button).not_to_be_visible()
    expect(checkout_pages.checkout_info).not_to_be_visible()
    expect(checkout_pages.cancel_button).not_to_be_visible()


def test_go_back_to_inventory_after_checkout(
    checkout_pages: SauceDemoCheckoutPages,
) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()
    checkout_pages.enter_customer_details("John", "Doe", "6000")
    checkout_pages.finish_checkout()
    checkout_pages.go_back_to_inventory()

    expect(checkout_pages.page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_can_logout_from_step_one(checkout_pages: SauceDemoCheckoutPages) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()

    # assertions before logout
    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )

    # logout
    checkout_pages.logout()

    # assertions after logout
    expect(checkout_pages.page).to_have_url("https://www.saucedemo.com/")


def test_can_logout_from_step_two(checkout_pages: SauceDemoCheckoutPages) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()
    checkout_pages.enter_customer_details("John", "Doe", "6000")

    # assertions before logout
    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-step-two.html"
    )

    # logout
    checkout_pages.logout()

    # assertions after logout
    expect(checkout_pages.page).to_have_url("https://www.saucedemo.com/")


def test_can_logout_from_finished_page(checkout_pages: SauceDemoCheckoutPages) -> None:
    checkout_pages.goto_inventory_standard()
    checkout_pages.add_item_to_cart(0)
    checkout_pages.goto_cart()
    checkout_pages.checkout()
    checkout_pages.enter_customer_details("John", "Doe", "6000")
    checkout_pages.finish_checkout()

    # assertions before logout
    expect(checkout_pages.page).to_have_url(
        "https://www.saucedemo.com/checkout-complete.html"
    )

    # logout
    checkout_pages.logout()

    # assertions after logout
    expect(checkout_pages.page).to_have_url("https://www.saucedemo.com/")
