# from _typeshed import Self
from enum import unique
import uuid
import logging
from sqlalchemy.orm import backref, relationship, lazyload
from sqlalchemy.sql.expression import null
# from werkzeug.datastructures import V
from app import db
from sqlalchemy import Integer, String, ForeignKey, Column, DATETIME,Float
import json
# Models
logging.basicConfig(level= logging.DEBUG)

# Province Model
class Province(db.Model):
    __tablename__ = "provinces"

    id = Column(String(255), primary_key = True)
    name = Column(String(60))
    lat = Column(Integer)
    long = Column(Integer)
    cid = Column(String(255), ForeignKey('countries.id'), nullable = True)
    prov_stat = relationship('ProvinceStat', backref="province", cascade="all, delete-orphan", uselist=False)
    cities = relationship('City', backref="province", cascade="all, delete-orphan", lazy="dynamic")
    
    
    def __init__(self, name, lat, long): #id,cid,name,lat,long
        self.name = name
        self.id = uuid.uuid4()
        self.lat = lat
        self.long = long

    def __repr__(self):
        return '' % self.name
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def to_json(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'lat' : self.lat,
            'long' : self.long,
            'province_stat' : self.prov_stat.to_json(),
            'cities' : [city.to_json() for city in self.cities.all()]
        }
    @classmethod
    def from_json_body(cls, data):
        print(data)
        insert_prov = Province(data['province'],data['lat'],data['long'])
        db.session.add(insert_prov)
        return insert_prov

    def search_json(self):
        # result = Province.query.filter_by(cid=cid).all()
        # chat.query.join(user.chats).filter(user.id == 1).all()
        return {
            'id' : self.id,
            'name' : self.name,
            'lat' : self.lat,
            'long' : self.long,
            'province_stat' : self.prov_stat.to_json() if self.prov_stat else {},
            'cities' : [city.to_json() for city in self.cities.all()]
        }

    # def search_json(iso):
    #     return {
    #             "id": Country.query.filter_by(iso=iso).first().id,
    #             "iso": iso,
    #             "name": Country.query.filter_by(iso=iso).first().name,
    #             "provinces": [province.search_json() for province in Province.query.filter_by(cid=Country.query.filter_by(iso=iso).id.all())]
                
    #     }

class ProvinceStat(db.Model):
    __tablename__ = "province_stats"

    id = Column(String(255), primary_key = True)
    pid = Column(String(255), ForeignKey('provinces.id'), nullable= False)
    date_ = Column(DATETIME)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    confirmed_diff = Column(Integer)
    deaths_diff = Column(Integer)
    recover_diff = Column(Integer) 
    last_update = Column(String(30))
    active = Column(Integer)
    active_diff = Column(Integer)
    fatality_rate = Column(Float)

    def to_json(self):
        return{
            "id" : self.id,
            "pid" : self.pid,
            "date" : self.date_,
            "confirmed" : self.confirmed,
            "deaths" : self.deaths,
            "recovered" : self.recovered,
            "confirmed_diff" : self.confirmed_diff,
            "deaths_diff" : self.deaths_diff,
            "recover_diff" : self.recover_diff,
            "last update" : self.last_update,
            "active" : self.active,
            "active_diff" : self.active_diff,
            "fatality rate": self.fatality_rate
        }
    
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, date_, confirmed, deaths, recovered, confirmed_diff, deaths_diff, recover_diff, last_update, active, active_diff, fatality_rate):
        self.id = uuid.uuid4()
        self.date_ = date_
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.confirmed_diff = confirmed_diff
        self.deaths_diff = deaths_diff
        self.recover_diff = recover_diff
        self.last_update = last_update
        self.active = active
        self.active_diff =active_diff
        self.fatality_rate =  fatality_rate
        
    
    
        

    def __repr__(self):
        return '' % self.id
    
    @classmethod
    def from_json_body(cls, Data):
        insert_prov_status = ProvinceStat(Data['date'], Data['confirmed'], Data['deaths'], Data['recovered'], Data['confirmed_diff'], Data['deaths_diff'], Data['recovered_diff'],Data['last_update'],Data['active'],Data['active_diff'],Data['fatality_rate']) 
        db.session.add(insert_prov_status)
        return insert_prov_status


