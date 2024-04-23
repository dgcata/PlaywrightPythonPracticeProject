from playwright.sync_api import Page
from pages.products_page import SauceDemoProductsPage


class SauceDemoCartPage(SauceDemoProductsPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.continue_shopping = page.get_by_role('button').filter(
            has_text="Continue Shopping"
        )
        self.checkout = page.get_by_role('button').filter(
            has_text="Checkout"
        )
