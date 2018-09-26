#Get all orders N.B When the list is populated
def test_get_all(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders/present')
    assert response.status_code == 200
    assert b"No Items present" not in response.data
    assert b"Coke" in response.data
    assert b"This is soda" in response.data
    assert b"Cocacola" in response.data
    assert b"Nairobi" in response.data
    assert b"Mombasa" in response.data
    assert b"Sprite Kings" in response.data
    assert b"www.this_is_my_image.com/img.png" in response.data
    assert b"drinks110" in response.data
    assert b"drinks115" in response.data
    