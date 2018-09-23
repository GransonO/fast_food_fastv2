class DataSet():

    ORDERS = []

#=========================Handles Administrators Transactions==================================
    #Get all orders
    def get_all_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.ORDERS

    #Add new order
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

    #Get specific order
    def get_specific_entry(self,num):
        '''Gets a specific order as requested'''
        if len(DataSet.ORDERS) < 1:
            return 'There are no items yet'
            
        else:
            result = 'The selected item does not exist'

            for each in DataSet.ORDERS:
                if each['id'] == num:
                    result = each

            return result

#=========================End Of Administrators Transactions==================================
