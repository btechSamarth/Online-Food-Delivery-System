from helpers.string_input_checker import string_checker
from helpers.int_input_checker import int_1_2_checker
from helpers.password_strength_validation import strength_validation
from helpers.hashing import encrypt_password , decrypt_password
from models.models_user import User , Owner
from services.service_auth import AuthService
from services.services_restaurant import RestaurantService
from services.service_carts import CartService


class AuthController:

    def __init__(self , db):
        self.db = db
        self.auth_service = AuthService(self.db)
        self.rest_service = RestaurantService(self.db)
        self.cart_service = CartService(self.db)

    def verify_Admin(self, username):
            print("You Have Asked To Login As ADMIN".rjust(70))
            code = ""
            while(True):
                code = input("Enter Your Security Code, If Not, Enter \"register\" to Register\n---->")
                if not string_checker(code):
                    continue
                if(code.lower() == "register"):
                    return self.register()
                break

            Code = ""
            with open("security.key" , "r") as f:
                Code = f.read()
            if(code == Code):
                print(f"Welcome {username}, Email Verified".rjust(70))
                return False
            else:
                print("Your Code Didn't Match".rjust(70))
                return True


    def login(self):
        print("Welcome to Login Page".rjust(70))
        username = ""
        password = ""
        flag = True
        user = None
        while(flag):
            while(True):
                username = input('Please Enter Your Username or "register" to Register\n---->')
                temp = string_checker(username)
                if not temp:
                    continue
                if(username.lower() == "register"):
                        return self.register()
                break
            password = input("Please Enter Your Password\n---->")
            data = self.auth_service.service_verify_user(username)
            if data != None and decrypt_password(password , data[2]):
                flag = False
                if(data[3] == "OWNER"):
                    user = Owner(*data)
                    restaurant_id = self.rest_service.services_get_restaurant_id(user.id)
                    if(restaurant_id is None):
                        print("\n[ADVICE] No Restaurant Found! Please Add a Restaurant\n".rjust(70))
                    else:
                        user.restaurant_id = restaurant_id
                else:
                    user = User(*data)

            else:
                print("Username and Password doesn't Match".rjust(70))
        return user
        
    

    def register(self ):
        print("Welcome to Registration Page".rjust(70))
        flag = True
        username =""
        password = ""
        role = ""
        while(True):
            while(True):
                role = input("Register as \n1)User Account \n2)Commercial Account \n3)Tomato Admin\n---->")
                if(role == "1" or role == "2" or role == "3"):
                    break
                else:
                    print("Please Enter input in the correct range".rjust(70))

            if(role == "1"):
                role = "USER"
            elif(role == "2"):
                role = "OWNER"
            elif(role == "3"):
                role = "ADMIN"

            while(True):
                username = input("Enter your username:\n----> ")
                temp = string_checker(username)
                if not temp:
                    continue
                break    
            
            while(True):
                str = "\n\nEnter Your Password, You Password Must Follow The Guidline\n1) Password length must be between 8 to 16 charachters longs\n2) Password must contain one Upper and one Lower Case Character\n3) Password must contain one digit from 0 to 9\n4) Password must contain one special character from '*@$%.'\n---->" 
                password = input(str.rjust(70))
                flag = string_checker(password)
                if not password:
                    continue
                if(len(password) < 8 or len(password) > 16):
                    print("Your PassWord is not Correct, Adhere To The Guidlines".rjust(70))
                    continue
                flag = strength_validation(password)
                if not flag:
                    continue

                break

            if(role == "ADMIN"):
                flag = self.verify_Admin(username)
                if(flag == True):
                    continue

            encrypted_password = encrypt_password(password)
            if(self.auth_service.service_add_user(username , encrypted_password , role) is True):
                if(role == "USER"):
                    data = self.auth_service.service_verify_user(username)
                    self.cart_service.service_create_cart(data[0])
                break
            else:
                return self.login()

        return self.login()

    def User_Authentication(self):
        user_input = -1
        while(True):
            user_input = input("Press 1 to Login     Press 2 to Register  \n---->" )
            flag = int_1_2_checker(user_input)
            if not flag:
                continue
            user_input = int(user_input)
            break

        if(user_input == 1): 
            return self.login()
        else:
            return self.register()