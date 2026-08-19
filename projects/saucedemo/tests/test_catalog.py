from saucedemo.steps.catalog_steps import CatalogSteps


class TestCatalog:

    def test_count_catalog(self, catalog_steps: CatalogSteps):
        assert catalog_steps.get_products_count() == 6, "Ожидаем 6 товаров в каталоге"

    def test_sorted_by_name(self, catalog_steps: CatalogSteps):
        catalog_steps.sort_items("az")

        names = catalog_steps.get_product_names()
        assert names == sorted(names), "Товары не отсортированы по имени A-Z"

    def test_sort_by_name_z_to_a(self, catalog_steps: CatalogSteps):
        catalog_steps.sort_items("za")

        names = catalog_steps.get_product_names()
        assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"

    def test_sort_by_price(self, catalog_steps: CatalogSteps):
        catalog_steps.sort_items("lohi")

        prices = catalog_steps.get_product_prices()
        assert prices == sorted(prices), "Товары не отсортированы по цене low → high"

        catalog_steps.sort_items("hilo")

        prices = catalog_steps.get_product_prices()
        assert prices == sorted(prices, reverse=True), "Товары не отсортированы по цене high → low"

    def test_add_to_cart(self, catalog_steps: CatalogSteps):
        catalog_steps.add_to_cart("Sauce Labs Bike Light")

        assert catalog_steps.get_cart_count() == 1, "Ожидаем 1 товар в корзине"

    def test_remove_from_cart(self, catalog_steps: CatalogSteps):
        catalog_steps.add_to_cart("Sauce Labs Onesie")
        assert catalog_steps.get_cart_count() == 1, "Ожидаем 1 товар в корзине"

        catalog_steps.remove_from_cart("Sauce Labs Onesie")
        assert catalog_steps.get_cart_count() == 0, "Ожидаем пустую корзину"

    def test_product_details_onesie(self, catalog_steps: CatalogSteps):
        name, price, detail_name, detail_price = catalog_steps.open_product_details(
            "Sauce Labs Onesie"
        )

        assert detail_name == name, "Название товара не совпадает"
        assert detail_price == price, "Цена товара не совпадает"

    def test_product_details_backpack(self, catalog_steps: CatalogSteps):
        name, price, detail_name, detail_price = catalog_steps.open_product_details(
            "Sauce Labs Backpack"
        )

        assert detail_name == name, "Название товара не совпадает"
        assert detail_price == price, "Цена товара не совпадает"

    def test_remove_item_from_catalog(self, catalog_steps: CatalogSteps):
        catalog_steps.add_to_cart("Test.allTheThings() T-Shirt (Red)")
        assert catalog_steps.get_cart_count() == 1, "Ожидаем 1 товар в корзине"

        catalog_steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
        assert catalog_steps.get_cart_count() == 0, "Ожидаем пустую корзину"

    def test_remove_onesie_from_catalog(self, catalog_steps: CatalogSteps):
        catalog_steps.add_to_cart("Sauce Labs Onesie")
        assert catalog_steps.get_cart_count() == 1, "Ожидаем 1 товар в корзине"

        catalog_steps.remove_from_cart("Sauce Labs Onesie")
        assert catalog_steps.get_cart_count() == 0, "Ожидаем пустую корзину"
