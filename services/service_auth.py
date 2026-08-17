import database.queries as query



class AuthService:

    def __init__(self , db):
        self.db = db

    def service_verify_user(self , username):

        data = self.db.fetch_item(query.VERIFY_USER, username)
        if data is None:
            print("Check Your Username and Password!!")
            return None
        else:
            return data


    def service_add_user(self , username , encrypted_password , role):
        if not self.db.add_item( query.ADD_USER , username , encrypted_password , role):
            print("User Already exist")
            return False
        else:
            print("Registered Successfully!!")
            return True