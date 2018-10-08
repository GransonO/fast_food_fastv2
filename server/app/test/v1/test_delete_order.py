user_id = {'uid':'granson275'}

#Deleting orders
def test_delete(create_test_app):
    '''Test for updating an order'''
    response = create_test_app.delete('/v1/orders/1', json=user_id)
    assert b"No Items present" not in response.data
    assert b"Coke" not in response.data
    assert b"Cocacola" not in response.data
    assert b"Nairobi" not in response.data
    assert b"drinks110" not in response.data

def test_delete_item2(create_test_app):
    '''Test for updating an order'''
    response = create_test_app.delete('/v1/orders/2', json=user_id)
    assert b"No Items present" not in response.data
    assert b"Sprite" not in response.data
    assert b"Sprite Kings" not in response.data
    assert b"Mombasa" not in response.data
    assert b"drinks115" not in response.data
