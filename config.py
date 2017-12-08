import os
import logging
import json

basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_info():
    """
    Initialized MySQL database connection
    This method will work in the following conditions:
      1) In Bluemix with Redis bound through VCAP_SERVICES
      2) With MySQL running on the local server as with Travis CI
      3) With MySQL --link in a Docker container called 'mysql'
    """
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        logging.info("Using VCAP_SERVICES...")
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        
        # cleardb
        # creds = services['cleardb'][0]['credentials']
        # username = creds["username"]
        # password = creds["password"]
        # hostname = creds["hostname"]
        # port = creds["port"]
        # name = creds["name"]

        # PostSQL
        full_uri = services['elephantsql'][0]['credentials']
        uri = full_uri.split('/')[-2]
        name = full_uri.split('/')[-1]
        hostname = uri.split('@')[1].split(':')[0]
        port = uri.split('@')[1].split(':')[1]
        username = uri.split('@')[0].split(':')[0]
        password = uri.split('@')[0].split(':')[1]

    else:
        logging.info("Using localhost database...")

        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD', '')
        hostname = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        name = os.getenv('DB_DBNAME')

    logging.info("Conecting to database on host %s port %s", hostname, port)
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
    uri = connect_string.format(username, password, hostname, port, name)
    
    return username, password, hostname, port, name, uri

DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_PORT, DB_NAME, SQLALCHEMY_TRACK_MODIFICATIONS = get_db_info()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'secret-for-dev-only'
LOGGING_LEVEL = logging.INFO
