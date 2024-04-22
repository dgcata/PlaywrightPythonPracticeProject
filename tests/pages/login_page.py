from playwright.sync_api import Page


class SauceDemoLoginPage:
    def __init__(self, page: Page) -> None:
        error_container_locator = '[class="error-message-container error"]'
        login_container_locator = '[data-test="login-container"]'

        self.page = page
        self.username_field = page.locator("#user-name")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_container = page.locator(error_container_locator)
        self.login_container = page.locator(login_container_locator)

    def navigate_to_login(self) -> None:
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str) -> None:
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()