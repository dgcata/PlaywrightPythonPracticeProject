import pytest
from playwright.sync_api import Page

from pages.base_page import SauceDemoBasePage


@pytest.mark.parametrize(
    "attribute_name",
    [
        "MAIN_URL",
        "URLS",
        "VALID_USERS",
        "LOCKED_OUT_USER",
        "PASSWORD",
        "VALID_ITEMS",
        "INVALID_ITEM",
        "TAX_RATE",
    ],
)
def test_can_not_change_class_attributes(page: Page, attribute_name: str) -> None:
    base_page = SauceDemoBasePage(page)

    # use built-in setattr function
    with pytest.raises(Exception) as e1:
        setattr(base_page, attribute_name, "lorem_ipsum")
    assert e1.type == AttributeError
    assert attribute_name in str(e1.value)

    # use built-in __setattr__ method in classes
    with pytest.raises(Exception) as e2:
        base_page.__setattr__(attribute_name, "lorem_ipsum")
    assert e2.type == AttributeError
    assert attribute_name in str(e2.value)
