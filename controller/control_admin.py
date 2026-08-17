from helpers.string_input_checker import string_checker
from helpers.int_input_checker import neg_int_checker
from services.service_coupon import CouponService


class AdminController:
    def __init__(self , user , db):
        self.user = user
        self.db = db
        self.coupon_service = CouponService(self.db)

    def view_coupons(self):
        self.coupon_service.service_view_coupon()

    def add_coupon(self):
        coupon_name = ""
        discount = 0

        while(True):
            coupon_name = input("Coupon Name\n---->").upper()
            flag = string_checker(coupon_name)
            if flag :
                break

        while(True):
            discount = input("Discount Value\n---->")
            flag = neg_int_checker(discount)
            if flag:
                if(discount == "0"):
                    print("discount cant be zero")
                else:
                    break
        discount = int(discount)

        self.coupon_service.service_add_coupon(coupon_name , discount)

    def delete_coupon(self):
        name = ""

        while(True):
            name = input("Coupon Name\n---->").upper()
            flag = string_checker(name)
            if flag :
                break

        self.coupon_service.service_delete_coupon(name)
            
