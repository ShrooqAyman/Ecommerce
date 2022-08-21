from django.test import TestCase
from store.models import Category, Product

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='Computer',slug='computer')

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))  

    def test_category_model_entry(self):
        """
        test category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'computer')