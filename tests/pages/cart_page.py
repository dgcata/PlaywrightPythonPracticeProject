from playwright.sync_api import Page
from pages.products_page import SauceDemoProductsPage


class SauceDemoCartPage(SauceDemoProductsPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.continue_shopping_button = page.get_by_role('button').filter(
            has_text="Continue Shopping"
        )
        self.checkout_button = page.get_by_role('button').filter(
            has_text="Checkout"
        )
        self.cart_list = self.page.locator('[data-test="cart-list"]')

    def checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
