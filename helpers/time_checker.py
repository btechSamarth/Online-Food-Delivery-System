from datetime import datetime
from helpers.string_input_checker import string_checker

def time_check(time):
    try:
        flag = string_checker(time)
        if(flag == False):
            return flag
        datetime.strptime(time , "%H:%M")
        return True
    except ValueError:
        print("Please Enter Time In Mentioned Format!")
        return False