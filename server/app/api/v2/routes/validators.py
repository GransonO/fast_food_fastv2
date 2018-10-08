import re

class Validation():
    '''Validations for data types'''
    def email_Validation(self,name):

        allowed = ['.com','.co.ke']
        match = re.findall(r'\S+@\S+', name)
        if len(match) >= 1:                
            result = match[0]
            if result.endswith(allowed[1]) or result.endswith(allowed[0]):
                return result

    def password_Validation(self,name):
        '''Validates password'''
        if len(name) < 6:
            return 'password length should have at least 6 characters'

        alpha = re.findall(r'[A-Z]',name)
        if len(alpha) < 1:
            return 'Your password lacks a capital character'

        small = re.findall(r'[a-z]',name)
        if len(small) < 1:
            return 'Your password lacks a small character'

        match = re.findall(r'\d+', name)
        result = len(match)
        if result >= 1:
            return 'Pass'
        else:
            return 'You need at least one integer in your password'