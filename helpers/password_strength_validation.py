import re

def strength_validation(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[*@$%.])"
    matches = re.match(pattern , password)
    if(matches == None):
        print("                                                                              Your PassWord is not Correct, Adhere To The Guidlines")
        return False
    else:
        return True