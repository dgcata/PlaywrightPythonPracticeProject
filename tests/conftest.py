import pytest
from pages.login_page import SauceDemoLoginPage
from playwright.sync_api import Page


@pytest.fixture
def login_page(page: Page) -> SauceDemoLoginPage:
    login_page = SauceDemoLoginPage(page)
    login_page.navigate_to_login()
    return login_page
