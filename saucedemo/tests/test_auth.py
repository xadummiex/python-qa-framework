from playwright.sync_api import expect

from saucedemo.steps.catalog_steps import CatalogSteps
from saucedemo.steps.login_steps import LoginSteps
from saucedemo.utils.constants import Users


class TestAuth:
    def test_login_standard_user(self, login_steps: LoginSteps):
        login_steps.open_login_page().login(Users.standard_user_username, Users.password)

        catalog_steps = CatalogSteps(login_steps.page)
        assert catalog_steps.get_products_count() > 0, "Ожидаем товары на странице каталога"

    def test_login_locked_out_user(self, login_steps: LoginSteps):
        login_steps.open_login_page().login(Users.locked_out_user_username, Users.password)

        expect(login_steps.login_page.error_message).to_contain_text("locked out")

    def test_logout_standard_user(self, login_steps: LoginSteps):
        login_steps.open_login_page().login(Users.standard_user_username, Users.password)

        catalog_steps = CatalogSteps(login_steps.page)
        assert catalog_steps.get_products_count() > 0, "Ожидаем товары на странице каталога"

        catalog_steps.logout()

        expect(login_steps.login_page.login_button).to_be_visible()

    def test_logout_visual_user(self, login_steps: LoginSteps):
        login_steps.open_login_page().login(Users.visual_user_username, Users.password)

        catalog_steps = CatalogSteps(login_steps.page)
        assert catalog_steps.get_products_count() > 0, "Ожидаем товары на странице каталога"

        catalog_steps.logout()

        expect(login_steps.login_page.login_button).to_be_visible()
