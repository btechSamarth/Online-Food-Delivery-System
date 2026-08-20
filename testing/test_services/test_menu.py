from unittest import TestCase
from unittest.mock import Mock , call
from services.services_menu import MenuService
import database.queries as query


class TestingMenu(TestCase):

    def setUp(self):
        self.db = Mock()
        self.menu = MenuService(self.db)

    def test_verify_menu_id_none(self):
        self.db.fetch_item.return_value = None
        result = self.menu.services_verify_menu_id(5)
        self.assertFalse(result)
        self.db.fetch_item.assert_called_once_with(query.FETCH_MENU_ID , 5)

    def test_verify_menu_id_found(self):
        self.db.fetch_item.return_value = (7 ,)
        result = self.menu.services_verify_menu_id(5)
        self.assertEqual(result , 7)
        self.db.fetch_item.assert_called_once_with(query.FETCH_MENU_ID , 5)

    def test_add_food_already_present(self):
        self.db.add_item.return_value = False
        self.menu.services_add_food(7 , "Pizza" , "Cheesy" , 200 , "MAIN COURSE")
        self.db.add_item.assert_called_once_with(query.ADD_DISH , 7 , "Pizza" , "Cheesy" , 200 , "MAIN COURSE")

    def test_add_food_success(self):
        self.db.add_item.return_value = True
        self.menu.services_add_food(7 , "Pizza" , "Cheesy" , 200 , "MAIN COURSE")
        self.db.add_item.assert_called_once_with(query.ADD_DISH , 7 , "Pizza" , "Cheesy" , 200 , "MAIN COURSE")

    def test_view_menu_no_food(self):
        self.db.fetch_all_items.return_value = False
        result = self.menu.services_view_menu(7)
        self.assertTrue(result)
        self.db.fetch_all_items.assert_has_calls([
            call(query.FETCH_FOODS , 7 , "STARTERS") ,
            call(query.FETCH_FOODS , 7 , "MAIN COURSE") ,
            call(query.FETCH_FOODS , 7 , "DESERT") ,
            call(query.FETCH_FOODS , 7 , "DRINKS") ,
        ])

    def test_view_menu_with_food(self):
        foods = [(1 , "Pizza" , "Cheesy" , 200 , "MAIN COURSE")]
        self.db.fetch_all_items.side_effect = [False , foods , False , False]
        result = self.menu.services_view_menu(7)
        self.assertTrue(result)
        self.assertEqual(self.db.fetch_all_items.call_count , 4)

    def test_get_food_id_by_name_none(self):
        self.db.fetch_item.return_value = None
        result = self.menu.service_get_food_id_by_name("Pizza" , 7)
        self.assertEqual(result , (None , None))
        self.db.fetch_item.assert_called_once_with(query.GET_FOOD_BY_MENU_ID , "Pizza" , 7)

    def test_get_food_id_by_name_found(self):
        self.db.fetch_item.return_value = (12 , 200)
        result = self.menu.service_get_food_id_by_name("Pizza" , 7)
        self.assertEqual(result , (12 , 200))
        self.db.fetch_item.assert_called_once_with(query.GET_FOOD_BY_MENU_ID , "Pizza" , 7)

    def test_get_food_id_by_rest_name(self):
        self.db.fetch_item.side_effect = [(3 ,) ,(7 ,) ,(12 , 200) ,]
        result = self.menu.service_get_food_id_by_rest_name("Dominos" , "Pizza")
        self.assertEqual(result , (12 , 200))
        self.db.fetch_item.assert_has_calls([
            call(query.GET_RESTAURANT_ID_BY_NAME , "Dominos") ,
            call(query.FETCH_MENU_ID , 3) ,
            call(query.GET_FOOD_BY_MENU_ID , "Pizza" , 7) ,
        ])