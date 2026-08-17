class Food:
    
    def __init__(self , Id , name , description , price , category):
        self.Id = Id
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def __str__(self):
        return f"Name: {self.name}\nId: {self.Id}\nDescription: {self.description}\nPrice: {self.price}"