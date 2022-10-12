def convert_institutes(pg_institutes: list) -> list:
    if not pg_institutes:
        raise ValueError('Данные не могут быть пустыми')

    list_institutes = pg_institutes
    for institute in list_institutes:
        institute[institute['institute_title']] = '{"institute": "' + str(institute['institute_id']) + '"}'
        del institute['institute_title']
        del institute['institute_id']

    return list_institutes


def convert_courses(pg_courses: list) -> list:
    if not pg_courses:
        raise ValueError('Данные не могут быть пустыми')

    list_courses = [{course: '{"course": "' + str(course) + '"}'} for course in pg_courses]

    return list_courses


def convert_groups(pg_groups: list) -> list:
    if not pg_groups:
        raise ValueError('Данные не могут быть пустыми')

    list_groups = pg_groups
    for group in list_groups:
        group[group['name']] = '{"group": "' + str(group['group_id']) + '"}'
        del group['name']
        del group['group_id']

    return list_groups