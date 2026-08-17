import database.queries as query
from models.models_food import Food


class MenuService:

        def __init__(self , db):
                self.db = db

        def services_verify_menu_id(self , rest_id):
                menu_id = self.db.fetch_item(query.FETCH_MENU_ID , rest_id)
                if menu_id is None:
                        print("No Restaurant Found! Please add a restaurant first")
                        return False
                return menu_id[0]

        def services_add_food(self , menu_id , name , description , price , category):
                if not self.db.add_item(query.ADD_DISH ,menu_id , name , description , price , category):
                        print("Dish Already Present in Menu")
                else:
                        print("Dish Added Successfully!!")

        def services_view_menu(self , menu_id):
                categories = ["STARTERS" , "MAIN COURSE" , "DESERT" , "DRINKS"]
                for category in categories:
                        foods = self.db.fetch_all_items(query.FETCH_FOODS , menu_id , category)
                        if not foods:
                                continue
                        foods = [Food(*food) for food in foods]
                        print(f"{category}".rjust(70))
                        for food in foods:
                                print(food)

                return True

        def service_get_food_id_by_name(self , name , menu_id):
                data = self.db.fetch_item(query.GET_FOOD_BY_MENU_ID , name , menu_id)
                if not data:
                        print("No Dish Found!!")
                        return None , None
                else:
                        return data

        def service_get_food_id_by_rest_name(self , rest_name , food_name):
                rest_id = self.db.fetch_item(query.GET_RESTAURANT_ID_BY_NAME , rest_name)[0]
                menu_id = self.db.fetch_item(query.FETCH_MENU_ID , rest_id)[0]
                food_id , price = self.db.fetch_item(query.GET_FOOD_BY_MENU_ID , food_name , menu_id)
                return food_id , price
