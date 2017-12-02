import os

mongo_username = os.environ["ACTASDB_USERNAME"]
mongo_password = os.environ["ACTASDB_PASSWORD"]
if os.name == 'nt':
    mongo_password = mongo_password.replace('^','')
mongo_dbname = 'tse_dump'
mongo_collections = [
    'ActasPresidenciales',
    'ActasPresidenciales2',
    'ActasPresidenciales3',
    'ActasPresidenciales4',
    'ActasPresidenciales5',
    'ActasPresidenciales6']
    
tse_api_url = 'https://api.tse.hn/prod/ApiActa/Consultar/1/{0}'