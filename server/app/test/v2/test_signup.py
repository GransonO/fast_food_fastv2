from ...api.v2.services.db_handler import ServiceSpace
register_user = {
  "type": "ADMIN",
  "name": "A Sign Up",
  "vendor_name": "Admin Store",
  "password": "Admin7SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}

register_wrong = {
  "type": "ADMINISTRATOR",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "Admin7SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}

register_empty = {}

register_key_error = {
  "type": "ADMINISTRATOR",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "Admin7SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG"
}


register_wrong_email = {
  "type": "ADMIN",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "Admin7SIGN",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.COM"
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
    assert b'XXX@email.com' in response.data

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
    assert response.status_code == 400
    assert b'Sorry Wrong Sign Up, the type value passed cannot be processed' in response.data

#Sign up
def test_signup_key_error(create_test_app): #User sign up key error
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_key_error)
    assert response.status_code == 400
    assert b'Please enter the data as specified' in response.data

#Sign up
def test_wrong_email(create_test_app): #User sign up key error
    '''Test for user sign up'''
    response = create_test_app.post('/auth/signup', json=register_wrong_email)
    assert response.status_code == 400
    assert b'Email does not conform to standards( yyy@xxx.(com or co.ke))' in response.data


register_wrong_pass1 = {
  "type": "ADMIN",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "Admin",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}

register_wrong_pass2 = {
  "type": "ADMIN",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "adminvsh7dg",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}

register_wrong_pass3 = {
  "type": "ADMIN",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "ADSFSDSSHS7",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}

register_wrong_pass4 = {
  "type": "ADMIN",
  "name": "Wrong Sign Up",
  "vendor_name": "Admin Store",
  "password": "ADssshuhu",
  "about": "THIS IS IT",
  "location": "NAIROBI",
  "image_url": "IMAGE.PNG",
  "phone_no": "345678287",
  "email": "XXX@email.com"
}
#Sign up
def test_wrong_password(create_test_app): #User sign up key error
    '''Test for user sign up'''
    response1 = create_test_app.post('/auth/signup', json=register_wrong_pass1)
    assert response1.status_code == 400
    assert b'password length should have at least 6 characters' in response1.data

    response2 = create_test_app.post('/auth/signup', json=register_wrong_pass2)
    assert response2.status_code == 400
    assert b'Your password lacks a capital character' in response2.data

    response3 = create_test_app.post('/auth/signup', json=register_wrong_pass3)
    assert response3.status_code == 400
    assert b'Your password lacks a small character' in response3.data

    response4 = create_test_app.post('/auth/signup', json=register_wrong_pass4)
    assert response4.status_code == 400
    assert b'You need at least one integer in your password' in response4.data
