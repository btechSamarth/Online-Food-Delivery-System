import database.queries as query
from models.models_cart_item import CartItem


class CartService:

    def __init__(self , db):
        self.db = db

    def service_create_cart(self ,Id):
        self.db.add_item(query.CREATE_CART , Id)

    def service_add_to_cart(self , Id , *args):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        if not self.db.add_item(query.ADD_TO_CART , cart_id , *args):
            print("Dish Already Present!!")
            return
        print("Dish Added!!")
        
    def service_view_my_cart(self , Id):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        items = self.db.fetch_all_items(query.FETCH_CART , cart_id)
        if not items:
            print("Cart is Empty!!")
            return None
        else:
            items = [CartItem(*item) for item in items]
            for item in items:
                print(item)
            return items

    def service_search_in_cart(self , Id , name):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        items = self.db.fetch_all_items(query.SEARCH_IN_CART , cart_id , name)
        if not items:
            print("Dish Not Found in Cart!!")
        else:
            items = [CartItem(*item) for item in items]
            for item in items:
                print(item)

            return items

    def service_update_cart(self , Id , *args):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        if not self.db.update_item(query.UPDATE_CART , *args , cart_id):
            print("Updation Failed!!")
        else:
            print("Updated Successfully!!")

    def service_delete_from_cart(self , Id , food_id):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        if not self.db.update_item(query.DELETE_ITEM_FROM_CART , food_id , cart_id):
            print("Item Deletion Failed!!")
        else:
            print("Item Deleted Successfully!!")

    def delete_cart(self , Id):
        cart_id = self.db.fetch_item(query.GET_CART_ID , Id)[0]
        self.db.update_item(query.DELETE_CART , cart_id)

