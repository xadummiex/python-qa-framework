import pytest
from playwright.sync_api import sync_playwright, Page

from saucedemo.steps.basket_steps import BasketSteps
from saucedemo.steps.catalog_steps import CatalogSteps
from saucedemo.steps.checkout_steps import CheckoutSteps
from saucedemo.steps.login_steps import LoginSteps
from saucedemo.utils.constants import Users


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def login_steps(page: Page) -> LoginSteps:
    """Шаги логина на чистой странице для тестов авторизации"""
    return LoginSteps(page)


@pytest.fixture(scope="function")
def standard_user_page(page: Page) -> Page:
    """Предусловие: залогинены под standard_user, открыт каталог"""
    LoginSteps(page).open_login_page().login(Users.standard_user_username, Users.password)
    return page


@pytest.fixture(scope="function")
def catalog_steps(standard_user_page: Page) -> CatalogSteps:
    return CatalogSteps(standard_user_page)


@pytest.fixture(scope="function")
def basket_steps(standard_user_page: Page) -> BasketSteps:
    return BasketSteps(standard_user_page)


@pytest.fixture(scope="function")
def checkout_steps(standard_user_page: Page) -> CheckoutSteps:
    return CheckoutSteps(standard_user_page)
