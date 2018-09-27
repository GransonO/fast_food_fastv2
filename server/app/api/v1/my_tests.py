ORDERS = [{'id':1,'name':'cake'},{'id':2,'name':'soda'},{'id':3,'name':'sweets'}]

def update_specific_entry(num):
    for x in ORDERS:
        if x['id'] == num:
            x['name'] = 'Juice'
            break
    
    print(ORDERS)

update_specific_entry(2)   

def get_specific_entry(num):
    if len(ORDERS) < 1:
        print('There are no items yet')

    else:
        result = 'The selected item could not be retrieved'

        for each in ORDERS:
            if each['id'] == num:
                result = each

        print(result)

get_specific_entry(4)

def post_entry(name):
    item_status = 0
    if len(ORDERS) > 0:

        for item in ORDERS:
            if item['name'] == name:
                item_status = 'Dear human, this item already exists'
                break

            else:
                item_status = 1

        print(item_status)

post_entry('Tea')

def delete_item(item_id,num):
    '''Deletes an item from the admins list'''
    for item in ORDERS:
        if item['id'] == num:
            ORDERS.remove(item)
    return ORDERS

print(delete_item('uid',1))
