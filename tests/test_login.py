from playwright.sync_api import Page, expect


def test_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    username_field = page.locator("#user-name")
    password_field = page.locator("#password")
    login_button = page.get_by_role("button")

    username_field.fill("standard_user")
    password_field.fill("secret_sauce")
    login_button.click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
