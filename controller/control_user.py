from datetime import datetime
from helpers.int_input_checker import int_1_2_checker , neg_int_checker
from helpers.string_input_checker import string_checker
from services.services_restaurant import RestaurantService
from services.service_carts import CartService
from services.services_menu import MenuService
from services.service_orders import OrderService
from services.service_coupon import CouponService
from services.service_bills import BillService
import random
from models.models_cart_item import CartItem

class UserController:

    def __init__(self , user , db):
        self.user = user
        self.db = db
        self.rest_service = RestaurantService(self.db)
        self.cart_service = CartService(self.db)
        self.menu_service = MenuService(self.db)
        self.order_service = OrderService(self.db)
        self.coupon_service = CouponService(self.db)
        self.bill_service = BillService(self.db)

    def view_all_restaurants(self):
        current_time = datetime.now().strftime("%H:%M")
        offset = 0
        while(True):
            restaurants = self.rest_service.services_view_all_restaurants(current_time , current_time , offset)
            if restaurants is None:
                return
            show_more = -1
            while(True):
                show_more = input("1)Show More 2)Exit")
                flag = int_1_2_checker(show_more)
                if flag:
                    break
            if(show_more == 1):
                offset += 10
            else:
                break
            

    def view_menu(self):
        rest_name = "" 
        rest_id = -1
        menu_id = -1

        while(True):
            rest_name = input("Restaurant Name\n---->").lower()
            flag = string_checker(rest_name)
            if  flag:
                break 

        data = self.rest_service.services_get_restaurant_id_by_name(rest_name)
        if(data is None):
            return

        rest_id , _ , _ = data
       
        menu_id = self.menu_service.services_verify_menu_id(rest_id)
        return self.menu_service.services_view_menu(menu_id)

    def add_to_cart(self):
        res_name = "" 
        food_name = ""
        res_id = -1
        menu_id = -1
        food_id = -1
        quantity = -1
        price = 0
        opening_time = ""
        closing_time = ""
        current_time = datetime.now().strftime("%H:%M")

        while(True):
            res_name = input("Restaurant Name\n---->").lower()
            flag = string_checker(res_name)
            if flag:
                data = self.rest_service.services_get_restaurant_id_by_name(res_name)
                if data is None:
                    return None
                else:
                    break
        rest_id , opening_time , closing_time = data
        if(closing_time < current_time or opening_time > current_time):
            print("Restaurant is Closed!!")
            return
        menu_id = self.menu_service.services_verify_menu_id(rest_id)

        while(True):
            food_name = input("Food Name\n---->").lower()
            flag = string_checker(food_name)
            if flag:
                food_id , price = self.menu_service.service_get_food_id_by_name(food_name , menu_id)
                print(price)
                if(food_id):
                    break

        while(True):
            quantity = input("Quantity\n---->")
            flag = neg_int_checker(quantity)
            if flag:
                break
        quantity = int(quantity)
        price = price * quantity
        print(price)
        self.cart_service.service_add_to_cart(self.user.id , food_id , quantity , price)


    def view_my_cart(self):
        self.cart_service.service_view_my_cart(self.user.id)

    def update_cart(self):
        dish_name = ""
        rest_name = ""
        cart_item = None
        quantity = -1
        while(True):
            dish_name = input("Dish Name\n---->").lower()
            flag = string_checker(dish_name)
            if flag:
                break
        items = self.cart_service.service_search_in_cart(self.user.id , dish_name)
        if not items:
            return
        while(True):
            rest_name = input("Restaurant Name\n---->").lower()
            flag = string_checker(dish_name)
            if not flag:
                continue
            cart_item = [item for item in items if item.rest_name == rest_name]
            if not len(cart_item):
                print("Please Check Your Restaurant Name!!")
            else:
                cart_item = cart_item[0]
                break
        print(cart_item)
        while(True):
            quantity = input("New Quantity?\n---->")
            flag = neg_int_checker(quantity)
            if not flag:
                continue
            quantity = int(quantity)
            food_id , price = self.menu_service.service_get_food_id_by_rest_name(rest_name , dish_name)
            if(quantity == 0):
                self.cart_service.service_delete_from_cart(self.user.id , food_id)
            else:
                new_price = price * quantity
                self.cart_service.service_update_cart(self.user.id , quantity , new_price , food_id)
            return

    def take_coupon_name(self):
        coupon_name = ""
        while(True):
            coupon_name = input("Coupon Name\n---->")
            flag = string_checker(coupon_name)
            if flag:
                break
        return coupon_name

    def creating_orders(self , items , address , discount , delivery_charge , current_time , bill_id):
        rest_ids = []
        order_ids = {}
        total_price = 0
        
        for item in items:
            rest_id , _ , _ = self.rest_service.services_get_restaurant_id_by_name(item.rest_name)
            if(rest_id not in rest_ids):
                rest_ids.append(rest_id)
                self.order_service.service_create_order(self.user.id , rest_id , bill_id ,address , current_time) 
                order_ids[rest_id] = self.order_service.service_get_order_id(self.user.id , rest_id , current_time)[0]
                self.order_service.service_add_order_item(order_ids[rest_id] , item.food_name , item.quantity , item.price)
            else:
                self.order_service.service_add_order_item(order_ids[rest_id] , item.food_name , item.quantity , item.price)
            total_price += item.price

        total_price = total_price - discount + delivery_charge
        return total_price



    def create_bill(self , user_id ,created_at , discount , delivery_charge , final_price):
        bill_id = -1
        order = -1
        flag = True
        self.bill_service.service_add_bill(user_id , created_at , discount , delivery_charge , final_price)


    def place_order(self):
        items = self.cart_service.service_view_my_cart(self.user.id)
        coupon_name = ""
        output = ""
        discount = 0
        
        if not items:
            print("Nothing in Cart, Cant't Place Order")
            return
        
        while(True):
            output = input("Have Coupon? (Y/N)\n---->").upper()
            flag = string_checker(output)
            if flag:
                if(output == "Y"):
                    coupon_name = self.take_coupon_name()
                    coupon = self.coupon_service.service_verify_coupon(coupon_name)
                    if coupon:
                        discount += coupon.discount
                        break
                elif(output == "N"):
                    break
                else:
                    print("please provide suitable input")
        
        address = ""
        while(True):
            address = input("Enter Address\n---->")
            flag = string_checker(address)
            if flag:
                break

        delivery_charge = random.randint(10 , 30)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        total_price = 0
        output = ""
        while(True):
            output = input(f"You will be charged {delivery_charge} as delivery charge, Continue? (Y/N)\n---->").upper()
            flag = string_checker(output)
            if flag:
                if(output == "N"):
                    return
                if(output == "Y"):
                    break

        self.create_bill(self.user.id ,current_time , discount , delivery_charge , total_price)
        bill_id = self.bill_service.service_get_bill_id(self.user.id , current_time)
        total_price = self.creating_orders(items , address , discount , delivery_charge , current_time , bill_id)
        self.bill_service.service_set_final_price(bill_id , total_price)
        self.cart_service.delete_cart(self.user.id)
        print("Order Placed Succesfully!!".rjust(70))

    def view_orders(self):
        self.order_service.service_view_orders(self.user.id , "customer")

    def cancel_order(self):
        output = ""
        order_id = -1
        while(True):
            order_id = input("Order Id\n---->")
            flag = neg_int_checker(order_id)
            if flag:
                break
        data = self.order_service.service_view_single_order("customer" , order_id , self.user.id)
        if not data:
            return
        if(data.status == "DELIVERED"):
            print("Your Order is Already Delivered!!")
            return
        if(data.status != "PLACED"):
            print("Restaurant Has Confirmed Your Order, It Cant Be Cancelled!!")
            return
        while(True):
            output = input("Are You Sure You Want To Cancel Your Order? (Y/N)\n---->").upper()
            flag = string_checker(output)
            if flag and output == "Y" or output == "N":
                break

        if(output == 'N'):
            return

        self.order_service.service_delete_order(order_id)

    def view_order_history(self):
        self.order_service.service_view_order_history(self.user.id , "customer")

    def view_bill(self):
        if not self.bill_service.service_view_all_bills(self.user.id):
            return
        
        bill_id = None
        while(True):
            bill_id = input("Bill Id\n---->")
            flag = neg_int_checker(bill_id)
            if flag:
                break
        bill_id = int(bill_id)
        bill = self.bill_service.service_view_bill(bill_id , self.user.id)
        if bill is None:
            return
        order_ids = self.bill_service.service_get_order_ids(bill_id)
        for order_id in order_ids:
            self.order_service.fetch_order_items(order_id[0])
        bill.print_final_amount()

        