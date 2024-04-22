import pytest
from playwright.sync_api import Page, expect

from pages.login_page import SauceDemoLoginPage


def test_successful_load(page: Page) -> None:
    login_page = SauceDemoLoginPage(page)
    login_page.navigate_to_login()

    expect(login_page.login_container).to_be_visible()
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")


@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ],
)
def test_successful_login(page: Page, username: str) -> None:
    login_page = SauceDemoLoginPage(page)
    login_page.navigate_to_login()

    login_page.login(username, "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        # wrong passwords
        (
            "standard_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "locked_out_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "problem_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "performance_glitch_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "error_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "visual_user",
            "wrong_password",
            "do not match any user in this service",
        ),
        (
            "standard_user",
            "different_password",
            "do not match any user in this service",
        ),
        # unregistered user
        (
            "not_a_user",
            "secret_sauce",
            "do not match any user in this service",
        ),
        (
            "not_a_user",
            "different_password",
            "do not match any user in this service",
        ),
        # locked out user
        (
            "locked_out_user",
            "secret_sauce",
            "Sorry, this user has been locked out",
        ),
        # empty fields
        ("", "", "Username is required"),
        ("", "test", "Username is required"),
        ("test", "", "Password is required"),
    ],
)
def test_failing_login(
    page: Page, username: str, password: str, expected_message: str
) -> None:
    login_page = SauceDemoLoginPage(page)
    login_page.navigate_to_login()

    expect(login_page.error_container).not_to_be_visible()

    login_page.login(username, password)

    expect(login_page.error_container).to_be_visible()
    expect(login_page.error_container).to_contain_text(expected_message)