import requests
import json
from create_db import init_db
from common.db_command import add_car, add_part, add_applicability, update_status, update_all_status, check_start_id,\
    add_image
from common.common import ADDRESS_FOR_YEAR, ADDRESS_MAKE, ADDRESS_MODEL, ADDRESS_ENGINE, ADDRESS_PARTS, ADDRESS_IMAGE,\
    ADDRESS_PART


def take_data(address):
    response = requests.get(address)
    rough_data = response.json()
    try:
        data = json.loads(rough_data)
    except TypeError:
        data = rough_data.get('list_partdetails')
    return data


def create_dict(arg, str_parce):
    if len(arg.get(str_parce)[1:-1]) > 0:
        first_data = json.loads(arg.get(str_parce)[1:-1])
    else:
        result = {}
    return result


def create_part():
    data = check_start_id()
    year_list = take_data(ADDRESS_FOR_YEAR)
    for year_dict in year_list:
        current_year = year_dict.get('AA_Year')
        if data is None or data[1] == current_year:
            address_for_get_marks = f'{ADDRESS_MAKE}{current_year}'
            marks_list = take_data(address_for_get_marks)
            for mark_dict in marks_list:
                current_mark = mark_dict.get('AA_Make')
                if data is None or data[3] == current_mark:
                    current_mark_id = int(mark_dict.get('ACESMakeid'))
                    address_for_get_models = f'{ADDRESS_MODEL}yearid={current_year}&makeid={current_mark_id}'
                    model_list = take_data(address_for_get_models)
                    for model_dict in model_list:
                        current_model = model_dict.get('AA_Model')
                        if data is None or data[4] == current_model:
                            address_for_get_engine = f'{ADDRESS_ENGINE}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}'
                            engine_list = take_data(address_for_get_engine)
                            for engine in engine_list:
                                current_engine = bytes(engine.get('Engineconfig'), 'utf-8').decode('unicode_escape')
                                current_engine_number = engine.get('EnginePartno')
                                if data is None or data[2] == current_engine:
                                    address_for_get_part = f'{ADDRESS_PARTS}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}&enginepartno={current_engine_number}'
                                    parts_list = take_data(address_for_get_part)
                                    id_car = add_car(current_year, current_engine, current_mark, current_model, 0)
                                    print(f'СКанируем машину {current_mark}:{current_model} {current_year} '
                                          f'года, с двигателем : {current_engine}')
                                    for part in parts_list:
                                        part_number = part.get('Partno')
                                        part_cost = part.get('userPrice')
                                        part_description = part
                                        response = requests.post(
                                            ADDRESS_PART,
                                            data={'partno': part_number, 'partdescription': 'Valve - Intake'})
                                        rough_part_data = response.content
                                        part_data = json.loads(rough_part_data)
                                        part_attrresult = create_dict(part_data, 'str_attrresult')
                                        part_partresult = create_dict(part_data, 'str_Partresult')
                                        part_description.update(part_attrresult)
                                        part_description.update(part_partresult)
                                        part_description = json.dumps(part)
                                        add_part(part_number, part_description, part_cost)
                                        add_applicability(id_car, part_number)
                                        images = json.loads(part_data.get('str_Imageresult'))
                                        for image in images:
                                            address_image = f'{ADDRESS_IMAGE}{image.get("AssetName")}'
                                            add_image(part_number, address_image)
                                    update_status(id_car, 1)
                                    data = None
    update_all_status()


if __name__ == '__main__':
    init_db()
    create_part()
