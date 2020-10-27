from sqlalchemy import create_engine, Table, String, Boolean, Date, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .common import BASE

engine_db = create_engine(f'sqlite:///{BASE}', echo=False)

Enginetech = declarative_base()

association_table = Table('applicability', Enginetech.metadata,
                          Column('car', Integer, ForeignKey('cars.id')),
                          Column('part', String, ForeignKey('parts.part')),
                          UniqueConstraint('car', 'part')
                          )

association_table_kit_part = Table('kits-part', Enginetech.metadata,
                              Column('part', String, ForeignKey('parts.part')),
                              Column('kit', String, ForeignKey('kits.kit')),
                              UniqueConstraint('part', 'kit')
                              )

association_table_kit_car = Table('applicability-kits', Enginetech.metadata,
                              Column('car', Integer, ForeignKey('cars.id')),
                              Column('kit', String, ForeignKey('kits.kit')),
                              UniqueConstraint('car', 'kit')
                              )


class Part(Enginetech):
    __tablename__ = 'parts'
    part = Column(String, primary_key=True, unique=True)
    description = Column(String)
    cost = Column(Integer)
    update_date = Column(Date)
    cars = relationship('Car',
                        secondary=association_table,
                        back_populates='parts')
    # images = relationship('Image')
    images = relationship('Image', back_populates='part')

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
    UniqueConstraint(year, engine_car, brand_car, model_car)

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
    part = relationship('Part', back_populates='images')
    part_id = Column(String, ForeignKey('parts.part'))

    def __init__(self, image):
        self.image = image


class Kit(Enginetech):
    __tablename__ = 'kits'
    id = Column(Integer, primary_key=True)
    kit = Column(String, unique=True)
    kit_img = Column(String)
    kit_type = Column(String)

    def __init__(self, kit):
        self.kit = kit


Enginetech.metadata.create_all(engine_db)
