import sys
from dataclasses import dataclass
from decimal import Decimal

from playwright.sync_api import Page


@dataclass
class SauceDemoItem:
    item_name: str
    item_price: Decimal
    item_desc: str


class SauceDemoBasePage:
    # TODO: should all of these remain as class attributes
    # or should it be implemented as read-only object attributes
    MAIN_URL = "https://www.saucedemo.com/"
    URLS = {
        "inventory": MAIN_URL + "inventory.html",
        "item": MAIN_URL + "inventory-item.html?id={}",
        "cart": MAIN_URL + "cart.html",
        "checkout_one": MAIN_URL + "checkout-step-one.html",
        "checkout_two": MAIN_URL + "checkout-step-two.html",
        "checkout_done": MAIN_URL + "checkout-complete.html",
    }
    VALID_USERNAMES = [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ]
    PASSWORD = "secret_sauce"
    VALID_ITEMS = {
        0: SauceDemoItem(
            item_name="Sauce Labs Bike Light",
            item_price=Decimal("9.99"),
            item_desc="A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        ),
        1: SauceDemoItem(
            item_name="Sauce Labs Bolt T-Shirt",
            item_price=Decimal("15.99"),
            item_desc="Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        ),
        2: SauceDemoItem(
            item_name="Sauce Labs Onesie",
            item_price=Decimal("7.99"),
            item_desc="Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        ),
        3: SauceDemoItem(
            item_name="Test.allTheThings() T-Shirt (Red)",
            item_price=Decimal("15.99"),
            item_desc="This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        ),
        4: SauceDemoItem(
            item_name="Sauce Labs Backpack",
            item_price=Decimal("29.99"),
            item_desc="carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        ),
        5: SauceDemoItem(
            item_name="Sauce Labs Fleece Jacket",
            item_price=Decimal("49.99"),
            item_desc="It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        ),
    }
    INVALID_ITEM = SauceDemoItem(
        item_name="ITEM NOT FOUND",
        item_price=Decimal("-1"),
        item_desc="We're sorry, but your call could not be completed as dialled. Please check your number, and try your call again. If you are in need of assistance, please dial 0 to be connected with an operator. This is a recording. 4 T 1.",
    )
    TAX_RATE = Decimal("0.08")

    def __init__(self, page: Page) -> None:
        self.page = page

        # emulate `npx playwright test --debug`
        # from JavaScript, to use run the following
        # command: `python -m pytest --headed --debug`
        # NOTE: flag '--headed' is neccessary
        if "--debug" in sys.argv:
            self.pause()

    def pause(self) -> None:
        self.page.pause()
