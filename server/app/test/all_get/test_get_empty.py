#Get all orders N.B When the list is empty
def test_get_all(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders')
    assert response.status_code == 200

def test_get_all_items(create_test_app):
    '''Test for get call orders'''
    response = create_test_app.get('/v1/orders')
    assert b"No Items present" in response.data
