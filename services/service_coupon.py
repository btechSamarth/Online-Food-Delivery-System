import database.queries as query
from models.models_coupon import Coupon
from helpers.string_input_checker import string_checker

class CouponService:

    def __init__(self , db):
        self.db = db

    def service_add_coupon(self , name , discount):
        if not self.db.add_item(query.ADD_COUPON , name , discount):
            print("Coupon Already Exists!!")
            return False
        else:
            print("Added Successfully!!")
            return True

    def service_delete_coupon(self , name):
        if not self.db.update_item(query.DELETE_COUPON , name):
            print("No Coupon Found")
            return False
        else:
            print("Deleted Successfully!!")
            return True

    def service_view_coupon(self):
        offset = 0
        while(True):
            coupons = self.db.fetch_all_items(query.VIEW_COUPON , 10 , offset)
            if not coupons:
                print("No coupons to show")
                return
            coupons = [Coupon(*coupon) for coupon in coupons]
            for coupon in coupons:
                print(coupon)

            view_more = ""

            while(True):
                view_more = input("View More? (Y/N)\n----->").upper()
                flag = string_checker(view_more)
                if flag:
                    if(view_more == "N"):
                        return
                    offset += 10
                    break

    def service_verify_coupon(self , name):
        coupon = self.db.fetch_item(query.VERIFY_COUPON , name)
        if coupon is None:
            print("Invalid Coupon!!")
            return None
        else:
            print("Coupon Added Successfully")
            return Coupon(*coupon)