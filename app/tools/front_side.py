from decorators.front_side_decorators import front_validation


@front_validation
def front_staff_tree(data: dict) -> dict:
    data.update({'_levels': {}, '_staff_path': {}})
    for pk, staff in data['staff'].items():
        data['_staff_path'][staff['path']] = staff
        data['_levels'].setdefault(staff['_level'], []).append(str(staff['path']))
    return data


@front_validation
def front_staff_by_id(data: dict) -> dict:
    pk = list(data['staff'].keys())[0]
    data['_staff'] = data['staff'][pk]
    return data
