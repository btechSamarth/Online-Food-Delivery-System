import database.queries as query
from models.models_order import Order
from models.models_order_item import OrderItem
from helpers.string_input_checker import string_checker


class OrderService:

    def __init__(self , db):
        self.db = db

        """
        CREATE TABLE IF NOT EXISTS ORDERS(
                                                ID INTEGER PRIMARY KEY,
                                                CUSTOMER_ID INTEGER NOT NULL,
                                                RESTAURANT_ID INTEGER NOT NULL,
                                                TOTAL_PRICE INTEGER NOT NULL,
                                                STATUS TEXT NOT NULL CHECK (STATUS IN ('PLACED' , 'CONFIRMED' , 'PREPARING' , 'OUT FOR DELIVERY' , 'DELIVERED')) DEFAULT 'PLACED',
                                    
                                                FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID),
                                                FOREIGN KEY(CUSTOMER_ID) REFERENCES USERS(ID)
                                            );
                                    
        
        
        """

    def service_create_order(self , *args):
        self.db.add_item(query.CREATE_ORDER , *args)
        return True

    def service_get_order_id(self , *args):
        return self.db.fetch_item(query.GET_ORDER_ID , *args)

    def service_add_order_item(self , *args):
        self.db.add_item(query.ADD_ORDER_ITEM , *args)

    def decorator2(func):
        def wrapper(self , role , *args):
            q = ""
            if(role == "customer"):
                q = query.VIEW_SINGLE_ORDER_CUSTOMER
            else:
                q = query.VIEW_SINGLE_ORDER_RESTAURANT
            return func(self , q , *args)
        return wrapper

    @decorator2
    def service_view_single_order(self , q , *args):
        order = self.db.fetch_item(q , *args)
        if order is None:
            print("Cant Find Any Order!!")
            return None
        else:
            order = Order(*order)
            return order


    def service_get_customer_id_from_order_id(self , order_id):
        cust_id = self.db.fetch_item(query.GET_CUSTOMER_ID_FROM_ORDER_ID , order_id)
        if cust_id is None:
            print("No Order Found!!")
            return None
        else:
            return cust_id[0]

    def decorator(func):
        def wrapper(self , Id , role):
            q = ""
            if(role == "customer"):
                q = query.VIEW_ORDERS_CUSTOMER
            else:
                q = query.VIEW_ALL_ORDERS
            return func(self , q , Id)
        return wrapper


    @decorator
    def service_view_orders(self , q ,Id):
            statuses = ['PLACED' , 'CONFIRMED' , 'PREPARING' , 'OUT FOR DELIVERY' , 'DELIVERED']
            offset = 0
            while(True):
                orders = self.db.fetch_all_items(q , Id , 10 , offset)
                if not orders:
                    print("No Current Order")
                    return None
                orders = [Order(*o) for o in orders]
                flag = True
                for order in orders:
                    if(order.status != "DELIVERED"):
                        flag = False
                        order_items = self.db.fetch_all_items(query.FETCH_ORDER_ITEMS , order.order_id)
                        order_items = [OrderItem(*order) for order in order_items]
                        for o in order_items:
                            print(o)
                            print("Status : " , end= "")
                            for status in statuses:
                                if(status != order.status):
                                    print(status , end="-->")
                                else:
                                    print(status , end = "")
                                    break
                            print("\n")
    
                if flag:
                    print("No Current Order")
                    return None
                view_more = ""
                while(True):
                    print("\n")
                    view_more = input("Show More (Y/N)\n---->").upper()
                    flag = string_checker(view_more)
                    if flag and view_more == "N":
                        return 
                    if(view_more == "Y"):
                        offset += 10
                        break 

    @decorator
    def  service_view_order_history(self , q , Id ):
        statuses = ['PLACED' , 'CONFIRMED' , 'PREPARING' , 'OUT FOR DELIVERY' , 'DELIVERED']
        offset = 0
        flag = True
        while(True):
            orders = self.db.fetch_all_items(q , Id , 10 , offset)
            if not orders:
                print("No Current Order")
                return None
            orders = [Order(*o) for o in orders]
            for order in orders:
                if(order.status == "DELIVERED"):
                    flag = False
                    order_items = self.db.fetch_all_items(query.FETCH_ORDER_ITEMS , order.order_id)
                    order_items = [OrderItem(*order) for order in order_items]
                    for o in order_items:
                        print(o)
                        for status in statuses:
                            if(status != order.status):
                                print(status , end="-->")
                            else:
                                print(status , end = "")
                                break
                        print("\n")

            if flag:
                print("No Current Order")
                return None
            view_more = ""
            while(True):
                print("\n")
                view_more = input("Show More (Y/N)\n---->").upper()
                flag = string_checker(view_more)
                if flag and view_more == "N":
                    return 
                offset += 10
                break


    def service_delete_order(self , order_id):
            self.db.update_item(query.DELETE_ORDER , order_id)
            print("Order Deleted Successfully")
    
    def update_order_status(self , order_id , status):
        self.db.update_item(query.UPDATE_ORDER_STATUS , status , order_id)
        print("Status Updated Successfully")

    def fetch_order_items(self , order_id):
        items = self.db.fetch_all_items(query.FETCH_ORDER_ITEMS , order_id)
        items = [OrderItem(*item) for item in items]
        for item in items:
            print(item)