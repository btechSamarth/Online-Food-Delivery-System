from unittest import TestCase
from unittest.mock import Mock
from services.service_carts import CartService
import database.queries as query

class TestingCarts(TestCase):

    def setUp(self):
        self.db = Mock()
        self.cart = CartService(self.db)

    def test_create_cart(self):
        self.db.add_item.return_value = True
        Id = 3
        self.cart.service_create_cart(Id)
        self.db.add_item.assert_called_once_with(query.CREATE_CART , Id)

    def test_add_to_cart_dish_already_present(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.add_item.return_value = False
        args = (12 , 2)
        self.cart.service_add_to_cart(1 , *args)
        self.db.fetch_item.assert_called_once_with(query.GET_CART_ID , 1)
        self.db.add_item.assert_called_once_with(query.ADD_TO_CART , 5 , *args)

    def test_add_to_cart_dish_added(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.add_item.return_value = True
        args = (12 , 2)
        self.cart.service_add_to_cart(1 , *args)
        self.db.add_item.assert_called_once_with(query.ADD_TO_CART , 5 , *args)

    def test_view_my_cart_empty(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.fetch_all_items.return_value = False
        result = self.cart.service_view_my_cart(1)
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(query.FETCH_CART , 5)

    def test_view_my_cart_not_empty(self):
        self.db.fetch_item.return_value = (5 ,)
        items = [(1 , 5 , 12 , 2)]
        self.db.fetch_all_items.return_value = items
        result = self.cart.service_view_my_cart(1)
        self.assertTrue(result)
        self.db.fetch_all_items.assert_called_once_with(query.FETCH_CART , 5)

    def test_search_in_cart_not_found(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.fetch_all_items.return_value = False
        result = self.cart.service_search_in_cart(1 , "Pizza")
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(query.SEARCH_IN_CART , 5 , "Pizza")

    def test_search_in_cart_found(self):
        self.db.fetch_item.return_value = (5 ,)
        items = [(1 , 5 , 12 , 2)]
        self.db.fetch_all_items.return_value = items
        result = self.cart.service_search_in_cart(1 , "Pizza")
        self.assertTrue(result)
        self.db.fetch_all_items.assert_called_once_with(query.SEARCH_IN_CART , 5 , "Pizza")

    def test_update_cart_failed(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.update_item.return_value = False
        args = (12 , 3)
        self.cart.service_update_cart(1 , *args)
        self.db.update_item.assert_called_once_with(query.UPDATE_CART , *args , 5)

    def test_update_cart_success(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.update_item.return_value = True
        args = (12 , 3)
        self.cart.service_update_cart(1 , *args)
        self.db.update_item.assert_called_once_with(query.UPDATE_CART , *args , 5)

    def test_delete_from_cart_failed(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.update_item.return_value = False
        self.cart.service_delete_from_cart(1 , 12)
        self.db.update_item.assert_called_once_with(query.DELETE_ITEM_FROM_CART , 12 , 5)

    def test_delete_from_cart_success(self):
        self.db.fetch_item.return_value = (5 ,)
        self.db.update_item.return_value = True
        self.cart.service_delete_from_cart(1 , 12)
        self.db.update_item.assert_called_once_with(query.DELETE_ITEM_FROM_CART , 12 , 5)

    def test_delete_cart(self):
        self.db.fetch_item.return_value = (5 ,)
        self.cart.delete_cart(1)
        self.db.fetch_item.assert_called_once_with(query.GET_CART_ID , 1)
        self.db.update_item.assert_called_once_with(query.DELETE_CART , 5)