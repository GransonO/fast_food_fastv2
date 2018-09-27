class DataSet():

    ADMIN = []
    ORDERS = []

    USERS = []
    USER_ORDERS = []

#=========================Handles Administrators Transactions==================================

#Get all orders
    def get_all_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.ORDERS

    #Adds a new item to the list
    def add_to_list(self,name,Description,quantity,price,vendor,location,image,identifier): 
        '''Adds items to list'''
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

    def add_new_entry(self,name,Description,quantity,price,vendor,location,image,identifier):
        '''Pre-adding new entry processing'''
        item_status = 0
        if len(DataSet.ORDERS) > 0:

            for item in DataSet.ORDERS:
                if item['name'] == name:
                    item_status = 'Dear human, this item already exists'                    
                    break

                else:
                    item_status = 1

            if item_status == 1:
                '''Item does not exist'''
                result = DataSet.add_to_list(self,name,Description,quantity,price,vendor,location,image,identifier)
                return result
                
            else:
                return item_status

        else:
            '''No item in list'''
            result = DataSet.add_to_list(self,name,Description,quantity,price,vendor,location,image,identifier)
            return result

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

    def update_entry(self,item_id,name,description,quantity,price,vendor,location,image,identifier):
        '''Checks for passed id and edits content as passed'''
        items_status = 0
        if len(DataSet.ORDERS) < 1 :
            return 'There are no items'

        else:              
            for items in DataSet.ORDERS:
                if items['id'] == item_id:
                    '''Get detail of specific item'''
                    items['name'] = name
                    items['description'] = description
                    items['quantity'] = quantity
                    items['price'] = price
                    items['vendor'] = vendor
                    items['location'] = location
                    items['image'] = image
                    items['identifier'] = identifier
                    items_status = 0
                    break
                else:
                    items_status = 1
                
            if items_status == 1:
                return 'Could not find the passed item'
            else:
                return DataSet.ORDERS

    def delete_item(self,item_id,num):
        '''Deletes an item from the admins list'''
        status = 0
        for item in DataSet.ORDERS:
            if item['id'] == num:
                DataSet.ORDERS.remove(item)  
                status = DataSet.ORDERS
                break
            else:
                status = 0
        if(status == 0):
            return 'The selected item could not be found'
        else:
            return DataSet.ORDERS    

#=========================End Of Administrators Transactions==================================
