class Bill:

    def __init__(self , *args):
        self.bill_id = args[0]
        self.customer_id = args[1]
        self.created_at = args[2]
        self.discount = args[3]
        self.delivery_charge = args[4]
        self.final_price = args[5]

    def __str__(self):
        return f"Bill Id : {self.bill_id}\nOrdered At : {self.created_at}"

    def print_final_amount(self):
        print(f"Discount : {self.discount}\nDelivery_Charge : {self.delivery_charge}\nFinal Amount : {self.final_price}")

    

    """
    CREATE TABLE IF NOT EXISTS BILLS(
                                            ID INTEGER PRIMARY KEY,
                                            CUSTOMER_ID INTEGER NOT NULL,
                                            RESTAURANT_ID INTEGER NOT NULL,
                                            ORDER_ID INTEGER NOT NULL,
                                            CREATED_AT TEXT NOT NULL,
                                            DISCOUNT INTEGER NOT NULL,
                                            DELIVERY_CHARGE INTEGER NOT NULL,
                                            FINAL_PRICE INTEGER NOT NULL,
    
                                            FOREIGN KEY(CUSTOMER_ID) REFERENCES USERS(ID),
                                            FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID),
                                            FOREIGN KEY(ORDER_ID) REFERENCES ORDERS(ID)
                                            ON DELETE CASCADE
                                        
                                        );
    
    """