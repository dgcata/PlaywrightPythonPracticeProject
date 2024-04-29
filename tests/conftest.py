import pytest
from playwright.sync_api import Page

from pages.cart_page import SauceDemoCartPage
from pages.checkout_pages import SauceDemoCheckoutPages
from pages.inventory_page import SauceDemoInventoryPage
from pages.item_page import SauceDemoItemPage
from pages.login_page import SauceDemoLoginPage


@pytest.fixture
def login_page(page: Page) -> SauceDemoLoginPage:
    login_page = SauceDemoLoginPage(page)
    login_page.goto_login()
    return login_page


@pytest.fixture
def inventory_page(page: Page) -> SauceDemoInventoryPage:
    inventory_page = SauceDemoInventoryPage(page)
    inventory_page.goto_inventory_standard()
    return inventory_page


@pytest.fixture
def item_page(page: Page) -> SauceDemoItemPage:
    item_page = SauceDemoItemPage(page)
    return item_page


@pytest.fixture
def cart_page(page: Page) -> SauceDemoCartPage:
    cart_page = SauceDemoCartPage(page)
    return cart_page


@pytest.fixture
def checkout_pages(page: Page) -> SauceDemoCheckoutPages:
    checkout_pages = SauceDemoCheckoutPages(page)
    return checkout_pages


@pytest.fixture
def inventory_page__buy_all(
    inventory_page: SauceDemoInventoryPage,
) -> SauceDemoInventoryPage:
    for item_id in inventory_page.VALID_ITEMS:
        inventory_page.add_item_to_cart(item_id)
    return inventory_page


@pytest.fixture
def fleece_jacket_item_page(
    inventory_page: SauceDemoInventoryPage,
) -> SauceDemoItemPage:
    inventory_page.goto_item_page(5)
    item_page = SauceDemoItemPage(inventory_page.page)
    return item_page
