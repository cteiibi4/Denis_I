import requests
import json
import time
from common.create_db import Part, Car
from common.db_command import add_car, add_part, check_object, update_all_status, check_start_id, \
    add_image, start_session, check_date, add_kit, add_parts_in_kit
from common.common import ADDRESS_FOR_YEAR, ADDRESS_MAKE, ADDRESS_MODEL, ADDRESS_ENGINE, ADDRESS_PARTS, ADDRESS_IMAGE, \
    ADDRESS_PART, ADDRESS_FOR_KIT


def take_parts_for_kit(kit, kit_type):
    if kit_type == 'pr_master' or kit_type == 'master':
        description = 'DMK'
    elif kit_type == 'pr_recon' or kit_type == 'recon':
        description = 'DRK'
    else:
        description = 'DREK'
    address_for_request = f'{ADDRESS_FOR_KIT}{kit}&partdescription={description}'
    all_description = take_data_get(address_for_request)
    table_2 = all_description.get('Table2')
    kit_part_list = [i.get('Partno') for i in table_2]
    return kit_part_list


def take_data_get(address):
    attempt = 1
    while attempt <= 20:
        try:
            response = requests.get(address)
            rough_data = response.json()
            try:
                data = json.loads(rough_data)
            except TypeError:
                data = rough_data
            # except TypeError:
            #     data = rough_data.get('list_partdetails')
            # except:
            #     data = rough_data.get('list_kitpartdetails')
            return data
        except:
            print(f'Ошибка соеденения с адресом {address} попытка №{attempt}')
            time.sleep(1)
            attempt += 1
    print(f'Нет доступа к адресу {address}')
    exit(1)


def take_data_post(address, dictionary):
    attempt = 1
    while attempt <= 20:
        try:
            response = requests.post(
                address,
                data=dictionary)
            rough_part_data = response.content
            return json.loads(rough_part_data)
        except:
            print(f'Ошибка соеденения с адресом {address} попытка №{attempt}')
            time.sleep(1)
            attempt += 1
    print(f'Нет доступа к адресу {address}')
    exit(1)


def create_dict(arg, str_parce):
    result = {}
    data = json.loads(arg.get(str_parce))
    if len(data) > 0:
        for i in data:
            result.update(i)
    return result


def create_part():
    session = start_session()
    data = check_start_id(session)
    year_list = take_data_get(ADDRESS_FOR_YEAR)
    for year_dict in year_list:
        current_year = year_dict.get('AA_Year')
        # if current_year == 1980:
        if data is None or data[1] == current_year:
            address_for_get_marks = f'{ADDRESS_MAKE}{current_year}'
            marks_list = take_data_get(address_for_get_marks)
            for mark_dict in marks_list:
                current_mark = mark_dict.get('AA_Make')
                if data is None or data[3] == current_mark:
                    current_mark_id = int(mark_dict.get('ACESMakeid'))
                    address_for_get_models = f'{ADDRESS_MODEL}yearid={current_year}&makeid={current_mark_id}'
                    model_list = take_data_get(address_for_get_models)
                    for model_dict in model_list:
                        current_model = model_dict.get('AA_Model')
                        if data is None or data[4] == current_model:
                            address_for_get_engine = f'{ADDRESS_ENGINE}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}'
                            engine_list = take_data_get(address_for_get_engine)
                            for engine in engine_list:
                                current_engine = bytes(engine.get('Engineconfig'), 'utf-8').decode('unicode_escape')
                                current_engine_number = engine.get('EnginePartno')
                                if data is None or data[2] == current_engine:
                                    address_for_get_part = f'{ADDRESS_PARTS}yearid={current_year}&makeid={current_mark_id}&modelname={current_model}&enginepartno={current_engine_number}'
                                    parts_list_rough = take_data_get(address_for_get_part)
                                    parts_list = parts_list_rough.get('list_partdetails')
                                    kit_list = parts_list_rough.get('list_kitpartdetails')
                                    new_car = add_car(session, current_year, current_engine, current_mark,
                                                      current_model, 1)
                                    print(f'Сканируем машину {current_mark}:{current_model} {current_year} '
                                          f'года, с двигателем : {current_engine}')
                                    for part in parts_list:
                                        # take_part_data(session, part, new_car)
                                        part_number = part.get('Partno')
                                        check_part = check_object(session, Part, part=part_number)
                                        if check_part is None or check_date(check_part.update_date) > 30 or check_part.description == 'No description':
                                            part_cost = part.get('userPrice')
                                            part_data = take_data_post(
                                                ADDRESS_PART,
                                                {'partno': part_number, 'partdescription': part.get('partdescription')})
                                            part_description = {'part': part, 'data': part_data}
                                            description = json.dumps(part_description)
                                            answer_part = add_part(session, new_car, part_number, description,
                                                                   part_cost)
                                            if answer_part[1] is True:
                                                images = json.loads(part_data.get('str_Imageresult'))
                                                for image in images:
                                                    address_image = f'{ADDRESS_IMAGE}{image.get("AssetName")}'
                                                    add_image(session, answer_part[0], address_image)
                                        else:
                                            add_part(session, new_car, part_number, 'No description', 0)
                                    for car_kit in kit_list:
                                        kits_for_car = car_kit
                                        dict_kit = {'pr_master': kits_for_car.get('pr_master'),
                                                    'pr_recon': kits_for_car.get('pr_recon'),
                                                    'pr_remain': kits_for_car.get('pr_remain'),
                                                    'master': kits_for_car.get('master'),
                                                    'recon': kits_for_car.get('recon'),
                                                    'remain': kits_for_car.get('remain'),
                                                    }
                                        dict_kit_img = {'pr_master': kits_for_car.get('pr_master_img'),
                                                        'pr_recon': kits_for_car.get('pr_recon_img'),
                                                        'pr_remain': kits_for_car.get('pr_remain_img'),
                                                        'master': kits_for_car.get('master_img'),
                                                        'recon': kits_for_car.get('recon_img'),
                                                        'remain': kits_for_car.get('remain_img'),
                                                        }
                                        for key in dict_kit:
                                            value = dict_kit[key]
                                            if value is not None and len(value) > 1:
                                                new_kit = add_kit(session, value, dict_kit_img.get(key), key, new_car)
                                                if new_kit[1] is True:
                                                    print(f'Сканируем набор {value}')
                                                    part_list_for_kit = take_parts_for_kit(value, key)
                                                    add_parts_in_kit(session, part_list_for_kit, new_kit[0], new_car)
                                    session.commit()
                                    data = None
    update_all_status(session)


if __name__ == '__main__':
    create_part()
