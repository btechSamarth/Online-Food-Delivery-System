from models.models_restaurant import Restaurant
import database.queries as query

class RestaurantService:

    def __init__(self , db):
         self.db = db

    def services_get_restaurant_data(self , rest_id):
        data = self.db.fetch_item(query.GET_RESTAURANT , rest_id)
        if(data is None):
                print("No Restaurant Found! Please add a restaurant first")
                return None
        restaurant = Restaurant(*data)
        print(restaurant)


    def services_add_restaurant(self , user , name , opening_time , closing_time ):
        
        if(self.db.add_item(query.ADD_RESTAURANT , name , opening_time , closing_time)):
                print("Restaurant Added Successfully !!") 
                restaurant_id = self.db.fetch_item(query.GET_RESTAURANT_ID_BY_NAME , name)
                user.restaurant_id = restaurant_id[0]
                self.db.add_item(query.ADD_OWNER ,user.id,user.restaurant_id)
                self.db.add_item(query.CREATE_MENU , user.restaurant_id)
        else:
                print("Restaurant Name Already Taken")


    def services_view_all_restaurants(self , current_time1 , current_time2 , offset):
        restaurants = self.db.fetch_all_items(query.FETCH_RESTAURANTS , current_time1 , current_time2,  10 , offset)
        if not restaurants:
            print("Nothing To Show".rjust(40))
            print("\n")
            return None
        restaurants = [Restaurant(*rest) for rest in restaurants]
        for rest in restaurants:
            print(rest)
        return True


    def services_get_restaurant_id_by_name(self , name):
        data = self.db.fetch_item(query.GET_RESTAURANT_ID_BY_NAME , name)
        if(data is None):
            print("Please Check Your Name")
            return None
        rest_id , opening_time , closing_time = data
        return rest_id , opening_time , closing_time

    def services_get_restaurant_id(self , Id):
        data = self.db.fetch_item(query.GET_RESTAURANT_ID , Id)
        if(data is None):
            return None
        else:
            return data[0]