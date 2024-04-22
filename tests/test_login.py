import pytest
from playwright.sync_api import Page, expect


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
    page.goto("https://www.saucedemo.com/")

    username_field = page.locator("#user-name")
    password_field = page.locator("#password")
    login_button = page.locator("#login-button")

    username_field.fill(username)
    password_field.fill("secret_sauce")
    login_button.click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.parametrize(
    "username, password",
    [
        ("standard_user", "wrong_password"),
        ("locked_out_user", "wrong_password"),
        ("problem_user", "wrong_password"),
        ("performance_glitch_user", "wrong_password"),
        ("error_user", "wrong_password"),
        ("visual_user", "wrong_password"),
    ],
)
def test_failing_login(page: Page, username: str, password: str) -> None:
    page.goto("https://www.saucedemo.com/")

    username_field = page.locator("#user-name")
    password_field = page.locator("#password")
    login_button = page.locator("#login-button")
    error_locator = '[class="error-message-container error"]'
    error_container = page.locator(error_locator)

    expect(error_container).not_to_be_visible()

    username_field.fill(username)
    password_field.fill(password)
    login_button.click()

    expect(error_container).to_be_visible()
