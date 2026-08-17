class Coupon:
    def __init__(self , name , discount):
        self.name = name
        self.discount = discount

    def __str__(self):
        return f"Name : {self.name}\nDiscount : {self.discount}\n\n"