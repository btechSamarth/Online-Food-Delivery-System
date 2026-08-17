#Initialization
CREATE_TABLES = """
                                    CREATE TABLE IF NOT EXISTS USERS(
                                        ID INTEGER PRIMARY KEY,
                                        USERNAME TEXT NOT NULL UNIQUE,
                                        PASSWORD TEXT NOT NULL,
                                        ROLE TEXT NOT NULL CHECK (ROLE IN ('USER' , 'OWNER' , 'ADMIN'))
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS OWNERS(
                                        ID INTEGER PRIMARY KEY,
                                        USER_ID INTEGER NOT NULL UNIQUE,
                                        RESTAURANT_ID INTEGER NOT NULL,
                            
                                        UNIQUE (USER_ID , RESTAURANT_ID),
                                        FOREIGN KEY(USER_ID) REFERENCES USERS(ID),
                                        FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID)
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS RESTAURANTS(
                                        ID INTEGER PRIMARY KEY,
                                        NAME TEXT UNIQUE NOT NULL,
                                        OPENING_TIME TEXT NOT NULL,
                                        CLOSING_TIME TEXT NOT NULL
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS MENU(
                                        ID INTEGER PRIMARY KEY,
                                        RESTAURANT_ID INTEGER NOT NULL UNIQUE,
                            
                                        FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID)
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS FOODS(
                                        ID INTEGER PRIMARY KEY,
                                        MENU_ID INTEGER NOT NULL,
                                        NAME TEXT NOT NULL,
                                        DESCRIPTION TEXT,
                                        PRICE INTEGER NOT NULL,
                                        CATEGORY TEXT NOT NULL CHECK (CATEGORY IN ("STARTERS" , "MAIN COURSE" , "DESERT" , "DRINKS")),

                                        UNIQUE (MENU_ID , NAME),
                                        FOREIGN KEY(MENU_ID) REFERENCES MENU(ID)
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS ORDERS(
                                        ID INTEGER PRIMARY KEY,
                                        CUSTOMER_ID INTEGER NOT NULL,
                                        RESTAURANT_ID INTEGER NOT NULL,
                                        BILL_ID INTEGER NOT NULL,
                                        ADDRESS TEXT NOT NULL,
                                        CREATED_AT TEXT NOT NULL,
                                        STATUS TEXT NOT NULL CHECK (STATUS IN ('PLACED' , 'CONFIRMED' , 'PREPARING' , 'OUT FOR DELIVERY' , 'DELIVERED')) DEFAULT 'PLACED',
                            
                                        FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID),
                                        FOREIGN KEY(CUSTOMER_ID) REFERENCES USERS(ID),
                                        FOREIGN KEY(BILL_ID) REFERENCES BILLS(ID)
                                    );

                                    CREATE TABLE IF NOT EXISTS ORDER_ITEMS(
                                        ORDER_ID INTEGER NOT NULL,
                                        FOOD_NAME TEXT NOT NULL,
                                        QUANTITY INTEGER NOT NULL,
                                        PRICE INTEGER NOT NULL,
                                        
                                        FOREIGN KEY(ORDER_ID) REFERENCES ORDERS(ID)
                                        ON DELETE CASCADE
                                    );
                            
                            
                                    CREATE TABLE IF NOT EXISTS CARTS(
                                        ID INTEGER PRIMARY KEY,
                                        USER_ID INTEGER NOT NULL,
                            
                                        FOREIGN KEY(USER_ID) REFERENCES USERS(ID)
                                    );
                            
                                    CREATE TABLE IF NOT EXISTS CART_ITEMS(
                                        CART_ID INTEGER NOT NULL,
                                        FOOD_ID INTEGER NOT NULL,
                                        QUANTITY INTEGER NOT NULL,
                                        PRICE INTEGER NOT NULL,
                            
                                        UNIQUE(CART_ID , FOOD_ID),
                                        FOREIGN KEY(CART_ID) REFERENCES CARTS(ID)
                                        ON DELETE CASCADE,
                                        FOREIGN KEY(FOOD_ID) REFERENCES FOODS(ID)  
                                        ON DELETE CASCADE  
                                    );


                                    CREATE TABLE IF NOT EXISTS COUPONS(
                                        NAME TEXT PRIMARY KEY,
                                        DISCOUNT INTEGER NOT NULL
                                    );

                                    
                                    CREATE TABLE IF NOT EXISTS BILLS(
                                        ID INTEGER PRIMARY KEY,
                                        CUSTOMER_ID INTEGER NOT NULL,
                                        CREATED_AT TEXT NOT NULL,
                                        DISCOUNT INTEGER NOT NULL,
                                        DELIVERY_CHARGE INTEGER NOT NULL,
                                        FINAL_PRICE INTEGER NOT NULL,

                                        FOREIGN KEY(CUSTOMER_ID) REFERENCES USERS(ID)
                                    );
                                

"""


