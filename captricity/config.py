from os import path

captricity_token="yourtoken"
data_dir = "some_place"
db_uri = "sqlite:////{}".format(path.join(data_dir, "captricity.db"))

class ConfigBase(object):
    # SQLALCHEMY_DATABASE_URI = connection_uri
    UPLOAD_FOLDER = path.join(data_dir)


class ConfigDev(ConfigBase):
    DEBUG = True
    SECRET_KEY = "SOOOOOO SECRET!!!!!!!"


class ConfigProd(ConfigBase):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '739273587a4647f7bba9782edcbccadbe7a0b0b0aa8b4b488689fe47c8090e28'
    #SERVER_NAME = "something"
    #APPLICATION_ROOT = "something else"
