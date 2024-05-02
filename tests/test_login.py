import pytest
from playwright.sync_api import expect

from pages.login_page import SauceDemoLoginPage


def test_successful_load(login_page: SauceDemoLoginPage) -> None:
    expect(login_page.login_container).to_be_visible()
    expect(login_page.page).to_have_url(login_page.MAIN_URL)
    expect(login_page.page).to_have_title(login_page.PAGE_TITLE)


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
def test_successful_login(login_page: SauceDemoLoginPage, username: str) -> None:
    login_page.login(username, "secret_sauce")

    expect(login_page.page).to_have_url(login_page.URLS["inventory"])


@pytest.mark.parametrize(
    "username, password, error_msg",
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
        # unregistered user
        (
            "not_a_user",
            "secret_sauce",
            "do not match any user in this service",
        ),
        # misspelled user
        (
            "standarduser",
            "secret_sauce",
            "do not match any user in this service",
        ),
        # case-sensitivity
        (
            # first letter in username is upper case
            "Standard_user",
            "secret_sauce",
            "do not match any user in this service",
        ),
        (
            # first letter in password is upper case
            "standard_user",
            "Secret_sauce",
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
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
)
def test_failing_login(
    login_page: SauceDemoLoginPage,
    username: str,
    password: str,
    error_msg: str,
) -> None:
    expect(login_page.error_container).not_to_be_visible()
    login_page.login(username, password)

    expect(login_page.error_container).to_be_visible()
    expect(login_page.error_container).to_contain_text(error_msg)
