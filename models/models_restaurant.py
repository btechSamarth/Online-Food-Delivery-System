class Restaurant:

    def __init__(self , Id , name , opening_time , closing_time):
        self.id = Id
        self.name = name
        self.opening_time = opening_time
        self.closing_time = closing_time

    def __str__(self):
        return f"Name: {self.name}\nOpening Time: {self.opening_time}\nClosing Time: {self.closing_time}\nId: {self.id}\n\n"