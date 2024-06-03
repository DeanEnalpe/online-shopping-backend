import unittest
from unittest.mock import patch
from services.UserCreation import (
    validate_first_name, validate_last_name, validate_login_id,
    validate_email, validate_password, validate_confirm_password,
    validate_contact_number, save_account
)
from model.User import User
import bcrypt


class UserCreationTest(unittest.TestCase):

    @patch('services.UserCreation.collection.count_documents')
    def test_validate_first_name(self, mock_count_documents):
        self.assertEqual(validate_first_name('John_Doe'), 'Valid!')
        with self.assertRaises(ValueError):
            validate_first_name('J')

    @patch('services.UserCreation.collection.count_documents')
    def test_validate_last_name(self, mock_count_documents):
        self.assertEqual(validate_last_name('Doe_John'), 'Valid!')
        with self.assertRaises(ValueError):
            validate_last_name('D')

    @patch('services.UserCreation.collection.count_documents')
    def test_validate_login_id(self, mock_count_documents):
        mock_count_documents.return_value = 0
        self.assertEqual(validate_login_id('user123'), 'Valid!')
        mock_count_documents.return_value = 1
        with self.assertRaises(ValueError):
            validate_login_id('user123')

    @patch('services.UserCreation.collection.count_documents')
    def test_validate_email(self, mock_count_documents):
        mock_count_documents.return_value = 0
        self.assertIsNone(validate_email('test.test@example.com'))
        mock_count_documents.return_value = 1
        with self.assertRaises(ValueError):
            validate_email('test.test@example.com')

    def test_validate_password(self):
        self.assertIsNone(validate_password('Password123!'))
        with self.assertRaises(ValueError):
            validate_password('short')

    def test_validate_confirm_password(self):
        self.assertIsNone(validate_confirm_password('Password123!', 'Password123!'))
        with self.assertRaises(ValueError):
            validate_confirm_password('Password123!', 'Password124!')

    def test_validate_contact_number(self):
        self.assertIsNone(validate_contact_number('09123456789'))
        with self.assertRaises(ValueError):
            validate_contact_number('0912345678')

    @patch('services.UserCreation.collection.insert_one')
    @patch('services.UserCreation.collection.find_one')
    def test_save_account(self, mock_find_one, mock_insert_one):
        mock_insert_one.return_value.inserted_id = '12345'
        mock_find_one.return_value = {
            'first_name': 'John',
            'last_name': 'Doee',
            'login_id': 'johndoe',
            'email': 'john.doe@example.com',
            'password': bcrypt.hashpw('Password123!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'contact_number': '09123456789',
            'confirm_password': 'Password123!'
        }

        user = User(
            first_name='John',
            last_name='Doee',
            login_id='johndoe',
            email='john.doe@example.com',
            password='Password123!',
            contact_number='09123456789',
            confirm_password='Password123!'
        )

        result = save_account(user)

        mock_insert_one.assert_called_once_with(user.convert_to_json())
        mock_find_one.assert_called_once_with({"_id": '12345'})
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, 'John')


if __name__ == '__main__':
    unittest.main()