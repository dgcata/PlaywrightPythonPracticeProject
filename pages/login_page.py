from playwright.sync_api import Page

from pages.base_page import SauceDemoBasePage


class InvalidUsernameException(Exception):
    pass


class SauceDemoLoginPage(SauceDemoBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_field = page.locator("#user-name")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.login_container = page.locator("#login_button_container")
        self.error_container = page.locator('[data-test="error"]')

    def goto_login(self) -> None:
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str) -> None:
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
