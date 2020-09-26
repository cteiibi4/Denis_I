import sqlite3
from common.common import BASE

def create_db():
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE parts
                            (part primary key,
                             description blob,
                             cost integer ,
                             image)
                        """)

    cursor.execute("""CREATE TABLE car
                            (id integer primary key AUTOINCREMENT,
                            year integer,
                            engine_car,
                            brand_car,
                            model_car,
                            foreign key (engine_car) references engine(engine_name),  
                            foreign key (brand_car) references brand(brand_name), 
                            foreign key (model_car) references model(model_name))
                        """)

    cursor.execute("""CREATE TABLE applicability
                            (car,
                             part,
                             foreign key (car) references car(id),
                             foreign key (part) references parts(part))
                        """)
    conn.commit()


create_db()