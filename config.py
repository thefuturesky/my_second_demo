import os
SECRET_KEY =  os.urandom(24)
DEBUG = True

USERNAME = 'root'
PASSWORD = 'python'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'second_demo'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,\
                                    PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
