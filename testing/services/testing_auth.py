from unittest import TestCase
from unittest.mock import Mock , patch
import builtins
from controller.control_auth import AuthService
from database.db_initialize import Database
from models.models_user import User

class Testing(TestCase):

    def setUp(self):
       self.db = Mock()
       self.auth = AuthService(self.db)

    def test_verify_user_none(self):
        self.db.fetch_item.return_value = None
        username = "anonymous"
        result = self.auth.service_verify_user(username)
        self.assertIsNone(result)

    def test_verify_user_valid(self):
            user = User(1, "samarth", "hashed_password", "USER")
            self.db.fetch_item.return_value = user
            username = "anonymous"
            result = self.auth.service_verify_user(username)
            self.assertEqual(result , user)

    def test_add_user_false(self):
        self.db.add_item.return_value = None
        result = self.auth.service_add_user("samarth" , "hashed_password" , "USER")
        self.assertEqual(result , False)

    def test_add_user_True(self):
            self.db.add_item.return_value = True
            result = self.auth.service_add_user("samarth" , "hashed_password" , "USER")
            self.assertEqual(result , True)


