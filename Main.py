"This script will compare current data in TSE API against the data backup taken on Monday"

import csv
import pandas
import requests
import threading
from pymongo import MongoClient
import Settings
from urllib import quote_plus

def obtener_votos(votos):
    "Devuelve una tupla de 2 elementos (votos_alianza, votos_nacional)"
    for voto in votos:
        if voto['CodPartido'] == 2:
            votos_nacional = int(voto['NumVotos'])
        elif voto['CodPartido'] == 67:
            votos_alianza = int(voto['NumVotos'])
    return (votos_alianza, votos_nacional)

def obtener_votos_tse(acta_id):
    "Llama al API del TSE y devuelve la tupla (votos_alianza, votos_nacional)"
    acta_url = Settings.tse_api_url.format(acta_id)
    print "GET: %s" % (acta_url)
    response = requests.get(acta_url)
    if response.status_code == 200:
        votos_alinza, votos_nacional = obtener_votos(response.json()['Votos'])
        return (votos_alinza, votos_nacional)
    else:
        return (-1, -1)

def worker(collection_name):
    """thread worker function"""
    with open('%s.csv' % (collection_name), 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #Write Headers
        csv_headers = ['ACTA', 'NOM_DEPARTAMENTO', 'NOM_MUNICIPIO', 'VOTOS_TSE_ALIANZA',
                    'VOTOS_TSE_NACIONAL', 'VOTOS_BACKUP_ALIANZA', 'VOTOS_BACKUP_NACIONAL']
        csv_writer.writerow(csv_headers)
        actas_estado_divulgacion = db[collection_name].find({'CodEstado':10}).batch_size(100)
        for acta in actas_estado_divulgacion:
            acta_id = int(acta['CodActa'])
            votos_backup_alianza, votos_backup_nacional = obtener_votos(acta['Votos'])
            votos_tse_alianza, votos_tse_nacional = obtener_votos_tse(acta_id)
            if votos_tse_alianza == -1 or votos_tse_nacional == -1:
                continue
            else:
                print "Comparando acta %s." % (acta_id)
                alianza_son_diferentes = votos_backup_alianza != votos_tse_alianza
                nacional_son_diferentes = votos_backup_nacional != votos_tse_nacional
                if alianza_son_diferentes or nacional_son_diferentes:
                    print "Existe incosistencia en votos en acta {0}.".format(acta_id)
                    nom_dep = acta["NomDepartamento"]
                    nom_municipio = acta["NomMunicipio"]
                    csv_row = [acta_id, nom_dep, nom_municipio, votos_tse_alianza, votos_tse_nacional, 
                                votos_backup_alianza, votos_backup_nacional]
                    csv_writer.writerow(csv_row)
    return

mongo_uri = 'mongodb://{0}:{1}@ds127456-a0.mlab.com:27456/tse_dump?authMechanism=SCRAM-SHA-1'
mongo_uri = mongo_uri.format(quote_plus(Settings.mongo_username), quote_plus(Settings.mongo_password))
client = MongoClient(mongo_uri)
db = client[Settings.mongo_dbname]

threads = []
for collection in Settings.mongo_collections:
    t = threading.Thread(target=worker, args=(collection,))
    threads.append(t)
    t.start()
