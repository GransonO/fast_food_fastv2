class Config:
    '''Base Config properties'''
    DEBUG = False
    TESTING = False


class DevelopmentConfiguration(Config):
    '''App Properties during development phase'''
    DEBUG = True
    TESTING = True


class TestingConfiguration(Config):
    '''App Properties during Testing phase'''
    DEBUG = True
    TESTING = True


class ProductionConfiguration(Config):
    '''App Properties during Production phase'''
    DEBUG = False
    TESTING = False


App_Configurations = {
    'Developing': DevelopmentConfiguration,
    'Testing': TestingConfiguration,
    'Production': ProductionConfiguration
}
