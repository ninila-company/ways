from django.test import TestCase
from django.utils import timezone
from .models import Poducts_in_palet, Palet, Poducts_in_palet_quantity


class PoductsInPaletModelTest(TestCase):
    def setUp(self):
        self.product = Poducts_in_palet.objects.create(
            product_name="Test Product"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "Test Product")
        self.assertEqual(str(self.product), "Test Product")


class PaletModelTest(TestCase):
    def setUp(self):
        self.palet = Palet.objects.create(
            number=1,
            pallets_from_the_date=timezone.now().date(),
            receipt_mark=False
        )

    def test_palet_creation(self):
        self.assertEqual(self.palet.number, 1)
        self.assertFalse(self.palet.receipt_mark)
        self.assertIsNone(self.palet.pallet_pick_up_date)
        self.assertEqual(str(self.palet), "1")

    def test_get_products_list_empty(self):
        self.assertEqual(self.palet.get_products_list(), "")

    def test_get_products_list_with_products(self):
        product = Poducts_in_palet.objects.create(product_name="Test Product")
        Poducts_in_palet_quantity.objects.create(
            palet=self.palet,
            product=product,
            quantity=5
        )
        expected_output = "Test Product - 5 шт."
        self.assertEqual(self.palet.get_products_list(), expected_output)


class PoductsInPaletQuantityModelTest(TestCase):
    def setUp(self):
        self.product = Poducts_in_palet.objects.create(
            product_name="Test Product"
        )
        self.palet = Palet.objects.create(
            number=1,
            pallets_from_the_date=timezone.now().date()
        )
        self.product_quantity = Poducts_in_palet_quantity.objects.create(
            palet=self.palet,
            product=self.product,
            quantity=5
        )

    def test_product_quantity_creation(self):
        self.assertEqual(self.product_quantity.palet, self.palet)
        self.assertEqual(self.product_quantity.product, self.product)
        self.assertEqual(self.product_quantity.quantity, 5)
        self.assertEqual(str(self.product_quantity), "Test Product - 5 шт.")

    def test_default_quantity(self):
        new_product_quantity = Poducts_in_palet_quantity.objects.create(
            palet=self.palet,
            product=self.product
        )
        self.assertEqual(new_product_quantity.quantity, 1)

    def test_positive_quantity(self):
        with self.assertRaises(Exception):
            Poducts_in_palet_quantity.objects.create(
                palet=self.palet,
                product=self.product,
                quantity=-1
            )
