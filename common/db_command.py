from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from .create_db import Car, Part, Image, Kit, engine_db
from datetime import datetime


def start_session():
    Session = sessionmaker(bind=engine_db)
    session = Session()
    return session


def add_object(session, object_request):
    new_object = object_request
    session.add(new_object)


def check_all_objects(session, model, **kwargs):
    # new_kwargs = {}
    # for key, value in kwargs.items():
    #     new_key = func.lower(key)
    #     new_value = value.lower()
    #     new_kwargs.update({new_key: new_value})
    # db.session.query(models.Product).filter(func.lower(models.Product.name) == u'курага').all()
    instance = session.query(model).filter_by(map(lambda **kwargs: func.lower(kwargs.items()[0]) == kwargs.get(kwargs.items()[0].lower()), **kwargs)).all()
    if instance:
        return instance
    else:
        return None


def check_object(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        return None


def check_date(last_date):
    date_now = datetime.date(datetime.today())
    # date_update = datetime.date(datetime.strptime(last_date, '%Y-%m-%d'))
    return abs(date_now - last_date).days


def add_car(session, year, engine_car, brand, model, status):
    check = check_object(session, Car, year=year, engine_car=engine_car, brand_car=brand, model_car=model)
    new_car = Car(year, engine_car, brand, model, status)
    if check is None:
        add_object(session, new_car)
        return new_car
    else:
        return check


def add_part(session, Car, part, description, cost):
    date_now = datetime.date(datetime.today())
    check = check_object(session, Part, part=part)
    if check is None:
        new_part = Part(part, description, cost, date_now)
        new_part.cars.append(Car)
        add_object(session, new_part)
        return new_part, True
    else:
        update_date = check.update_date
        if check_date(update_date) > 30:
            check.update({Part.description: description, Part.cost: cost, Part.update_date: date_now},
                         synchronize_session=False)
            check.cars.append(Car)
            return check, True
        else:
            check.cars.append(Car)
            return check, False


def add_image(session, Part, image):
    new_image = Image(image)
    # new_image.part.append(Part)
    Part.images.append(new_image)
    add_object(session, new_image)


def update_status(car, status):
    car.status = status


def update_all_status(session):
    for instance in session.query(Car):
        instance.status = 0
    session.commit()


def add_kit(session, kit, Car):
    check = check_object(session, Kit, kit=kit)


def check_start_id(session):
    instance = session.query(Car).filter_by(status=0).first()
    if instance:
        data = [instance.id, instance.year, instance.engine_car, instance.brand_car, instance.model_car]
    elif len(session.query(Car).all()) > 1:
        instance = session.query(Car).all()
        a = instance[-1]
        data = [a.id, a.year, a.engine_car, a.brand_car, a.model_car]
    else:
        data = None
    return data