#authentication
ADD_USER = "INSERT INTO USERS(USERNAME , PASSWORD , ROLE) VALUES(? , ? , ?)"
VERIFY_USER = "SELECT * FROM USERS WHERE USERNAME = ?"


#Restaurant
ADD_RESTAURANT = "INSERT INTO RESTAURANTS(NAME, OPENING_TIME , CLOSING_TIME) VALUES(? , ? , ?)"
GET_RESTAURANT_ID_BY_NAME = "SELECT ID, OPENING_TIME, CLOSING_TIME FROM RESTAURANTS WHERE NAME = ?"
ADD_OWNER = "INSERT INTO OWNERS(USER_ID , RESTAURANT_ID)  VALUES(? , ?)"
GET_RESTAURANT = "SELECT * FROM RESTAURANTS WHERE ID = ?"
CREATE_MENU = "INSERT INTO MENU(RESTAURANT_ID) VALUES(?)"
FETCH_MENU_ID = "SELECT ID FROM MENU WHERE RESTAURANT_ID = ?"
ADD_DISH = "INSERT INTO FOODS(MENU_ID , NAME , DESCRIPTION , PRICE , CATEGORY) VALUES(? , ? , ? , ? , ?)"
FETCH_FOODS = "SELECT ID , NAME , DESCRIPTION , PRICE , CATEGORY FROM FOODS WHERE MENU_ID = ? AND CATEGORY = ?"
GET_RESTAURANT_ID = "SELECT RESTAURANT_ID FROM OWNERS WHERE USER_ID = ?"
FETCH_RESTAURANTS = "SELECT * FROM RESTAURANTS WHERE CLOSING_TIME > ? AND OPENING_TIME < ? LIMIT ? OFFSET ?"


#food
GET_FOOD_BY_MENU_ID = "SELECT ID , PRICE FROM FOODS WHERE NAME = ? AND MENU_ID = ?"


#cart
CREATE_CART = "INSERT INTO CARTS(USER_ID) VALUES(?)"
GET_CART_ID = "SELECT ID FROM CARTS WHERE USER_ID = ?"
ADD_TO_CART = "INSERT INTO CART_ITEMS(CART_ID , FOOD_ID , QUANTITY , PRICE) VALUES(? , ? , ? , ?)"
FETCH_CART = "SELECT f.NAME , c.PRICE , c.QUANTITY , r.NAME FROM CART_ITEMS AS c JOIN FOODS AS f ON f.ID = c.FOOD_ID JOIN MENU AS m ON f.MENU_ID = m.ID JOIN RESTAURANTS AS r ON m.RESTAURANT_ID = r.ID WHERE c.CART_ID = ?"
SEARCH_IN_CART = "SELECT f.NAME , c.PRICE , c.QUANTITY , r.NAME FROM CART_ITEMS AS c JOIN FOODS AS f ON f.ID = c.FOOD_ID JOIN MENU AS m ON f.MENU_ID = m.ID JOIN RESTAURANTS AS r ON m.RESTAURANT_ID = r.ID WHERE c.CART_ID = ? AND f.NAME= ? "
UPDATE_CART = "UPDATE CART_ITEMS SET QUANTITY = ? , PRICE = ? WHERE FOOD_ID = ? AND CART_ID = ?"
DELETE_ITEM_FROM_CART = "DELETE FROM CART_ITEMS WHERE FOOD_ID = ? AND CART_ID = ?"
DELETE_CART = "DELETE FROM CART_ITEMS WHERE CART_ID = ?"