class City(db.Model):
    __tablename__ = "cities"

    id = Column(String(255), primary_key = True)
    pid = Column(String(255), ForeignKey('provinces.id'),nullable=False)
    lat = Column(Integer)
    long = Column(Integer)
    citystat = relationship('CityStat', backref="city", cascade="all, delete-orphan", lazy="dynamic")
    # ForeignKeyConstraint(['pid'], ['province.pid'])
    
    def to_json(self):
        return {
            'id' : self.id,
            'pid' : self.pid,
            'lat' : self.lat,
            'long' : self.long,
            'city_stats' : [city.to_json() for city in self.citystat.all()]
        }
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, lat, long):
        self.id = uuid.uuid4()
        # self.pid = pid
        self.name = name
        self.lat = lat
        self.long = long
        

    def __repr__(self):
        return '' % self.id

    @classmethod
    def from_json_body(cls, data):
        city_data = City(data['name'],data['lat'],data['long'])
        db.session.add(city_data)
        return city_data


class CityStat(db.Model):
    __tablename__ = "city_stats"
    id = Column(String(255), primary_key = True)
    name = Column(String(20))
    city_id = Column(String(255), ForeignKey('cities.id'),nullable=False)
    date = Column(DATETIME)
    last_update = Column(DATETIME)
    fips = Column(Integer)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    confirmed_diff = Column(Integer)
    deaths_diff = Column(Integer)
    
    def to_json(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "city id" : self.city_id,
            "date" : self.date,
            "last update" : self.last_update,
            "fips" : self.fips,
            "confirmed" : self.confirmed,
            "deaths" : self.deaths,
            "confirmed_diff" : self.confirmed_diff,
            "deaths_diff" : self.deaths_diff
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, date, last_update, fips, confirmed, deaths, confirmed_diff, deaths_diff):
        self.date = date
        self.last_update = last_update
        self.fips = fips
        self.confirmed = confirmed
        self.deaths = deaths
        self.confirmed_diff = confirmed_diff
        self.deaths_diff = deaths_diff
        self.id = uuid.uuid4()

    def __repr__(self):
        return '' % self.id
    
    @classmethod
    def from_json_body(cls, data):
        city_stats = CityStat(data['date'],data['last_update'],data['fips'],data['confirmed'],data['deaths'],data['confirmed_diff'],data['deaths_diff'])
        db.session.add(city_stats)
        return city_stats


class Country(db.Model):

    __tablename__ = "countries"
    
    iso = Column(String(60), nullable = False)
    name = Column(String(50), nullable = False)
    id = Column(String(255), primary_key = True)
    prov = relationship('Province', backref="country", cascade="all, delete-orphan", lazy="dynamic")
    # prov = relationship('Province',backref='country',cascade="all, delete, save")  # cascade?  # backref?? 



    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, iso, name):
        self.id = uuid.uuid4()
        self.iso = iso
        self.name = name

    def __repr__(self):
        return '' % self.id
    # data.query.filter_by(item_name=name).filter_by(location=loc).first()
    def search_json(iso):
        return {
                "id": Country.query.filter_by(iso=iso).first().id,
                "iso": iso,
                "name": Country.query.filter_by(iso=iso).first().name,
                "provinces": [province.search_json() for province in Province.query.filter_by(cid=Country.query.filter_by(iso=iso).first().id).all()]

                # chat.query.join(user.chats).filter(user.id == 1).all()
                
        }

    def to_json(self):
        return {
                "id":self.id,
                "iso": self.iso,
                "name": self.name,
                "provinces": [province.to_json() for province in self.prov.all()]
                
        }

    @classmethod
    def from_json_body(cls, data):
        country_obj = Country(iso = data['iso'], name = data['name'])
        db.session.add(country_obj)
        return country_obj

    @classmethod
    def test(cls,data,country_obj):
        logging.debug('<------------------>')
        if not data.get("data"):
            return

        # # TODO verify
        # for stats in data['data']:
        #     province_obj = Province.from_json_body(stats['region']) #inserting name lat long to Province
        #     province_obj.country = country_obj
        #     provincial_stats = ProvinceStat.from_json_body(stats)
        #     provincial_stats.province = province_obj



        for i in range(len(data['data'])):
            insert_province = Province.from_json_body(data['data'][i]['region'])
            insert_province.country= country_obj

            insert_prov_stats = ProvinceStat.from_json_body(data['data'][i]) #inserting province stats
            insert_prov_stats.province = insert_province #relationship one-many
            # db.session.commit()
            if not data['data'][i]['region']['cities']:
                return 
        
            for single_city in data['data'][i]['region']['cities']:
                city_data = City.from_json_body(single_city)      #inserting city data
                city_stats = CityStat.from_json_body(single_city) #inserting city stats
                city_data.province = insert_province #relationship one-many
                city_stats.city = city_data #relationship one-many
                db.session.commit()
        print('<--------- data added--------->')
        return 0

        
    