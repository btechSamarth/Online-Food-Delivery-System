from helpers.int_input_checker import neg_int_checker
from controller.control_owner import OwnerController
from controller.control_user import UserController
from controller.control_admin import AdminController


class DashboardController:

    def __init__(self , user , db):
        self.user = user
        self.db = db

    def User_Dashboard(self):
        print(self.user)

        while(True):
            user_input = ""
            str = ""
            if(self.user.role == "USER"):

                control = UserController(self.user , self.db)

                str = "\n1)To View Restaurants\n2)To View Menu\n3)To Add in Cart\n4)To View Cart\n5)To Update Cart\n6)To Place Order\n7)To View Order Status\n8)To Cancel Order\n9)To Order History\n10)To View Bills\n11)To Exit\n\n---->"
                user_dict = {
                    1 : control.view_all_restaurants,
                    2 : control.view_menu,
                    3 : control.add_to_cart,
                    4 : control.view_my_cart,
                    5 : control.update_cart,
                    6 : control.place_order,
                    7 : control.view_orders,
                    8 : control.cancel_order,
                    9 : control.view_order_history,
                    10 : control.view_bill
                }
                while(True):
                    user_input = input(str)
                    flag = neg_int_checker(user_input)
                    if(flag):
                        break
                user_input = int(user_input)
                if(user_input <= 0 or user_input > 11):
                    print("Invalid Input!!")
                elif(user_input == 11):
                    return
                else:
                    action = user_dict[user_input]
                    action()
                    
            elif(self.user.role == "OWNER"):

                control = OwnerController(self.user , self.db)
                str = "1)Add Your Restaurant\n2)Fetch Your Restaurant Detailes\n3)Add Menu Items\n4)To View Your Menu\n5)To View All Orders\n6)To Update Order Status\n7)To View Order History\n8)To Exit\n\n---->"
                owner_dict = {
                    1 : control.add_restaurant,
                    2 : control.get_restaurant,
                    3 : control.add_food,
                    4 : control.view_menu,
                    5 : control.view_my_orders,
                    6 : control.update_order_status,
                    7 : control.view_order_history
                }
                while(True):
                    user_input = input(str)
                    flag = neg_int_checker(user_input)
                    if(flag):
                        break
                user_input = int(user_input)
                if(user_input <= 0 or user_input > 8):
                    print("Invalid Input!!")
                elif(user_input == 8):
                    return
                else:
                    action = owner_dict[user_input]
                    action()
            else:
                control = AdminController(self.user , self.db)
                str = "1)To Add Discount Coupons\n2)To Remove Discount Coupons\n3)To View All Coupons\n4)To Exit\n\n---->"
                admin_dict = {
                    1 : control.add_coupon,
                    2 : control.delete_coupon,
                    3 : control.view_coupons
                }
                while(True):
                    user_input = input(str)
                    flag = neg_int_checker
                    if(flag):
                        break
                user_input = int(user_input)
                if(user_input <= 0 or user_input > 4):
                    print("Invalid Input!!")
                elif(user_input == 4):
                    return
                else:
                    action = admin_dict[user_input]
                    action()

        

