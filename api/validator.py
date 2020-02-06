from cerberus import Validator


def data_validate(req):
    data_dict = req.to_dict()
    nutrition_num = len({k for k, v in data_dict.items() if 'max' in k})
    material_num = len({k for k, v in data_dict.items() if 'x_name_' in k})
    data = {}
    check_keys = {}
    for i in range(0, material_num):
        key = chr(ord('a') + i) + '_cost'
        check_keys.update({key: {'required': True}})
        if req[key]:
            data[key] = req[key]
    for i in range(0, nutrition_num):
        key = 'max_' + str(i + 1)
        check_keys.update({key: {'required': True}})
        if req[key]:
            data[key] = req[key]
    v = Validator(check_keys)
    return v.validate(data)
