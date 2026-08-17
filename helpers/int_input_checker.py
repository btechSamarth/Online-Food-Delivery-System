class CustomError2(Exception):

    def __init__(self):
        super().__init__("                                                                              Input Must be 1/2")

class CustomError1(Exception):

    def __init__(self):
        super().__init__("                                                                              Input can be 0 or Positive")


def neg_int_checker(num):
    try:
        num = int(num)
        if(num < 0):
            raise CustomError1
    except CustomError1 as e:
        print(e)
        return False
    except ValueError:
        print("                                                                              Please Enter Input in Digits")
        return False
    else:
        return True

def int_1_2_checker(num):
    try:
        num = int(num)
        if(num != 1 and num != 2):
            raise CustomError2
    except CustomError2 as e:
        print(e)
        return False
    except ValueError:
        print("                                                                              Please Enter Input in Digits")
        return False
    else:
        return True