import pytest
from playwright.sync_api import Page
from pages.login_page import SauceDemoLoginPage
from pages.products_page import SauceDemoProductsPage


@pytest.fixture
def login_page(page: Page) -> SauceDemoLoginPage:
    login_page = SauceDemoLoginPage(page)
    login_page.navigate_to_login()
    return login_page


@pytest.fixture
def product_page(page: Page) -> SauceDemoProductsPage:
    product_page = SauceDemoProductsPage(page)
    product_page.navigate_to_inventory_standard()
    return product_page
