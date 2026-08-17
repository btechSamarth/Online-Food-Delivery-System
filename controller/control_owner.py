from helpers.string_input_checker import string_checker
from helpers.int_input_checker import neg_int_checker
from helpers.time_checker import time_check
from datetime import datetime
from services.services_restaurant import RestaurantService
from services.services_menu import MenuService
from services.service_orders import OrderService

class OwnerController:

        def __init__(self , user , db):
                self.user = user
                self.db = db
                self.rest_service = RestaurantService(self.db)
                self.menu_service = MenuService(self.db)
                self.order_service = OrderService(self.db)
        
        def add_restaurant(self):
                name = ""
                opening_time = ""
                closing_time = ""
                if(self.user.restaurant_id != -1):
                        print("One Restaurant Already Added!!")
                        return
                while(True):
                        name = input("Restaurant Name :\n---->").lower()
                        flag = string_checker(name)
                        if flag:
                                break

                while(True):
                        opening_time = input("Opening time (HH:MM):\n---->")
                        flag = time_check(opening_time)
                        if flag:
                                opening_time = datetime.strptime(opening_time , "%H:%M").time()
                                opening_time = opening_time.strftime("%H:%M")
                                break
                        

                while(True):
                        closing_time = input("Closing time (HH:MM):\n---->")
                        flag = time_check(closing_time)
                        if flag:
                                closing_time = datetime.strptime(closing_time , "%H:%M").time()
                                closing_time = closing_time.strftime("%H:%M")
                                break
                

                return self.rest_service.services_add_restaurant(self.user , name , opening_time , closing_time)


        def get_restaurant(self):
                return self.rest_service.services_get_restaurant_data(self.user.restaurant_id)

                

        def add_food(self):
                menu_id = self.menu_service.services_verify_menu_id(self.user.restaurant_id)
                if not menu_id:
                        return
                name = ""
                description = ""
                price = 0
                categories = ["STARTERS", "MAIN COURSE" , "DESERT" , "DRINKS"]
                category = ""

                while(True):
                        name = input("Name of The Dish\n---->").lower()
                        flag = string_checker(name)
                        if flag:
                                break

                while(True):
                        description = input("Description of the Dish\n---->")
                        flag = string_checker(description)
                        if flag:
                                break

                while(True):
                        price = input("Price of The Dish\n---->")
                        flag = neg_int_checker(price)
                        if flag:
                                break

                while(True):
                        category = input(f'Please Select a category from {categories}\n---->').upper()
                        if category in categories:
                                break
                        else: 
                                print("Please Select a Suitable Category")

                return self.menu_service.services_add_food(menu_id , name , description , price , category)


        def view_menu(self):
                menu_id = self.menu_service.services_verify_menu_id(self.user.restaurant_id)
                return self.menu_service.services_view_menu(menu_id)

        def view_my_orders(self):
                self.order_service.service_view_orders(self.user.restaurant_id , "restaurant")

        def update_order_status(self):
                order_id = -1
                statuses = ['PLACED' , 'CONFIRMED' , 'PREPARING' , 'OUT FOR DELIVERY' , 'DELIVERED']
                output = ""
                upgrade_to = ""

                while(True):
                        order_id = input("Enter Order Id\n---->")
                        flag = neg_int_checker(order_id)
                        if flag and order_id != "0":
                                order_id = int(order_id)
                                break
                order =  self.order_service.service_view_single_order("restaurant" , order_id , self.user.restaurant_id)
                if order is None:
                        return
               
                if(order.status == "DELIVERED"):
                        print("Order is Delivered! Status Cant Be Changed!!")
                        return                

                while(True):
                        print(statuses)
                        upgrade_to = input("Upgrade to?\n---->").upper()
                        flag = string_checker(upgrade_to)
                        if flag:
                                if(upgrade_to in statuses):
                                        self.order_service.update_order_status(order_id , upgrade_to)
                                        return
                                else:
                                        print("Please Enter Correct Status!!")

        def view_order_history(self):
                self.order_service.service_view_order_history(self.user.restaurant_id , "restuarant")
