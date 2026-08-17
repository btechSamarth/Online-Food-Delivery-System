class OrderItem:

    def __init__(self , order_id , name , quantity , price):
        self.order_id = order_id
        self.food_name = name
        self.quantity = quantity
        self.price = price


    def __str__(self):
        return f"OrderId : {self.order_id}\nName : {self.food_name}\nQuantity : {self.quantity}\nTotal Price : {self.price}"