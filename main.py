from database.db_initialize import Database
from controller.control_auth import AuthController
from controller.control_dashboard import DashboardController

def main():
    # db initialized
    try:
        print("                                                                              Welcome to Tomato")
        db = Database()
        db.Initialize()
        # login/register
        control = AuthController(db)
        user = control.User_Authentication()
        #dashboard1
        control = DashboardController(user , db)
        control.User_Dashboard()
    except KeyboardInterrupt:
        return
    finally:
        db.connection.close()
        print("                                                                              Missing You Already!")

    
if __name__ == "__main__":
    main()