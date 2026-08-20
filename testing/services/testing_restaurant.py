from unittest import TestCase
from unittest.mock import Mock
from services.services_restaurant import RestaurantService
import database.queries as query


class TestingRestaurant(TestCase):

    def setUp(self):
        self.db = Mock()
        self.rest = RestaurantService(self.db)

    def test_get_restaurant_data_none(self):
        self.db.fetch_item.return_value = None
        result = self.rest.services_get_restaurant_data(5)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(query.GET_RESTAURANT , 5)

    def test_get_restaurant_data_found(self):
        data = (5 , "Dominos" , "09:00" , "23:00")
        self.db.fetch_item.return_value = data
        result = self.rest.services_get_restaurant_data(5)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(query.GET_RESTAURANT , 5)

    def test_add_restaurant_success(self):
        user = Mock()
        user.id = 1
        self.db.add_item.return_value = True
        self.db.fetch_item.return_value = (5 ,)
        self.rest.services_add_restaurant(user , "Dominos" , "09:00" , "23:00")
        self.db.add_item.assert_any_call(
            query.ADD_RESTAURANT , "Dominos" , "09:00" , "23:00"
        )
        self.db.fetch_item.assert_called_once_with(
            query.GET_RESTAURANT_ID_BY_NAME , "Dominos"
        )
        self.assertEqual(user.restaurant_id , 5)
        self.db.add_item.assert_any_call(query.ADD_OWNER , 1 , 5)
        self.db.add_item.assert_any_call(query.CREATE_MENU , 5)

    def test_add_restaurant_name_taken(self):
        user = Mock()
        self.db.add_item.return_value = False
        self.rest.services_add_restaurant(user , "Dominos" , "09:00" , "23:00")
        self.db.add_item.assert_called_once_with(
            query.ADD_RESTAURANT , "Dominos" , "09:00" , "23:00"
        )
        self.db.fetch_item.assert_not_called()

    def test_view_all_restaurants_none(self):
        self.db.fetch_all_items.return_value = False
        result = self.rest.services_view_all_restaurants("09:00" , "23:00" , 0)
        self.assertIsNone(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.FETCH_RESTAURANTS , "09:00" , "23:00" , 10 , 0
        )

    def test_view_all_restaurants_found(self):
        restaurants = [(5 , "Dominos" , "09:00" , "23:00")]
        self.db.fetch_all_items.return_value = restaurants
        result = self.rest.services_view_all_restaurants("09:00" , "23:00" , 0)
        self.assertTrue(result)
        self.db.fetch_all_items.assert_called_once_with(
            query.FETCH_RESTAURANTS , "09:00" , "23:00" , 10 , 0
        )

    def test_get_restaurant_id_by_name_none(self):
        self.db.fetch_item.return_value = None
        result = self.rest.services_get_restaurant_id_by_name("Dominos")
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(
            query.GET_RESTAURANT_ID_BY_NAME , "Dominos"
        )

    def test_get_restaurant_id_by_name_found(self):
        self.db.fetch_item.return_value = (5 , "09:00" , "23:00")
        result = self.rest.services_get_restaurant_id_by_name("Dominos")
        self.assertEqual(result , (5 , "09:00" , "23:00"))
        self.db.fetch_item.assert_called_once_with(
            query.GET_RESTAURANT_ID_BY_NAME , "Dominos"
        )

    def test_get_restaurant_id_none(self):
        self.db.fetch_item.return_value = None
        result = self.rest.services_get_restaurant_id(1)
        self.assertIsNone(result)
        self.db.fetch_item.assert_called_once_with(query.GET_RESTAURANT_ID , 1)

    def test_get_restaurant_id_found(self):
        self.db.fetch_item.return_value = (5 ,)
        result = self.rest.services_get_restaurant_id(1)
        self.assertEqual(result , 5)
        self.db.fetch_item.assert_called_once_with(query.GET_RESTAURANT_ID , 1)