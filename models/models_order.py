class Order:

    def __init__(self , order_id , cust_id , rest_id , bill_id , addr , created_at , status):
        self.order_id = order_id
        self.cust_id = cust_id
        self.rest_id = rest_id
        self.bill_id = bill_id
        self.addr = addr
        self.created = created_at
        self.status = status

    
    