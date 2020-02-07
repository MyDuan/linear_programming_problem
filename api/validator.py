from cerberus import Validator


def data_validate(req):
    data_dict = req.to_dict()
    if len(data_dict.keys()) == 1:
        return False
    b_num = len({k for k, v in data_dict.items() if 'max' in k})
    x_num = len({k for k, v in data_dict.items() if 'x_name_' in k})
    data = {}
    check_keys = {}
    for i in range(0, x_num):
        key = chr(ord('a') + i) + '_cost'
        check_keys.update({key: {'required': True}})
        if req[key]:
            data[key] = req[key]
    for i in range(0, b_num):
        key = 'max_' + str(i + 1)
        check_keys.update({key: {'required': True}})
        if req[key]:
            data[key] = req[key]
    v = Validator(check_keys)
    return v.validate(data)
