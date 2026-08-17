class CartItem:

    def __init__(self , food_name , price , quantity , rest_name):
        self.food_name = food_name
        self.quantity = quantity
        self.price = price
        self.rest_name = rest_name

    def __str__(self):
        return f"Name : {self.food_name}\nTotal Price : {self.price}\nQuantity : {self.quantity}\nRestaurant: {self.rest_name}\n\n"