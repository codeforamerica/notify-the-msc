class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    EMAIL_RECIPIENT = "daniel@codeforamerica.org"


class DevelopmentConfig(Config):
    DEBUG = True
    EMAIL_RECIPIENT = "daniel@codeforamerica.org"


class TestingConfig(Config):
    TESTING = True
