import configparser

config = configparser.ConfigParser()

config.add_section('sqlalchemy')
config.set('sqlalchemy', 'host', 'localhost')
config.set('sqlalchemy', 'user', 'qasim')
config.set('sqlalchemy', 'port', '5000')
config.set('sqlalchemy', 'password', 'Qwer_1234-')
config.set('sqlalchemy', 'db', 'lostnfound')

with open("configfile.ini", 'w') as configfile:
    config.write(configfile) 
