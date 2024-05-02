import pytest
from playwright.sync_api import expect

from pages.checkout_pages import SauceDemoCheckoutPages


def test_successful_load(
    checkout_with_one_item: SauceDemoCheckoutPages,
) -> None:
    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_one"]
    )

    expect(checkout_with_one_item.cancel_button).to_be_visible()
    expect(checkout_with_one_item.continue_button).to_be_visible()
    expect(checkout_with_one_item.checkout_info).to_be_visible()

    expect(checkout_with_one_item.cart_list).not_to_be_visible()
    expect(checkout_with_one_item.subtotal_label).not_to_be_visible()
    expect(checkout_with_one_item.tax_label).not_to_be_visible()
    expect(checkout_with_one_item.total_label).not_to_be_visible()
    expect(checkout_with_one_item.finish_button).not_to_be_visible()
    expect(checkout_with_one_item.back_to_home_button).not_to_be_visible()
    expect(checkout_with_one_item.complete_checkout_container).not_to_be_visible()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code",
    [
        ("John", "Doe", "6000"),
        ("Jane", "Doe", "7000"),
        ("standard", "user", "8000"),
    ],
)
def test_customer_details__succeeds(
    checkout_with_one_item: SauceDemoCheckoutPages,
    first_name: str,
    last_name: str,
    postal_code: str,
) -> None:
    checkout_with_one_item.enter_customer_details(first_name, last_name, postal_code)

    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_two"]
    )

    expect(checkout_with_one_item.cancel_button).to_be_visible()
    expect(checkout_with_one_item.cart_list).to_be_visible()
    expect(checkout_with_one_item.subtotal_label).to_be_visible()
    expect(checkout_with_one_item.tax_label).to_be_visible()
    expect(checkout_with_one_item.total_label).to_be_visible()
    expect(checkout_with_one_item.finish_button).to_be_visible()

    expect(checkout_with_one_item.continue_button).not_to_be_visible()
    expect(checkout_with_one_item.checkout_info).not_to_be_visible()
    expect(checkout_with_one_item.back_to_home_button).not_to_be_visible()
    expect(checkout_with_one_item.complete_checkout_container).not_to_be_visible()


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
    checkout_with_one_item: SauceDemoCheckoutPages,
    first_name: str,
    last_name: str,
    postal_code: str,
    error_msg: str,
) -> None:
    # assertions before entering erroneous customer details
    expect(checkout_with_one_item.error_container).not_to_be_visible()

    # entering erroneous customer details
    checkout_with_one_item.enter_customer_details(first_name, last_name, postal_code)

    # assertions after entering erroneous customer details
    expect(checkout_with_one_item.error_container).to_be_visible()
    expect(checkout_with_one_item.error_container).to_contain_text(error_msg)


def test_complete_checkout(checkout_with_one_item: SauceDemoCheckoutPages) -> None:
    checkout_with_one_item.enter_customer_details("John", "Doe", "6000")
    checkout_with_one_item.finish_checkout()

    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_done"]
    )

    expect(checkout_with_one_item.back_to_home_button).to_be_visible()
    expect(checkout_with_one_item.complete_checkout_container).to_be_visible()

    expect(checkout_with_one_item.cart_list).not_to_be_visible()
    expect(checkout_with_one_item.subtotal_label).not_to_be_visible()
    expect(checkout_with_one_item.tax_label).not_to_be_visible()
    expect(checkout_with_one_item.total_label).not_to_be_visible()
    expect(checkout_with_one_item.finish_button).not_to_be_visible()
    expect(checkout_with_one_item.continue_button).not_to_be_visible()
    expect(checkout_with_one_item.checkout_info).not_to_be_visible()
    expect(checkout_with_one_item.cancel_button).not_to_be_visible()


def test_go_back_to_inventory_after_checkout(
    checkout_with_one_item: SauceDemoCheckoutPages,
) -> None:
    checkout_with_one_item.enter_customer_details("John", "Doe", "6000")
    checkout_with_one_item.finish_checkout()
    checkout_with_one_item.go_back_to_inventory()

    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["inventory"]
    )


def test_can_logout_from_step_one(
    checkout_with_one_item: SauceDemoCheckoutPages,
) -> None:
    # assertions before logout
    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_one"]
    )

    # logout
    checkout_with_one_item.logout()

    # assertions after logout
    expect(checkout_with_one_item.page).to_have_url(checkout_with_one_item.MAIN_URL)


def test_can_logout_from_step_two(
    checkout_with_one_item: SauceDemoCheckoutPages,
) -> None:
    checkout_with_one_item.enter_customer_details("John", "Doe", "6000")

    # assertions before logout
    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_two"]
    )

    # logout
    checkout_with_one_item.logout()

    # assertions after logout
    expect(checkout_with_one_item.page).to_have_url(checkout_with_one_item.MAIN_URL)


def test_can_logout_from_finished_page(
    checkout_with_one_item: SauceDemoCheckoutPages,
) -> None:
    checkout_with_one_item.enter_customer_details("John", "Doe", "6000")
    checkout_with_one_item.finish_checkout()

    # assertions before logout
    expect(checkout_with_one_item.page).to_have_url(
        checkout_with_one_item.URLS["checkout_done"]
    )

    # logout
    checkout_with_one_item.logout()

    # assertions after logout
    expect(checkout_with_one_item.page).to_have_url(checkout_with_one_item.MAIN_URL)
