import sqlite3
from common.common import BASE


def sql_massage(sql_request):
    conn = sqlite3.connect(BASE)
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_request)
    except sqlite3.IntegrityError:
        pass
    conn.commit()


def add_brand(brand_name, brand_id):
    request_add_brand = f'''INSERT INTO brand
                            values ({brand_name}, {brand_id})'''
    sql_massage(request_add_brand)


def add_model(model_name):
    request_add_model = f'''INSERT INTO model SET {model_name}'''
    sql_massage(request_add_model)


def add_engine(engine):
    request_add_engine = f'''INSERT INTO engine SET {engine}'''
    sql_massage(request_add_engine)


def add_car(year, engine, brand, model):
    request_add_car = f'''INSERT INTO car
                            values ({year}, {engine}, {brand}, {model})'''
    sql_massage(request_add_car)


def add_part(part, description, cost, image):
    request_add_part = f'''INSERT INTO parts
                            values ({part}, {description}, {cost}, {image})'''
    sql_massage(request_add_part)


def add_applicability(id_car, part_no):
    request_add_applicability = f'''INSERT INTO applicability
                            values ({id_car}, {part_no})'''
    sql_massage(request_add_applicability)
