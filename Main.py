"This script will compare current data in VotoSocial against the data backup taken on Monday"

import csv
import os
import pandas
from pymongo import MongoClient
from urllib import quote_plus

mongo_username = os.environ["ACTASDB_USERNAME"]
mongo_password = os.environ["ACTASDB_PASSWORD"]
if os.name == 'nt':
    mongo_password = mongo_password.replace('^','')
mongo_collections = [
    'ActasPresidenciales',
    'ActasPresidenciales2',
    'ActasPresidenciales3',
    'ActasPresidenciales4',
    'ActasPresidenciales5',
    'ActasPresidenciales6']

data_frame = pandas.read_csv("ActasVotoSocial2017HN.csv", header=0)
uri = 'mongodb://%s:%s@ds127456-a0.mlab.com:27456/tse_dump?authMechanism=SCRAM-SHA-1' % (quote_plus(mongo_username), quote_plus(mongo_password))
client = MongoClient(uri)
db = client['tse_dump']

with open('ActasInconsistentes.csv', 'wb') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #Write Headers
    csv_headers = ['ACTA', 'VOTOS_ALIANZA', 'VOTOS_NACIONAL',
                   'VOTOS_ORIGINAL_ALIANZA', 'VOTOS_ORIGINAL_NACIONAL']
    csv_writer.writerow(csv_headers)
    for row in data_frame.itertuples():
        acta_id = row.numero
        for collection in mongo_collections:
            acta = db[collection].find_one({'CodEstado':10, 'CodActa':acta_id})
            if acta is not None:
                originales_nacional = 0
                originales_alianza = 0
                votos_nacional = row.nacional
                votos_alianza = row.libre_pinu
                csv_row = [acta_id, votos_alianza, votos_nacional]
                # Partido 2 = Nacional, Partido 67 = Alianza Lire-Pinu
                for voto in acta['Votos']:
                    if voto['CodPartido'] == 2:
                        originales_nacional = voto['NumVotos']
                    elif voto['CodPartido'] == 67:
                        originales_alianza = voto['NumVotos']
                csv_row += [originales_nacional, originales_alianza]
                if votos_nacional != originales_nacional or votos_alianza != originales_alianza:
                    csv_writer.writerow(csv_row)
