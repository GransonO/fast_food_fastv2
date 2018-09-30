#Call method during setup to add all tables
from instantiate_db import DatabaseBase

def first_call():
    dbase = DatabaseBase()
    return dbase.order_of_creation()

if __name__ == '__main__':
    print(first_call())
