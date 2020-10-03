import sqlite3
from sqlalchemy import create_engine, Table, String, Boolean, Date, Column, Integer, BLOB, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from common import BASE

engine = create_engine(f'sqlite:///{BASE}', echo=True)

Enginetech = declarative_base()

association_table = Table('applicability', Enginetech.metadata,
                          Column('car', Integer, ForeignKey('cars.id')),
                          Column('part', String, ForeignKey('parts.part'))
                          )

class Part(Enginetech):
    __tablename__ = 'parts'
    part = Column(String, primary_key=True)
    description = Column(BLOB)
    cost = Column(Integer)
    update_date = Column(Date)
    cars = relationship('Car',
                           secondary=association_table,
                           back_populates='parts')
    images = relationship('Image')

    def __init__(self, part, description, cost, update_date):
        self.part = part
        self.description = description
        self.cost = cost
        self.update_date = update_date


class Car(Enginetech):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    engine_car = Column(String)
    brand_car = Column(String)
    model_car = Column(String)
    status = Column(Boolean)
    parts = relationship('Part',
                            secondary=association_table,
                            back_populates='cars')

    def __init__(self, year, engine_car, brand_car, model_car, status):
        self.year = year
        self.engine_car = engine_car
        self.brand_car = brand_car
        self.model_car = model_car
        self.status = status

    def __repr__(self):
        return f'Сканируем машину {self.brand_car} {self.model_car} {self.year} года с двигателем {self.engine_car}'


class Image(Enginetech):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    part = Column(String, ForeignKey('parts.part'))

    def __init__(self, image, part):
        self.image = image
        self.part = part


Enginetech.metadata.create_all(engine)

# conn = sqlite3.connect(BASE)
# cursor = conn.cursor()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS parts
#                         (part primary key,
#                          description blob,
#                          cost integer,
#                          update_date)
#                     """)
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS car
#                         (id integer primary key AUTOINCREMENT,
#                         year integer,
#                         engine_car,
#                         brand_car,
#                         model_car,
#                         status integer,
#                         foreign key (engine_car) references engine(engine_name),
#                         foreign key (brand_car) references brand(brand_name),
#                         foreign key (model_car) references model(model_name))
#                     """)
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS image
#                             (id integer primary key AUTOINCREMENT,
#                             part,
#                             image,
#                             foreign key (part) references parts(part))
#                         """)
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS applicability
#                         (car,
#                          part,
#                          foreign key (car) references car(id),
#                          foreign key (part) references parts(part))
#                     """)
# conn.commit()
