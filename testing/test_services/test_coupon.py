from unittest import TestCase
from unittest.mock import Mock , patch , call
from services.service_coupon import CouponService
import database.queries as query


class TestingCoupons(TestCase):

    def setUp(self):
        self.db = Mock()
        self.coupon = CouponService(self.db)

    def test_add_coupon_already_exists(self):
        self.db.add_item.return_value = False
        result = self.coupon.service_add_coupon("SAVE10" , 10)
        self.assertFalse(result)
        self.db.add_item.assert_called_once_with(query.ADD_COUPON , "SAVE10" , 10)

    def test_add_coupon_success(self):
        self.db.add_item.return_value = True
        result = self.coupon.service_add_coupon("SAVE10" , 10)
        self.assertTrue(result)
        self.db.add_item.assert_called_once_with(query.ADD_COUPON , "SAVE10" , 10)

    def test_delete_coupon_not_found(self):
        self.db.update_item.return_value = False
        result = self.coupon.service_delete_coupon("SAVE10")
        self.assertFalse(result)
        self.db.update_item.assert_called_once_with(query.DELETE_COUPON , "SAVE10")

    def test_delete_coupon_success(self):
        self.db.update_item.return_value = True
        result = self.coupon.service_delete_coupon("SAVE10")
        self.assertTrue(result)
        self.db.update_item.assert_called_once_with(query.DELETE_COUPON , "SAVE10")

    def test_view_coupon_none(self):
        self.db.fetch_all_items.return_value = False
        result = self.coupon.service_view_coupon()
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(query.VIEW_COUPON , 10 , 0)

    @patch("builtins.input")
    def test_view_coupon_pagination_then_stop(self, mock_input):
        coupons = [("SAVE10", 10)]
        self.db.fetch_all_items.side_effect = [coupons, None]
        mock_input.return_value = "Y"
        result = self.coupon.service_view_coupon()
        self.assertIsNone(result)
        mock_input.assert_called_with("View More? (Y/N)\n----->")
        self.db.fetch_all_items.assert_has_calls([call(query.VIEW_COUPON, 10, 0),call(query.VIEW_COUPON, 10, 10)])

    @patch("builtins.input")
    def test_view_coupon_user_stops(self, mock_input):
        coupons = [("SAVE10", 10)]
        self.db.fetch_all_items.return_value = coupons
        mock_input.return_value = "N"
        result = self.coupon.service_view_coupon()
        self.assertIsNone(result)
        mock_input.assert_called_once_with("View More? (Y/N)\n----->")
        self.db.fetch_all_items.assert_called_once_with(query.VIEW_COUPON , 10 , 0)

    def test_verify_coupon_invalid(self):
        self.db.fetch_item.return_value = None
        result = self.coupon.service_verify_coupon("SAVE10")
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(query.VERIFY_COUPON , "SAVE10")

    def test_verify_coupon_valid(self):
        self.db.fetch_item.return_value = ("SAVE10" , 10)
        result = self.coupon.service_verify_coupon("SAVE10")
        self.assertIsNotNone(result)
        self.db.fetch_item.assert_called_once_with(query.VERIFY_COUPON , "SAVE10")