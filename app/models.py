from enum import unique

from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import null
# from werkzeug.datastructures import V
from app import db
from sqlalchemy import Integer, String, ForeignKey, Column, DATETIME,Float
import json
# Models

class Province(db.Model):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key = True)
    name = Column(String(60))
    lat = Column(Integer)
    long = Column(Integer)
    cid = Column(Integer, ForeignKey('countries.id'), nullable = True)
    prov_stat = relationship('ProvinceStat', backref="province", cascade="all, delete-orphan", uselist=False)
    cities = relationship('City', backref="province", cascade="all, delete-orphan", lazy="dynamic")
    
    
    def __init__(self, id, name, lat, long): #id,cid,name,lat,long
        self.name = name
        self.id = id
        self.lat = lat
        self.long = long

    def __repr__(self):
        return '' % self.name
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ProvinceStat(db.Model):
    __tablename__ = "province_stats"

    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('provinces.id'), nullable= False)
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
    
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, id, date_, confirmed, deaths, recovered, confirmed_diff, deaths_diff, recover_diff, last_update, active, active_diff, fatality_rate):
        self.id = id
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




class City(db.Model):
    __tablename__ = "cities"
    id = Column(Integer, primary_key = True)
    pid = Column(Integer, ForeignKey('provinces.id'),nullable=False)
    lat = Column(Integer)
    long = Column(Integer)
    citystat = relationship('CityStat', backref="city", cascade="all, delete-orphan", lazy="dynamic")
    # ForeignKeyConstraint(['pid'], ['province.pid'])
    

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, id, name, lat, long):
        self.id = id
        # self.pid = pid
        self.name = name
        self.lat = lat
        self.long = long
        

    def __repr__(self):
        return '' % self.id

class CityStat(db.Model):
    __tablename__ = "city_stats"
    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    city_id = Column(Integer, ForeignKey('cities.id'),nullable=False)
    date = Column(DATETIME)
    last_update = Column(DATETIME)
    fips = Column(Integer)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    confirmed_diff = Column(Integer)
    deaths_diff = Column(Integer)
    

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, id, date, last_update, fips, confirmed, deaths, confirmed_diff, deaths_diff):
        self.date = date
        self.last_update = last_update
        self.fips = fips
        self.confirmed = confirmed
        self.deaths = deaths
        self.confirmed_diff = confirmed_diff
        self.deaths_diff = deaths_diff
        self.id = id

    def __repr__(self):
        return '' % self.id

class Country(db.Model):

    __tablename__ = "countries"
    
    iso = Column(String(60), nullable = False)
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    prov = relationship('Province', backref="country", cascade="all, delete-orphan", lazy="dynamic")
    # prov = relationship('Province',backref='country',cascade="all, delete, save")  # cascade?  # backref?? 



    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, iso, name,id):
        self.iso = iso
        self.name = name
        self.id = id

    def __repr__(self):
        return '' % self.id

    @classmethod
    def test(cls,pagee,serial,obj):
        pid=serial
        datas = ''
        for a in pagee:
            a=a.decode("utf-8")
            datas = datas + a
        dctnn = json.loads(datas)
        info = []
        city_=[]
        prov=[]
        city_dataa=[]
        for a in dctnn:
            for i in dctnn[a]:  
                for key, val in i.items():

                    # print(key , "-------------------",val)
                    if key != "region":
                        info.append(val)
                        # print(key,"---->",val)
                    if key == "region":
                        for a , b in val.items():
                            if a == 'cities':
                                city_dataa.append(b)
                                # for z in b:
                                #     if z: 
                                #         # print(a,"----->",z)
                                #         for u , v in z.items():
                                #             city_.append(v)
                                #         city_data.append(city_)
                                #         city_.pop()

                                        # city_data = City(serial+1,city_[-10],city_[-7],city_[-6])
                                        # serial = serial + 1
                                        # city_stats = CityStat(serial+1,serial-1,city_[-9],city_[-1],city_[-8],city_[-5],city_[-4],city_[-3],city_[-2])
                                        # serial=serial+1
                                        # db.session.add(city_data)
                                        # db.session.add(city_stats)
                            else:
                                prov.append(b)
        
                         #self, name,cid,id,lat,long): id,cid,name,lat,long
                
                insert_prov = Province(pid,prov[-3],prov[-1],prov[-2])
                # insert_prov.country=obj
                insert_prov.country= obj
                
                insert_prov_status = ProvinceStat(serial+1,info[-11],info[-10],info[-9],info[-8],info[-7],info[-6],info[-5],info[-4],info[-3],info[-2],info[-1]) 
                insert_prov_status.provinces = insert_prov
                # Province.prov_stat.provinces.append(insert_prov_status)
                # insert_prov_status.provinces=insert_prov
                
                pid = pid + 1
                db.session.add(insert_prov)
                db.session.commit()
                serial = serial + 2

                if city_dataa:
                    for a in city_dataa:
                        print("city----------------->",a)
                        for b in a:
                            for u , v in b.items():
                                city_.append(v)
                            city_data = City(serial+1,city_[-10],city_[-7],city_[-6])
                            serial = serial + 1
                            city_stats = CityStat(serial+1,city_[-9],city_[-1],city_[-8],city_[-5],city_[-4],city_[-3],city_[-2])
                            serial=serial+1

                            city_data.province = insert_prov
                            city_stats.city = city_data

                            city_.pop()

                        db.session.commit()


                        # for b in a:
                        #     print("b------->",a)
                        #     city_data = City(serial+1,b[-10],b[-7],b[-6])
                        #     serial = serial + 1
                        #     city_stats = CityStat(serial+1,b[-9],b[-1],b[-8],b[-5],b[-4],b[-3],b[-2])
                        #     serial=serial+1
                        #     city_data.city = insert_prov
                        #     city_stats.province = city_data
                        #     db.session.add(city_data)
                        #     db.session.add(city_stats)
                    city_dataa.clear()
                




                
                        

                        
                # print(info)
                print("<------------------------------------------->")


                
                serial = serial + 1
        # print(city_)
        print(prov)
        return serial
    