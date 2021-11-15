import configparser

config = configparser.ConfigParser()

config.add_section('sqlalchemy')
config.set('sqlalchemy', 'host', 'db')
config.set('sqlalchemy', 'user', 'root')
# config.set('sqlalchemy', 'port', '5000')
config.set('sqlalchemy', 'password', 'root')
config.set('sqlalchemy', 'database', 'covid')

with open("configfile.ini", 'w') as configfile:
    config.write(configfile) 
