import requests
import json
from common.db_command import add_car, add_part, add_applicability
from common.common import ADDRESS_FOR_YEAR, ADDRESS_MAKE, ADDRESS_MODEL, ADDRESS_ENGINE, ADDRESS_PARTS, ADDRESS_IMAGE

def take_data(address):
    response = requests.get(address)
    rough_data = response.json()
    try:
        data = json.loads(rough_data)
    except TypeError:
        data = rough_data.get('list_partdetails')
    return data


def create_part():
    year_list = take_data(ADDRESS_FOR_YEAR)
    for year_dict in year_list:
        current_year = year_dict.get('AA_Year')
        address_for_get_marks = f'{ADDRESS_MAKE}{current_year}'
        marks_list = take_data(address_for_get_marks)
        for mark_dict in marks_list:
            current_mark = mark_dict.get('AA_Make')
            current_mark_id = int(mark_dict.get('ACESMakeid'))
            address_for_get_models = f'{ADDRESS_MODEL}yearid={current_year}&makeid={current_mark_id}'
            model_list = take_data(address_for_get_models)
            for model_dict in model_list:
                current_model = model_dict.get('AA_Model')
                address_for_get_engine = f'{ADDRESS_ENGINE}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}'
                engine_list = take_data(address_for_get_engine)
                for engine in engine_list:
                    current_engine = bytes(engine.get('Engineconfig'), 'utf-8').decode('unicode_escape')
                    current_engine_number = engine.get('EnginePartno')
                    id_car = add_car(current_year, current_engine, current_mark, current_model)
                    address_for_get_part = f'{ADDRESS_PARTS}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}&enginepartno={current_engine_number}'
                    parts_list = take_data(address_for_get_part)
                    for part in parts_list:
                        part_number = part.get('Partno')
                        part_image = f'{ADDRESS_IMAGE}{part.get("AssetName")}'
                        part_cost = part.get('userPrice')
                        part_description = json.dumps(part)
                        add_part(part_number, part_description, part_cost, part_image)
                        add_applicability(id_car, part_number)




if __name__ == '__main__':
    create_part()
