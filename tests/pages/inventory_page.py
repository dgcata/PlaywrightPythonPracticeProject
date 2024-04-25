from pages.login_page import InvalidUsernameException, SauceDemoLoginPage
from playwright.sync_api import Locator, Page


class ItemDoesNotExistException(Exception):
    pass


class SauceDemoInventoryPage(SauceDemoLoginPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.shopping_cart = page.locator('[data-test="shopping-cart-link"]')
        self.sidebar_button = page.get_by_role("button", name="Open Menu")
        self.logout_button = page.locator('[data-test="logout-sidebar-link"]')

    def goto_inventory_as_user(self, username: str) -> None:
        if username not in self.VALID_USERNAMES:
            raise InvalidUsernameException(
                f"username '{username}' is an invalid username"
            )
        self.goto_login()
        self.login(username, self.PASSWORD)

    def goto_inventory_standard(self) -> None:
        self.goto_inventory_as_user("standard_user")

    def logout(self) -> None:
        self.sidebar_button.click()
        self.logout_button.click()

    def goto_cart(self) -> None:
        self.shopping_cart.click()

    def goto_item_page(self, item_id: int) -> None:
        self.__get_item_link(item_id).click()

    def add_item_to_cart(self, item_id: int) -> None:
        self.__get_add_to_cart_button(item_id).click()

    def remove_item_from_cart(self, item_id: int) -> None:
        self.__get_remove_from_cart_button(item_id).click()

    def __get_item_link(self, item_id: int) -> Locator:
        item_name = self.__get_item_name(item_id)
        item_link = self.page.get_by_role("link").filter(has_text=item_name)
        return item_link

    def __get_add_to_cart_button(self, item_id: int) -> Locator:
        item_name = self.__get_item_name(item_id)
        formatted_item_name = item_name.lower().replace(" ", "-")
        add_to_card_button = self.page.locator(
            f'[data-test="add-to-cart-{formatted_item_name}"]'
        )
        return add_to_card_button

    def __get_remove_from_cart_button(self, item_id: int) -> Locator:
        item_name = self.__get_item_name(item_id)
        formatted_item_name = item_name.lower().replace(" ", "-")
        remove_from_card_button = self.page.locator(
            f'[data-test="remove-{formatted_item_name}"]'
        )
        return remove_from_card_button

    def __get_item_name(self, item_id: int) -> str:
        try:
            item_name = self.VALID_ITEMS[item_id].item_name
            return item_name
        except KeyError:
            raise ItemDoesNotExistException(f"item with id '{item_id}' not found")
