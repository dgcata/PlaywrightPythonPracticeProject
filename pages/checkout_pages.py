from playwright.sync_api import Page

from pages.cart_page import SauceDemoCartPage


class SauceDemoCheckoutPages(SauceDemoCartPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.checkout_info = page.locator(".checkout_info")
        self.first_name_field = page.locator('[data-test="firstName"]')
        self.last_name_field = page.locator('[data-test="lastName"]')
        self.postal_code_field = page.locator('[data-test="postalCode"]')

        self.cancel_button = page.locator('[data-test="cancel"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')

        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')

        self.complete_checkout_container = page.locator(
            '[data-test="checkout-complete-container"]'
        )
        self.back_to_home_button = page.locator('[data-test="back-to-products"]')
