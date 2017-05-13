import pypyodbc

database_path = 'C:\\Users\\Monika\\Desktop\\baza.mdb'
connection = pypyodbc.win_connect_mdb(database_path)
cursor = connection.cursor()

PATIENTS_TABLE_NAME = 'Pacjent'
COMPLICATIONS_TABLE_NAME = 'PowiklaniaPooperacyjne'
COMPLICATIONS_DICT_TABLE_NAME = 'Slownik_PowiklaniaPooperacyjne'

ID = 'id'
DISEASE_NUMBER = 'nrHistChoroby'
YEAR = 'Rok'
AGE = 'wiek'
SEX = 'płeć'
COMPLICATIONS = 'powiklania'

def get_complications_dict():
    cursor.execute('SELECT * FROM {};'.format(COMPLICATIONS_DICT_TABLE_NAME))
    complications_dict = {}
    for t in cursor.fetchall():
        complications_dict[t[0]] = t[1]

    return complications_dict

def create_patient_dict(data_tuple):
    d = dict()
    d[ID] = data_tuple[0]
    d[DISEASE_NUMBER] = data_tuple[1]
    d[YEAR] = data_tuple[2]
    d[AGE] = data_tuple[3]
    d[SEX] = data_tuple[4]
    d[COMPLICATIONS] = get_complication(d[DISEASE_NUMBER], d[YEAR])
    return d

def get_complications(disease_history_number, year):
    complications = []

    cursor.execute('''select * from {} where {}={} and {}={} ;'''
                   .format(COMPLICATIONS_TABLE_NAME,
                           DISEASE_NUMBER, disease_history_number,
                           YEAR, year))

    for c in cursor.fetchall():
        complications.append(c[2])
    return complications

def get_complication(disease_history_number, year):
    cursor.execute('''select * from {} where {}={} and {}={} ;'''
                   .format(COMPLICATIONS_TABLE_NAME,
                           DISEASE_NUMBER, disease_history_number,
                           YEAR, year))

    for c in cursor.fetchall():
        return c[2]

def get_patients():
    cursor.execute('select * from {};'.format(PATIENTS_TABLE_NAME))
    patients_data = cursor.fetchall()
    patients = []
    n = len(patients_data)
    i = 0
    d = int(n/100)
    for pd in patients_data:
        i += 1
        if (i % d) == 0:
            print('{}%'.format(int(i*100/n)))
        patients.append(create_patient_dict(pd))

    return patients

complications_dict = get_complications_dict()
patients = get_patients()

print(complications_dict)
for p in patients:
    print(p)

connection.close()