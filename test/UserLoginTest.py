import unittest
from unittest.mock import patch
from services.UserLogin import process_login
import bcrypt


class UserLoginTest(unittest.TestCase):

    @patch('services.UserLogin.collection.find_one')
    def test_process_login_valid(self, mock_find_one):
        mock_find_one.return_value = {
            'login_id': 'test_user',
            'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }
        login_id = 'test_user'
        password = 'password123'
        self.assertEqual(process_login(login_id, password), 'test_user')

    @patch('services.UserLogin.collection.find_one')
    def test_process_login_invalid_user(self, mock_find_one):
        mock_find_one.return_value = None
        login_id = 'non_existing_user'
        password = 'password123'
        with self.assertRaises(ValueError):
            process_login(login_id, password)

    @patch('services.UserLogin.collection.find_one')
    def test_process_login_invalid_password(self, mock_find_one):
        mock_find_one.return_value = {
            'login_id': 'test_user',
            'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        }
        login_id = 'test_user'
        password = 'wrong_password'
        with self.assertRaises(ValueError):
            process_login(login_id, password)

if __name__ == '__main__':
    unittest.main()