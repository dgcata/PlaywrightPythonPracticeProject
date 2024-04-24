from playwright.sync_api import Page


class InvalidUsernameException(Exception):
    pass


class SauceDemoLoginPage:
    VALID_USERNAMES = [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ]
    PASSWORD = "secret_sauce"

    def __init__(self, page: Page) -> None:
        self.page = page
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
