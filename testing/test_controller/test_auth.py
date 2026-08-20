from unittest import TestCase
from unittest.mock import Mock , patch
import builtins
from controller.control_auth import AuthController
from database.db_initialize import Database

class TestingAuth(TestCase):

    def setUp(self):
        self.db = Mock()
        self.auth = AuthController(self.db)


    @patch("builtins.input")
    @patch("controller.control_auth.int_1_2_checker")
    def test_login_register_out_of_range_register(self, mock_checker, mock_input):
        mock_input.side_effect = ["3", "2"]
        mock_checker.side_effect = [False, True]
        self.auth.register = Mock()
        self.auth.User_Authentication()
        self.assertEqual(mock_input.call_count, 2)
        mock_checker.assert_any_call("3")
        mock_checker.assert_any_call("2")
        self.auth.register.assert_called_once()


    @patch("builtins.input")
    @patch("controller.control_auth.int_1_2_checker")
    def test_login_register_out_of_range_login(self, mock_checker, mock_input):
        mock_input.side_effect = ["3", "1"]
        mock_checker.side_effect = [False, True]
        self.auth.login = Mock()
        self.auth.User_Authentication()
        self.assertEqual(mock_input.call_count, 2)
        mock_checker.assert_any_call("3")
        mock_checker.assert_any_call("1")
        self.auth.login.assert_called_once()


    @patch("builtins.input")
    @patch("controller.control_auth.int_1_2_checker")
    def test_login_register_login(self, mock_checker, mock_input):
        mock_input.return_value = "1"
        mock_checker.return_value = True
        self.auth.login = Mock()
        self.auth.User_Authentication()
        self.assertEqual(mock_input.call_count, 1)
        mock_checker.assert_any_call("1")
        self.auth.login.assert_called_once()


    @patch("builtins.input")
    @patch("controller.control_auth.int_1_2_checker")
    def test_login_register_register(self, mock_checker, mock_input):
        mock_input.return_value = "2"
        mock_checker.return_value = True
        self.auth.register = Mock()
        self.auth.User_Authentication()
        self.assertEqual(mock_input.call_count, 1)
        mock_checker.assert_any_call("2")
        self.auth.register.assert_called_once()
        

    

    