#orders
CREATE_ORDER = "INSERT INTO ORDERS(CUSTOMER_ID , RESTAURANT_ID , BILL_ID , ADDRESS ,  CREATED_AT) VALUES(? , ? , ? , ? , ?)"
GET_ORDER_ID = "SELECT ID FROM ORDERS WHERE CUSTOMER_ID = ? AND RESTAURANT_ID = ? AND CREATED_AT = ?"
ADD_ORDER_ITEM = "INSERT INTO ORDER_ITEMS(ORDER_ID , FOOD_NAME , QUANTITY , PRICE) VALUES(? , ? , ? , ?)"
FETCH_ORDER_ITEMS = "SELECT * FROM ORDER_ITEMS WHERE ORDER_ID = ?"
VIEW_ORDERS_CUSTOMER = "SELECT * FROM ORDERS WHERE CUSTOMER_ID = ? LIMIT ? OFFSET ?"
VIEW_ALL_ORDERS = "SELECT * FROM ORDERS WHERE RESTAURANT_ID = ? LIMIT ? OFFSET ? "
DELETE_ORDER = "DELETE FROM ORDERS WHERE ID = ?"
GET_CUSTOMER_ID_FROM_ORDER_ID = "SELECT CUSTOMER_ID FROM ORDERS WHERE ID = ?"
UPDATE_ORDER_STATUS = "UPDATE ORDERS SET STATUS = ? WHERE ID = ?"
VIEW_SINGLE_ORDER_RESTAURANT = "SELECT * FROM ORDERS WHERE ID = ? AND RESTAURANT_ID = ?"
VIEW_SINGLE_ORDER_CUSTOMER = "SELECT * FROM ORDERS WHERE ID = ? AND CUSTOMER_ID = ?"



#coupons
ADD_COUPON = "INSERT INTO COUPONS(NAME , DISCOUNT) VALUES(? , ?)"
DELETE_COUPON = "DELETE FROM COUPONS WHERE NAME = ?"
VIEW_COUPON = "SELECT * FROM COUPONS LIMIT ? OFFSET ?"
VERIFY_COUPON = "SELECT * FROM COUPONS WHERE NAME = ?"


#bill
ADD_BILL = "INSERT INTO BILLS(CUSTOMER_ID , CREATED_AT , DISCOUNT , DELIVERY_CHARGE , FINAL_PRICE) VALUES(? , ? , ? , ? , ?)"
VIEW_BILLS = "SELECT * FROM BILLS WHERE CUSTOMER_ID = ? LIMIT ? OFFSET ?"
VIEW_BILL = "SELECT * FROM BILLS WHERE ID = ? AND CUSTOMER_ID = ?"
GET_BILL_ID = "SELECT ID FROM BILLS WHERE CUSTOMER_ID = ? AND CREATED_AT = ?"
SET_FINAL_AMOUNT = "UPDATE BILLS SET FINAL_PRICE = ? WHERE ID = ?"
GET_ORDER_IDS = "SELECT ID FROM ORDERS WHERE BILL_ID = ?"

"""
        CREATE TABLE IF NOT EXISTS BILLS(
                                            ID INTEGER PRIMARY KEY,
                                            CUSTOMER_ID INTEGER NOT NULL,
                                            RESTAURANT_ID INTEGER NOT NULL,
                                            ORDER_ID INTEGER NOT NULL,
                                            CREATED_AT TEXT NOT NULL,
                                            DISCOUNT INTEGER NOT NULL,
                                            DELIVERY_CHARGE INTEGER NOT NULL,
                                            FINAL_PRICE INTEGER NOT NULL,
    
                                            FOREIGN KEY(CUSTOMER_ID) REFERENCES USERS(ID),
                                            FOREIGN KEY(RESTAURANT_ID) REFERENCES RESTAURANTS(ID),
                                            FOREIGN KEY(ORDER_ID) REFERENCES ORDERS(ID)
                                        
                                        );
                                
"""