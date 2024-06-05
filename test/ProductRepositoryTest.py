import unittest
from unittest.mock import patch
from services.ProductsRepository import products_to_dictionary, find_all_products, find_product, save_product
from model.Products import FSEProducts
import pandas as pd


class ProductRepositoryTest(unittest.TestCase):

    @patch('services.ProductsRepository.os.path.exists')
    @patch('services.ProductsRepository.pd.read_csv')
    @patch('services.ProductsRepository.collection.insert_many')
    def test_products_to_dictionary(self, mock_insert_many, mock_read_csv, mock_exists):
        mock_exists.return_value = True
        mock_data = pd.DataFrame([{
            'product_name': 'Test Product',
            'product_description': 'Description',
            'price': '10.00',
            'features': 'Feature1, Feature2',
            'quantity': 10,
            'product_status': 'HURRY UP TO PURCHASE'
        }])
        mock_read_csv.return_value = mock_data

        products_to_dictionary()

        mock_read_csv.assert_called_once_with('/app/resources/new_products.csv')
        mock_insert_many.assert_called_once()

    @patch('services.ProductsRepository.collection.find')
    @patch('services.ProductsRepository.collection.count_documents')
    @patch('services.ProductsRepository.products_to_dictionary')
    def test_find_all_products(self, mock_products_to_dictionary, mock_count_documents, mock_find):
        mock_count_documents.return_value = 1
        mock_find.return_value = [{
            'product_name': 'Test Product',
            'product_description': 'Description',
            'price': '10.00',
            'features': 'Feature1, Feature2',
            'quantity': 10,
            'product_status': 'HURRY UP TO PURCHASE'
        }]

        result = find_all_products()

        mock_find.assert_called_once_with({}, {"_id": 0})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['product_name'], 'Test Product')

    @patch('services.ProductsRepository.collection.find_one')
    @patch('services.ProductsRepository.collection.count_documents')
    @patch('services.ProductsRepository.products_to_dictionary')
    def test_find_product(self, mock_products_to_dictionary, mock_count_documents, mock_find_one):
        mock_find_one.return_value = {
            'product_name': 'Test Product',
            'product_description': 'Description',
            'price': '10.00',
            'features': 'Feature1, Feature2',
            'quantity': 10,
            'product_status': 'HURRY UP TO PURCHASE'
        }

        result = find_product('Test Product')

        mock_find_one.assert_called_once_with({"product_name": 'Test Product'}, {"_id": 0})
        self.assertIsNotNone(result)
        self.assertEqual(result['product_status'], 'HURRY UP TO PURCHASE')

    @patch('services.ProductsRepository.collection.insert_one')
    @patch('services.ProductsRepository.collection.find_one')
    def test_save_product(self, mock_find_one, mock_insert_one):
        mock_insert_one.return_value.inserted_id = '12345'
        mock_find_one.return_value = {
            'product_name': 'Test Product',
            'product_description': 'Description',
            'price': '10.00',
            'features': 'Feature1, Feature2',
            'quantity': 10,
            'product_status': 'HURRY UP TO PURCHASE'
        }

        product = FSEProducts(
            product_name='Test Product',
            product_description='Description',
            price='10.00',
            features='Feature1, Feature2',
            quantity=10,
            product_status='HURRY UP TO PURCHASE'
        )

        result = save_product(product)

        mock_insert_one.assert_called_once_with(product.convert_to_json())
        mock_find_one.assert_called_once_with({"_id": '12345'})
        self.assertIsNotNone(result)
        self.assertEqual(result.product_name, 'Test Product')


if __name__ == '__main__':
    unittest.main()