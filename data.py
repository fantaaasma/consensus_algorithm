import pypyodbc

database_path = 'C:\\Users\\Monika\\Desktop\\baza.mdb'
connection = pypyodbc.win_connect_mdb(database_path)
cursor = connection.cursor()

PATIENT_TABLE_NAME = 'Pacjent'
COMPLICATIONS_TABLE_NAME = 'PowiklaniaPooperacyjne'
ADDITIONAL_DISEASES_TABLE_NAME = 'ChorobyWspolistniejace'
COMPLICATIONS_DICT_TABLE_NAME = 'Slownik_PowiklaniaPooperacyjne'
ADDITIONAL_DISEASES_DICT_TABLE_NAME = ''
CATALOGUE_DATA_TABLE_NAME = 'Karta'
OPERATION_TYPE = 'IdRodzajZabiegu'

ID = 'id'
DISEASE_NUMBER = 'nrHistChoroby'
YEAR = 'Rok'
AGE = 'wiek'
SEX = 'płeć'
ADDITIONAL_DISEASES = 'ChorobyWspolistniejace'

COMPLICATION = 'powiklanie'


def get_complications_dict():
    cursor.execute('SELECT * FROM {};'.format(COMPLICATIONS_DICT_TABLE_NAME))
    complications_dict = {}
    for t in cursor.fetchall():
        complications_dict[t[0]] = t[1]

    return complications_dict


def create_case_dicts(data_tuple):
    case_dict = dict()
    case_dict[ID] = data_tuple[0]
    case_dict[DISEASE_NUMBER] = data_tuple[1]
    case_dict[YEAR] = data_tuple[2]
    case_dict[AGE] = 1 if data_tuple[3] > 45 else 0
    case_dict[SEX] = data_tuple[4] - 1
    case_dict[COMPLICATION] = get_case_data_from_table(COMPLICATIONS_TABLE_NAME, case_dict)
    case_dict[ADDITIONAL_DISEASES] = get_case_data_from_table(ADDITIONAL_DISEASES_TABLE_NAME, case_dict)
    case_dict[OPERATION_TYPE] = get_case_data_from_table(CATALOGUE_DATA_TABLE_NAME, case_dict, 13, 'Karta_')

    return case_dict


def get_case_data_from_table(table_name, case_dict, items_to_get=2, prefix_name=''):
    data = []
    cursor.execute('''select * from {} where {}={} and {}={} ;'''
                   .format(table_name,
                           prefix_name + DISEASE_NUMBER, case_dict[DISEASE_NUMBER],
                           prefix_name + YEAR, case_dict[YEAR]))

    fa = cursor.fetchall()
    for c in fa:
        if isinstance(items_to_get, list):
            for index in items_to_get:
                data.append(c[index])
        else:
            data.append(c[items_to_get])

    if not data:
        return [0]
    return data


def get_cases():
    connection = pypyodbc.win_connect_mdb(database_path)
    cursor = connection.cursor()
    cursor.execute('select * from {};'.format(PATIENT_TABLE_NAME))
    cases_data = cursor.fetchall()
    cases = []
    n = len(cases_data)
    i = 0
    d = int(n / 100)
    print('wczytywanie danych z bazy')

    for pd in cases_data:
        i += 1
        if (i % d) == 0:
            print('{}%'.format(int(i * 100 / n)))
        cases.append(create_case_dicts(pd))
    print('zakonczono wczytywanie danych z bazy')
    connection.close()
    return cases


def print_stats(cases, type_name):
    d = {}
    for c in cases:
        types = c[type_name]
        for t in types:
            d[t] = d.get(t, 0) + 1
    print('czestosc wystepowaia ', type_name)
    for x, y in d.items():
        print(x, y)


def get_views(cases, filter_additional_diseases, filter_operation_type, filter_complications):
    outs = []

    for c in cases:
        out = []
        out.append(c[SEX])
        out.append(c[AGE])
        for ad in filter_additional_diseases:
            out.append(int(ad in c[ADDITIONAL_DISEASES]))
        for ot in filter_operation_type:
            out.append(int(ot in c[OPERATION_TYPE]))
        for comp in filter_complications:
            out.append(int(comp in c[COMPLICATION]))
        outs.append(out)
    return outs


def get_symptom_vectors_for_given_complication(complication_number, number_of_complications, views):
    number_of_symptoms = len(views[0]) - number_of_complications
    symptom_vectors_with_complication = []
    for v in views:
        if v[number_of_symptoms + complication_number]:
            symptom_vectors_with_complication.append(v[:number_of_symptoms])

    return symptom_vectors_with_complication
