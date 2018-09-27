
ADMIN = []
ORDERS = []
NEW_ORDERS = []
DEL_ORDERS = []
UPDATE_ORDERS = []

#=========================Handles Administrators Transactions==================================
#Get all orders
def test_get_all_orders():
    '''Return all orders to the request'''
    ORDERS.clear()
    if len(ORDERS) < 1:
        return 'No Items present'
    else:
        return ORDERS
    assert ORDERS[0] == False
    assert len(ORDERS) == 0
    assert len(ORDERS) != 1

#Add new order
def test_add_new_entry():
    '''Add new item to list'''
    ORDERS.clear()
    item_id = len(ORDERS) + 1
    item = {
        'id' : item_id,
        'name' : 'Coke',
        'description' : 'This is soda',
        'quantity' : 10,
        'price' : 50,
        'vendor' : 'Cocacola',
        'location' : 'Nairobi',
        'image' : 'image',
        'identifier' : 'identifier'
    }
    ORDERS.append(item)
    #test if entry added to list
    assert ORDERS[0] == item
    assert len(ORDERS) == 1
    assert len(ORDERS) != 0

#Get specific order
def test_get_specific_entry(num = 1):
    '''Gets a specific order as requested'''
    if len(ORDERS) < 1:
        return 'There are no items yet'
        
#Test if theres no item in list        
assert test_get_specific_entry() == 'There are no items yet'
assert len(ORDERS) == 0
assert len(ORDERS) != 1

def test_not_existent(num = 1):
    item_id = len(NEW_ORDERS) + 1
    item = {
        'id' : item_id,
        'name' : 'Coke',
        'description' : 'This is soda',
        'quantity' : 10,
        'price' : 50,
        'vendor' : 'Cocacola',
        'location' : 'Nairobi',
        'image' : 'image',
        'identifier' : 'identifier'
    }
    NEW_ORDERS.append(item)
    if len(NEW_ORDERS) < num:

        result = 'The selected item does not exist'
    else:
        
        for each in NEW_ORDERS:
            if each['id'] == num:
                result = each

    return result

assert test_not_existent(1) == {'id' : 1,'name' : 'Coke', 'description' : 'This is soda', 'quantity' : 10,'price' : 50, 'vendor' : 'Cocacola','location' : 'Nairobi', 'image' : 'image','identifier' : 'identifier' }
assert test_not_existent(4) == 'The selected item does not exist'

def test_update_entry():
    '''Checks for passed id and edits content as passed'''

    if len(UPDATE_ORDERS) < 1 :
        return 'There are no items'

    else:              
        for items in UPDATE_ORDERS:
            if items['id'] == 1:
                '''Get detail of specific item'''
                items['name'] = 'Item Name'
                items['description'] = 'Item describe'
                items['quantity'] = 10
                items['price'] = 1000
                items['vendor'] = 'Granson'
                items['location'] = 'Nairobi'
                items['image'] = 'img-url'
                items['identifier'] = 'identifier'
                items_status = 0

                break
            else:
                items_status = 1
            
        if items_status == 1:
            return 'Could not find the passed item'
        else:
            return UPDATE_ORDERS
assert test_update_entry() == 'There are no items'

def test_update_with_entry(num = 1):
    UPDATE_ORDERS.clear()
    '''Checks for passed id and edits content as passed'''
    item = {
        'id' : 1,
        'name' : 'Coke',
        'description' : 'This is soda',
        'quantity' : 10,
        'price' : 50,
        'vendor' : 'Cocacola',
        'location' : 'Nairobi',
        'image' : 'image',
        'identifier' : 'identifier'
    }
    UPDATE_ORDERS.append(item)

    if len(UPDATE_ORDERS) < 1 :
        return 'There are no items'

    else:              
        for items in UPDATE_ORDERS:
            if items['id'] == num:
                '''Get detail of specific item'''
                items['name'] = 'Item Name'
                items['description'] = 'Item describe'
                items['quantity'] = 10
                items['price'] = 1000
                items['vendor'] = 'Granson'
                items['location'] = 'Nairobi'
                items['image'] = 'img-url'
                items['identifier'] = 'identifier'
                items_status = 0

                break
            else:
                items_status = 1
            
        if items_status == 1:
            return 'Could not find the passed item'
        else:
            return UPDATE_ORDERS

assert test_update_with_entry(1)[0] == {'id' : 1,'name' : 'Item Name','description' : 'Item describe','quantity' : 10,'price' : 1000,'vendor' : 'Granson', 'location' : 'Nairobi','image' : 'img-url', 'identifier' : 'identifier'}
assert test_update_with_entry(4) == 'Could not find the passed item'
assert len(test_update_with_entry(1)) == 1

def test_delete_item(num = 1):
    '''Deletes an item from the admins list'''
    item_id = len(DEL_ORDERS) + 1
    item = {
        'id' : item_id,
        'name' : 'Coke',
        'description' : 'This is soda',
        'quantity' : 10,
        'price' : 50,
        'vendor' : 'Cocacola',
        'location' : 'Nairobi',
        'image' : 'image',
        'identifier' : 'identifier'
    }
    DEL_ORDERS.append(item)

    for item in DEL_ORDERS:
        if item['id'] == num:
            DEL_ORDERS.remove(item)

    return DEL_ORDERS  

assert test_delete_item(1) == []
assert len(test_delete_item(1)) == 0
assert len(test_delete_item(1)) != 1 
