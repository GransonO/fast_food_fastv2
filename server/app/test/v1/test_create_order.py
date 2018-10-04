TEST_DATA = {
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

#Posting orders
def test_post(create_test_app):
    '''Test for posting a new order'''
    response = create_test_app.post('/v1/orders', json=TEST_DATA)
    assert response.status_code == 200
    assert b"Coke" in response.data
    assert b"Cocacola" in response.data
    assert b"www.this_is_my_image.com/img.png" in response.data
        
