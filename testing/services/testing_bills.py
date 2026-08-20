from unittest import TestCase
from unittest.mock import Mock , patch , call
from services.service_bills import BillService
import database.queries as query

class TestingBills(TestCase):

    def setUp(self):
        self.db = Mock()
        self.bill = BillService(self.db)

    def test_add_bill(self):
        self.db.add_item.return_value = True
        args = (3 , "23:45" , 100 , 24 , 1000)
        self.bill.service_add_bill(args)
        self.db.add_item.assert_called_once_with(query.ADD_BILL , args)

    def test_view_all_bills_none(self):
        self.db.fetch_all_items.return_value = False
        result = self.bill.service_view_all_bills(2)
        self.assertIsNone(result)

    @patch("builtins.input")
    def test_view_all_bills_none(self, mock_input):
        bills = [(1, 2, "23:59", 100, 30, 1000)]
        self.db.fetch_all_items.side_effect = [bills, None]
        mock_input.return_value = "Y"
        result = self.bill.service_view_all_bills(2)
        self.assertTrue(result)
        mock_input.assert_called_with("Show More? (Y/N)\n---->")
        self.db.fetch_all_items.assert_has_calls([call(query.VIEW_BILLS, 2, 10, 0),call(query.VIEW_BILLS, 2, 10, 10)])

