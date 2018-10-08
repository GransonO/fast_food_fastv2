from ...api.v2.services.db_handler import ServiceSpace

fail_test = {
  "type": "ADMIN",
  "name": "Login_Test",
  "password": "Power"
}
admin_pass_test = {
  "type": "ADMIN",
  "name": "Admin_Login",
  "password": "password"
}

cust_pass_test = {
  "type": "CUSTOMER",
  "name": "Customer_Login",
  "password": "password"
}

wrong_type_test = {
  "type": "USER",
  "name": "Customer_Login",
  "password": "password"
}

empty_test = {}

def addUser():
      serviceSpace = ServiceSpace()
      serviceSpace.Add_user_to_db('ADMIN','Admin_Login','password','Test Store','07000100','admtest@gmail.com','This is about me.','Adm_Loc','The image','Testing')
        #Customer Entry
      serviceSpace.Add_user_to_db('CUSTOMER','Customer_Login','password','No Store','0700200','custtest@gmail.com','This is about me.','Test_Loc','The image','Testing')
    
#login fail
def test_login_fail(create_test_app): #User not in DB
    '''Test for user login'''
    response = create_test_app.post('/auth/login', json=fail_test)
    assert response.status_code == 401
    assert b'Your username or password may be wrong' in response.data

#login pass
def test_login_pass_admin(create_test_app): #User in DB
    '''Test for user login'''
    addUser()
    response = create_test_app.post('/auth/login', json=admin_pass_test)
    assert response.status_code == 202
    assert b'login success' in response.data

#login pass
def test_login_pass_cust(create_test_app): #User in DB
    '''Test for user login'''
    addUser()
    response = create_test_app.post('/auth/login', json=cust_pass_test)
    assert response.status_code == 202
    assert b'login success' in response.data

#login pass
def test_wrong_type(create_test_app): #User in DB
    '''Test for user login'''
    addUser()
    response = create_test_app.post('/auth/login', json=wrong_type_test)
    assert response.status_code == 405
    assert b'The passed type is not allowed' in response.data

#login fail 
def test_login_empty(create_test_app): #Empty json
    '''Test for user login'''
    response = create_test_app.post('/auth/login', json=empty_test)
    assert response.status_code == 403
    assert b'You cant send an empty request' in response.data
