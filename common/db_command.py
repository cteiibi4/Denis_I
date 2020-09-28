import sqlite3
from common.common import BASE


def sql_massage(sql_request):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    result = cursor.lastrowid
    conn.commit()
    return result


def check_row(request_check_row):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(request_check_row)
    check = cursor.fetchone()
    conn.commit()
    return check


def add_car(year, engine, brand, model, status):
    request_check_car = f'''SELECT id FROM car WHERE brand_car = '{brand}' AND model_car = '{model}' AND 
                                                        engine_car = '{engine}' AND year={year}'''
    check = check_row(request_check_car)
    if check is not None:
        request_update_car = f'''UPDATE car SET year={year}, brand_car = '{brand}',
                                                            model_car = '{model}', engine_car = '{engine}'
                                                            WHERE brand_car = '{brand}' AND model_car = '{model}' AND 
                                                            engine_car = '{engine}' AND year={year}'''
        answer = sql_massage(request_update_car)
    else:
        request_add_car = f'''INSERT INTO car(year, brand_car, model_car, engine_car, status)
                                                            VALUES({year}, '{brand}', '{model}', '{engine}', {status})'''
        answer = sql_massage(request_add_car)
    return answer


def add_part(part, description, cost):
    request_check_part = f'''SELECT part FROM parts WHERE part = "{part}"'''
    check = check_row(request_check_part)
    if check is None:
        request_add_part = f'''INSERT INTO parts(part, description, cost)
                                VALUES ('{part}', '{description}', {cost})'''
        sql_massage(request_add_part)
    else:
        request_update_part = f'''UPDATE parts SET part = '{part}', description = '{description}',
                                    cost = {cost}
                                    WHERE part = "{part}"'''
        sql_massage(request_update_part)


def add_applicability(id_car, part):
    try:
        request_add_applicability = f'''INSERT INTO applicability
                                values ({id_car}, '{part}')'''
        sql_massage(request_add_applicability)
    except sqlite3.IntegrityError:
        pass


def add_image(part, image):
    request_check_image = f'''SELECT id FROM image WHERE part = "{part}" AND image = "{image}"'''
    check = check_row(request_check_image)
    if check is None:
        request_add_image = f'''INSERT INTO image(part, image)
                                    VALUES ('{part}', '{image}')'''
        sql_massage(request_add_image)
    else:
        request_update_image = f'''UPDATE image SET part = '{part}', image = '{image}'
                                        WHERE part = '{part}' AND image = "{image}"'''
        sql_massage(request_update_image)


def update_status(id_car, status):
    request_update_status = f'''UPDATE car SET status = {status} WHERE id = {id_car}'''
    sql_massage(request_update_status)


def update_all_status():
    request_update_all_status = f'''UPDATE car SET status = 0'''
    sql_massage(request_update_all_status)


def check_start_id():
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    request_check_1st = f'''SELECT * from car WHERE status = 0'''
    cursor.execute(request_check_1st)
    data = cursor.fetchone()
    conn.commit()
    return data

