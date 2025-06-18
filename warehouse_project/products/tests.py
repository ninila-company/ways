from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            zone=1
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.zone, 1)
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(str(self.product), "Test Product")

    def test_slug_generation(self):
        # Test automatic slug generation
        product = Product.objects.create(
            name="Another Test Product",
            zone=2
        )
        self.assertEqual(product.slug, "another-test-product")

        # Test slug with special characters (should be unique)
        product = Product.objects.create(
            name="Test & Product!",
            zone=3
        )
        self.assertEqual(product.slug, "test-product-1")

        # Test slug with Russian characters
        product = Product.objects.create(
            name="Тестовый Продукт",
            zone=4
        )
        self.assertEqual(product.slug, "testovyi-produkt")

    def test_unique_slug(self):
        # Create first product
        Product.objects.create(
            name="Unique Product",
            zone=5
        )

        # Try to create second product with same name (should have different slug)
        product2 = Product.objects.create(
            name="Unique Product",
            zone=6
        )
        self.assertEqual(product2.slug, "unique-product-1")

        # Try to create third product with same name
        product3 = Product.objects.create(
            name="Unique Product",
            zone=7
        )
        self.assertEqual(product3.slug, "unique-product-2")

    def test_zone_validation(self):
        # Test that zone can be any integer
        product = Product.objects.create(
            name="Product with Zone",
            zone=999
        )
        self.assertEqual(product.zone, 999)

    def test_name_validation(self):
        # Test that name can't be empty
        product = Product(name="", zone=1)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_verbose_names(self):
        self.assertEqual(Product._meta.verbose_name, "Товар")
        self.assertEqual(Product._meta.verbose_name_plural, "Товары")
