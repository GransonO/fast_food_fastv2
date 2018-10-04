#Get item 1
def test_get_specific(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders/1')
    assert response.status_code == 200
    assert b"No Items present" not in response.data
    assert b"Coke" in response.data
    assert b"This is soda" in response.data
    assert b"Cocacola" in response.data
    assert b"Nairobi" in response.data
    assert b"drinks110" in response.data

#Get item 2
def test_get_specific_two(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders/2')
    assert response.status_code == 200
    assert b"No Items present" not in response.data
    assert b"Sprite" in response.data
    assert b"Sprite Kings" in response.data
    assert b"Mombasa" in response.data
    assert b"drinks115" in response.data
    assert b"www.this_is_my_image.com/img.png" in response.data
    assert b"55" in response.data

#Get NO item present
def test_get_specific_three(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders/3')
    assert response.status_code == 200
    assert b"The selected item does not exist" in response.data
