class User:       
    def __init__(self , Id , username , password , role):
        self.id = Id
        self.username = username
        self.role = role

    def __str__(self):
        return f"id : {self.id} , username : {self.username} , role : {self.role}"


class Owner(User):

    def __init__(self , Id , username , password , role):
        super().__init__(Id , username , password , role)
        self.restaurant_id = -1