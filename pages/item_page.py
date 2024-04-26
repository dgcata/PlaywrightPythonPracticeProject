from playwright.sync_api import Page

from pages.inventory_page import SauceDemoInventoryPage


class SauceDemoItemPage(SauceDemoInventoryPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.back_to_products_button = page.locator('[data-test="back-to-products"]')
        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.item_price = page.locator('[data-test="inventory-item-price"]')
        self.item_image = page.locator('[class="inventory_details_img"]')
        self.item_description = page.locator('[data-test="inventory-item-desc"]')
        self.add_to_cart_button = page.locator('[data-test="add-to-cart"]')
        self.remove_button = page.locator('[data-test="remove"]')

    def go_back_to_inventory(self) -> None:
        self.back_to_products_button.click()

    def add_item_to_cart(self) -> None:  # type: ignore[override]
        self.add_to_cart_button.click()

    def remove_item_from_cart(self) -> None:  # type: ignore[override]
        self.remove_button.click()

    def goto_item_page(self, item_id: int) -> None:
        self.page.goto(f"https://www.saucedemo.com/inventory-item.html?id={item_id}")
