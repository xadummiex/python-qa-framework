from playwright.sync_api import expect

from saucedemo.steps.basket_steps import BasketSteps
from saucedemo.steps.catalog_steps import CatalogSteps
from saucedemo.steps.checkout_steps import CheckoutSteps


class TestBasket:

    def test_add_item_and_check_in_cart(self, catalog_steps: CatalogSteps, basket_steps: BasketSteps):
        catalog_steps.add_to_cart("Sauce Labs Backpack")

        basket_steps.open_cart().expect_item_in_cart("Sauce Labs Backpack")

    def test_add_items_and_check_in_cart(self, catalog_steps: CatalogSteps, basket_steps: BasketSteps):
        catalog_steps.add_to_cart("Sauce Labs Onesie")
        catalog_steps.add_to_cart("Sauce Labs Bike Light")

        basket_steps.open_cart()
        basket_steps.expect_item_in_cart("Sauce Labs Onesie")
        basket_steps.expect_item_in_cart("Sauce Labs Bike Light")

    def test_remove_item_from_cart(self, catalog_steps: CatalogSteps, basket_steps: BasketSteps):
        catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")

        basket_steps.open_cart().expect_item_in_cart("Sauce Labs Fleece Jacket")
        basket_steps.remove_item("Sauce Labs Fleece Jacket")
        basket_steps.expect_item_not_in_cart("Sauce Labs Fleece Jacket")

    def test_checkout_multiple_items(self, catalog_steps: CatalogSteps,
                                     basket_steps: BasketSteps, checkout_steps: CheckoutSteps):
        catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")
        catalog_steps.add_to_cart("Sauce Labs Bolt T-Shirt")

        basket_steps.open_cart()
        basket_steps.expect_item_in_cart("Sauce Labs Fleece Jacket")
        basket_steps.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

        expected_total = basket_steps.get_items_total_price()

        basket_steps.checkout()
        checkout_steps.start_checkout("A", "K", "000")

        item_total = checkout_steps.get_item_total_after_continue()
        assert item_total == expected_total, \
            f"Item total {item_total} не совпадает с суммой товаров {expected_total}"

        checkout_steps.finish_checkout()

        expect(checkout_steps.checkout.success_message).to_have_text("Thank you for your order!")

    def test_checkout_without_items(self, catalog_steps: CatalogSteps,
                                    basket_steps: BasketSteps, checkout_steps: CheckoutSteps):
        catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")

        basket_steps.open_cart().expect_item_in_cart("Sauce Labs Fleece Jacket")
        basket_steps.checkout()

        checkout_steps.start_checkout("NewUser", "Nrk", "")

        expect(checkout_steps.checkout.error_message).to_have_text("Error: Postal Code is required")
