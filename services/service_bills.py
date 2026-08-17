import database.queries as query
from models.models_bill import Bill
from helpers.string_input_checker import string_checker

class BillService:
    def __init__(self , db):
        self.db = db

    def service_add_bill(self , *args):
        self.db.add_item(query.ADD_BILL , *args)

    def service_view_all_bills(self , user_id):
        offset = 0
        while(True):
            bills = self.db.fetch_all_items(query.VIEW_BILLS , user_id , 10 , offset)
            if not bills:
                print("No Bills Available!!")
                if(offset == 0):
                    return None
                return True
            bills = [Bill(*bill) for bill in bills]
            for bill in bills:
                print(bill)

            output = ""
            while(True):
                output = input("Show More? (Y/N)\n---->").upper()
                flag = string_checker(output)
                if flag:
                    if output == "N":
                        return True
                    elif(output == "Y"):
                        offset += 10
                        break

    def service_view_bill(self , bill_id , user_id):
        bill = self.db.fetch_item(query.VIEW_BILL , bill_id , user_id)
        if bill is None:
            print("Please Enter Correct Bill Id!!")
            return
        bill = Bill(*bill)
        print(bill)
        return bill

    def service_get_order_ids(self , bill_id):
        return self.db.fetch_all_items(query.GET_ORDER_IDS , bill_id)

    def service_get_bill_id(self , user_id , current_time):
        return self.db.fetch_item(query.GET_BILL_ID , user_id , current_time)[0]

    def service_set_final_price(self , bill_id , price):
        self.db.update_item(query.SET_FINAL_AMOUNT , price , bill_id)
        

        