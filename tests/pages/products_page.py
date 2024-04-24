from playwright.sync_api import Page, ElementHandle
from pages.login_page import InvalidUsernameException, SauceDemoLoginPage


class InvalidItemName(Exception):
    pass


class SauceDemoProductsPage(SauceDemoLoginPage):
    VALID_ITEMS = {
        0: "Sauce Labs Bike Light",
        1: "Sauce Labs Bolt T-Shirt",
        2: "Sauce Labs Onesie",
        3: "Test.allTheThings() T-Shirt (Red)",
        4: "Sauce Labs Backpack",
        5: "Sauce Labs Fleece Jacket",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.inventory_container = page.locator(
            '[data-test="inventory-container"]'
        )
        self.shopping_cart = page.locator(
            '[data-test="shopping-cart-link"]'
        )
        self.sidebar_button = page.get_by_role(
            "button", name="Open Menu"
        )
        self.logout_button = page.locator(
            '[data-test="logout-sidebar-link"]'
        )

    def navigate_to_inventory_as_user(self, username: str) -> None:
        if username not in self.VALID_USERNAMES:
            raise InvalidUsernameException(
                f"username '{username}' is an invalid username"
            )
        self.navigate_to_login()
        self.login(username, self.PASSWORD)

    def navigate_to_inventory_standard(self) -> None:
        self.navigate_to_inventory_as_user("standard_user")

    def logout(self) -> None:
        self.sidebar_button.click()
        self.logout_button.click()

    def goto_cart(self) -> None:
        self.shopping_cart.click()

    def goto_item_page(self, item_name: str) -> None:
        self.__get_item_link(item_name).click()

    def add_item_to_cart(self, item_name: str) -> None:
        self.__get_add_to_cart_button(item_name).click()

    def remove_item_from_cart(self, item_name: str) -> None:
        self.__get_remove_from_cart_button(item_name).click()

    def __get_item_link(self, item_name: str) -> ElementHandle:
        self.__check_item_name(item_name)
        item_link = self.page.get_by_role("link").filter(
            has_text=item_name
        )
        return item_link

    def __get_add_to_cart_button(self, item_name: str) -> ElementHandle:
        self.__check_item_name(item_name)
        item_name = item_name.lower().replace(" ", "-")
        add_to_card_button = self.page.locator(
            f'[data-test="add-to-cart-{item_name}"]'
        )
        return add_to_card_button

    def __get_remove_from_cart_button(self, item_name: str) -> ElementHandle:
        self.__check_item_name(item_name)
        item_name = item_name.lower().replace(" ", "-")
        remove_from_card_button = self.page.locator(
            f'[data-test="remove-{item_name}"]'
        )
        return remove_from_card_button

    def __check_item_name(self, item_name: str) -> None:
        if item_name not in self.VALID_ITEMS.values():
            raise InvalidItemName(
                f"item '{item_name}' is not a valid item"
            )
