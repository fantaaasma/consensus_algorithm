import pypyodbc

database_path = 'C:\\Users\\Monika\\Desktop\\baza.mdb'
connection = pypyodbc.win_connect_mdb(database_path)
cursor = connection.cursor()

caseS_TABLE_NAME = 'Pacjent'
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

# def get_complications_dict():
#     cursor.execute('SELECT * FROM {};'.format(COMPLICATIONS_DICT_TABLE_NAME))
#     complications_dict = {}
#     for t in cursor.fetchall():
#         complications_dict[t[0]] = t[1]
#
#     return complications_dict
#
# def get_complications_dict():
#     cursor.execute('SELECT * FROM {};'.format(COMPLICATIONS_DICT_TABLE_NAME))
#     complications_dict = {}
#     for t in cursor.fetchall():
#         complications_dict[t[0]] = t[1]
#
#     return complications_dict

def create_case_dicts(data_tuple):
    case_dicts = []
    case_dict = dict()
    id = data_tuple[0]
    disease_number = data_tuple[1]
    year = data_tuple[2]

    case_dict[ID] = data_tuple[0]
    case_dict[DISEASE_NUMBER] = data_tuple[1]
    case_dict[YEAR] = data_tuple[2]

    case_dict[AGE]  = 1 if data_tuple[3] > 45 else 0
    case_dict[SEX] = data_tuple[4] - 1
    complications = get_case_data_from_table(COMPLICATIONS_TABLE_NAME, case_dict)
    additional_diseases = get_case_data_from_table(ADDITIONAL_DISEASES_TABLE_NAME, case_dict)
    operation_types = get_case_data_from_table(CATALOGUE_DATA_TABLE_NAME, case_dict, 13, 'Karta_')
    for c in complications:
        for ad in additional_diseases:
            for ot in operation_types:
                case_dicts.append(enrich_case_dict(case_dict, age, sex, c, ad, ot))

    #case_dicts.append(case_dict)

    return case_dicts




def enrich_case_dict(case_dict,
                            age,
                            sex,
                            complication,
                            additional_disease,
                            operation_type):
    # case_dict = dict()
    # case_dict[ID] = id
    # case_dict[DISEASE_NUMBER] = disease_number
    # case_dict[YEAR] = year
    case_dict[AGE] = age
    case_dict[SEX] = sex
    case_dict[COMPLICATION] = complication
    case_dict[ADDITIONAL_DISEASES] = additional_disease
    case_dict[OPERATION_TYPE] = operation_type
    return case_dict


def get_case_data_from_table(table_name, case_dict, items_to_get=2, prefix_name=''):
    data = []
    cursor.execute('''select * from {} where {}={} and {}={} ;'''
                   .format(table_name,
                           prefix_name + DISEASE_NUMBER, case_dict[DISEASE_NUMBER],
                           prefix_name + YEAR, case_dict[YEAR]))

    fa = cursor.fetchall()
    # #print(fa)
    # if not fa:
    #     raise Exception(fa)
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
    cursor.execute('select * from {};'.format(caseS_TABLE_NAME))
    cases_data = cursor.fetchall()
    cases = []
    n = len(cases_data)
    i = 0
    d = int(n/100)
    for pd in cases_data:
        i += 1
        if (i % d) == 0:
            print('{}%'.format(int(i*100/n)))
        for case in create_case_dicts(pd):
            cases.append(case)

    return cases

def print_stats(cases, type_name):
    d = {}
    for c in cases:
        type = c[type_name]
        d[type] = d.get(type, 0) + 1
    print('czestosc wystepowaia ', type_name)
    for x, y in d.items():
        print(x, y)

cases = get_cases()
print_stats(cases, OPERATION_TYPE)
print_stats(cases, ADDITIONAL_DISEASES)
print_stats(cases, COMPLICATION)

def get_views(cases, filter_additional_diseases, filter_operation_type):
    outs = []

    for c in cases:
        out = []
        out.append(c[SEX])
        out.append(c[AGE])
        for ad in filter_additional_diseases:
            out.append(int(ad == c[ADDITIONAL_DISEASES]))
        for ot in filter_operation_type:
            out.append(int(ot == c[OPERATION_TYPE]))
        out.append(c[COMPLICATION])
        outs.append(out)
    return outs


for p in cases[100:120]:
    print(p)

views = get_views(cases,
                  filter_additional_diseases=[3, 4, 7],
                  filter_operation_type=[1, 3]
                  )


for v in views[100:120]:
    print(v)

connection.close()