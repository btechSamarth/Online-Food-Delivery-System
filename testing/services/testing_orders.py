from unittest import TestCase
from unittest.mock import Mock
from services.service_orders import OrderService
import database.queries as query


class TestingOrders(TestCase):

    def setUp(self):
        self.db = Mock()
        self.order = OrderService(self.db)

    def test_create_order(self):
        args = (2 , 3 , 500 , "PLACED")
        result = self.order.service_create_order(*args)
        self.assertTrue(result)
        self.db.add_item.assert_called_once_with(query.CREATE_ORDER , *args)

    def test_get_order_id(self):
        self.db.fetch_item.return_value = (7 ,)
        args = (2 , "23:45")
        result = self.order.service_get_order_id(*args)
        self.assertEqual(result , (7 ,))
        self.db.fetch_item.assert_called_once_with(query.GET_ORDER_ID , *args)

    def test_add_order_item(self):
        args = (1 , 12 , 2)
        self.order.service_add_order_item(*args)
        self.db.add_item.assert_called_once_with(query.ADD_ORDER_ITEM , *args)

    def test_view_single_order_customer_none(self):
        self.db.fetch_item.return_value = None
        result = self.order.service_view_single_order("customer" , 1 , 2)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(
            query.VIEW_SINGLE_ORDER_CUSTOMER , 1 , 2
        )

    def test_view_single_order_customer_found(self):
        data = (1 , 2 , 3 , 500 , "PLACED" , "123 St")
        self.db.fetch_item.return_value = data
        result = self.order.service_view_single_order("customer" , 1 , 2)
        self.assertIsNotNone(result)
        self.db.fetch_item.assert_called_once_with(
            query.VIEW_SINGLE_ORDER_CUSTOMER , 1 , 2
        )

    def test_view_single_order_restaurant_query(self):
        self.db.fetch_item.return_value = None
        result = self.order.service_view_single_order("restaurant" , 1 , 5)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(
            query.VIEW_SINGLE_ORDER_RESTAURANT , 1 , 5
        )

    def test_get_customer_id_from_order_id_none(self):
        self.db.fetch_item.return_value = None
        result = self.order.service_get_customer_id_from_order_id(9)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(
            query.GET_CUSTOMER_ID_FROM_ORDER_ID , 9
        )

    def test_get_customer_id_from_order_id_found(self):
        self.db.fetch_item.return_value = (4 ,)
        result = self.order.service_get_customer_id_from_order_id(9)
        self.assertEqual(result , 4)
        self.db.fetch_item.assert_called_once_with(
            query.GET_CUSTOMER_ID_FROM_ORDER_ID , 9
        )

    def test_view_orders_customer_none(self):
        self.db.fetch_all_items.return_value = False
        result = self.order.service_view_orders(2 , "customer")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.VIEW_ORDERS_CUSTOMER , 2 , 10 , 0
        )

    def test_view_orders_restaurant_query_selection(self):
        self.db.fetch_all_items.return_value = False
        result = self.order.service_view_orders(2 , "restaurant")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.VIEW_ALL_ORDERS , 2 , 10 , 0
        )

    def test_view_orders_all_delivered_returns_none(self):
        orders = [(1 , 2 , 3 , 500 , "DELIVERED" , "123 St")]
        self.db.fetch_all_items.return_value = orders
        result = self.order.service_view_orders(2 , "customer")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.VIEW_ORDERS_CUSTOMER , 2 , 10 , 0
        )

    def test_view_order_history_none(self):
        self.db.fetch_all_items.return_value = False
        result = self.order.service_view_order_history(2 , "customer")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.VIEW_ORDERS_CUSTOMER , 2 , 10 , 0
        )

    def test_view_order_history_no_delivered_returns_none(self):
        orders = [(1 , 2 , 3 , 500 , "PLACED" , "123 St")]
        self.db.fetch_all_items.return_value = orders
        result = self.order.service_view_order_history(2 , "customer")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.VIEW_ORDERS_CUSTOMER , 2 , 10 , 0
        )

    def test_delete_order(self):
        self.order.service_delete_order(9)
        self.db.update_item.assert_called_once_with(query.DELETE_ORDER , 9)

    def test_update_order_status(self):
        self.order.update_order_status(9 , "CONFIRMED")
        self.db.update_item.assert_called_once_with(
            query.UPDATE_ORDER_STATUS , "CONFIRMED" , 9
        )

    def test_fetch_order_items(self):
        items = [(1 , 9 , 12 , 2)]
        self.db.fetch_all_items.return_value = items
        self.order.fetch_order_items(9)
        self.db.fetch_all_items.assert_called_once_with(
            query.FETCH_ORDER_ITEMS , 9
        )