from ...api.v2.services.db_handler import ServiceSpace
register_user = {
  "type": "ADMIN",
  "name": "A Sign Up",
  "vendor_name": "Admin Store",
  "password": "ADMIN SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@EMAIL.COM"
}

register_wrong = {
  "type": "ADMINISTRATOR",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "ADMIN SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@EMAIL.COM"
}

register_empty = {}

register_key_error = {
  "type": "ADMINISTRATOR",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "ADMIN SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG"
}

#Sign up
def test_signup_pass(create_test_app): #User sign up pass
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_user)
    assert response.status_code == 201
    assert b'Thanks A Sign Up for creating an ADMIN account with us.' in response.data
    assert b'A Sign Up' in response.data
    assert b'Admin Store' in response.data
    assert b'345678287' in response.data
    assert b'XXX@EMAIL.COM' in response.data

#Sign up
def test_signup_empty(create_test_app): #User sign up fail
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_empty)
    assert response.status_code == 403
    assert b'You cant send an empty request' in response.data

#Sign up
def test_signup_wrong(create_test_app): #User sign up fail
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_wrong)
    assert response.status_code == 405
    assert b'Sorry Wrong Sign Up, the type value passed cannot be processed' in response.data


#Sign up
def test_signup_type_error(create_test_app): #User sign up empty error
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_wrong)
    assert response.status_code == 405
    assert b'Sorry Wrong Sign Up, the type value passed cannot be processed' in response.data

#Sign up
def test_signup_key_error(create_test_app): #User sign up key error
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_key_error)
    assert response.status_code == 400
    assert b'Please enter the data as specified' in response.data
