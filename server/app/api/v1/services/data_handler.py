class DataSet():

    ORDERS = []

    def get_all_orders(self):
        '''Return all orders to the request'''
        if len(DataSet.ORDERS) < 1:
            return 'No Items present'
        else:
            return DataSet.ORDERS
        