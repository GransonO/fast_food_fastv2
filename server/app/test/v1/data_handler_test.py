class DataSet():
    item1 = {
        'id' : 1,
        'name' : 'Coke',
        'Description' : 'This is soda',
        'quantity' : 10,
        'price' : 50,
        'vendor' : 'Cocacola',
        'location' : 'Nairobi',
        'image' : 'www.this_is_my_image.com/img.png',
        'identifier' : 'drinks110'
    }

    item2 = {
        'id' : 2,
        'name' : 'Sprite',
        'Description' : 'This is Sprite',
        'quantity' : 15,
        'price' : 55,
        'vendor' : 'Sprite Kings',
        'location' : 'Mombasa',
        'image' : 'www.this_is_my_image.com/img.png',
        'identifier' : 'drinks115'
    }
    ORDERS = [] #Tested for empty list
    ENTRY_ORDERS = [] #Test for new entries
    POPULATED_ORDERS = [item1, item2] #Tested for Populated list
    DELETE_ORDERS = [item1, item2] #Test for deleting orders
    UPDATE_ENTRIES = [item1, item2] #Test for updating entries

#=========================Handles Administrators Transactions==================================
    #Get all orders
    def get_all_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.ORDERS
    
    #Get all orders from populated list
    def get_present_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.POPULATED_ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.POPULATED_ORDERS

    #Add new order
    def add_new_entry(self,name,Description,quantity,price,vendor,location,image,identifier):
        '''Add new item to list'''
        item_id = len(DataSet.ENTRY_ORDERS) + 1
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
        DataSet.ENTRY_ORDERS.append(item)
        return DataSet.ENTRY_ORDERS

    #Get specific order
    def get_specific_entry(self,num):
        '''Gets a specific order as requested'''
        if len(DataSet.POPULATED_ORDERS) < 1:
            return 'There are no items yet'
            
        else:
            result = 'The selected item does not exist'

            for each in DataSet.POPULATED_ORDERS:
                if each['id'] == num:
                    result = each

            return result

    def update_entry(self,item_id,name,description,quantity,price,vendor,location,image,identifier):
        '''Checks for passed id and edits content as passed'''
        items_status = 0
        if len(DataSet.UPDATE_ENTRIES) < 1 :
            return 'There are no items'

        else:              
            for items in DataSet.UPDATE_ENTRIES:
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
                return DataSet.UPDATE_ENTRIES

    def delete_item(self,item_id,num):
        '''Deletes an item from the admins list'''
        call_me = 0
        for item in DataSet.DELETE_ORDERS:
            if item['id'] == num:
                DataSet.DELETE_ORDERS.remove(item) 
                break

            else:
                call_me = 'Could not find the item' 

        if(call_me == 0):
            return DataSet.DELETE_ORDERS 
        else:
            return call_me
#=========================End Of Administrators Transactions==================================
