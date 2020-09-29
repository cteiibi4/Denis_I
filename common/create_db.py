import sqlite3
from common.common import BASE


def init_db():
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS parts
                            (part primary key,
                             description blob,
                             cost integer)
                        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS car
                            (id integer primary key AUTOINCREMENT,
                            year integer,
                            engine_car,
                            brand_car,
                            model_car,
                            status integer,
                            foreign key (engine_car) references engine(engine_name),  
                            foreign key (brand_car) references brand(brand_name), 
                            foreign key (model_car) references model(model_name))
                        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS image
                            (id integer primary key AUTOINCREMENT,
                            part,
                            image,
                            foreign key (part) references parts(part))
                        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS applicability
                            (car,
                             part,
                             foreign key (car) references car(id),
                             foreign key (part) references parts(part))
                        """)
    conn.commit()
