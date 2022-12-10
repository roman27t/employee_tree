

def front_staff_tree(data: dict) -> dict:
    data.update({'_levels': {}, '_staff_path': {}})
    for pk, staff in data['staff'].items():
        data['_staff_path'][staff['path']] = staff
        data['_levels'].setdefault(staff['_level'], []).append(str(staff['path']))
    return data
