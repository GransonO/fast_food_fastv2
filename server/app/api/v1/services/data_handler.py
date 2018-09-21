class DataSet():

    ORDERS = []

#=========================Handles Administrators Transactions==================================
 
    def get_all_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.ORDERS

    def add_new_entry(self,name,Description,quantity,price,vendor,location,image,identifier):
        '''Add new item to list'''
        item_id = len(DataSet.ORDERS) + 1
        item = {
            'id' : item_id,
            'name' : name,
            'description' : Description,
            'quantity' : quantity,
            'price' : price,
            'vendor' : vendor,
            'location' : location,
            'image' : image,
            'identifier' : identifier
        }
        DataSet.ORDERS.append(item)
        return DataSet.ORDERS

#=========================End Of Administrators Transactions==================================