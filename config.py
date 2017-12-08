import os
import logging
import json

basedir = os.path.abspath(os.path.dirname(__file__))

def get_sql_uri():
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
        creds = services['elephantsql'][0]['credentials']
        #uri = creds["uri"]
        DB_USERNAME = creds["username"]
        DB_PASSWORD = creds["password"]
        DB_HOSTNAME = creds["hostname"]
        DB_PORT = creds["port"]
        DB_NAME = creds["name"]
    else:
        logging.info("Using localhost database...")

        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_HOSTNAME = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')
        DB_NAME = os.getenv('DB_DBNAME')

    logging.info("Conecting to database on host %s port %s", DB_HOSTNAME, DB_PORT)
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
    return connect_string.format(DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_PORT, DB_NAME)

def get_db_info():
    if 'VCAP_SERVICES' in os.environ:
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['elephantsql'][0]['credentials']
        #uri = creds["uri"]
        username = creds["username"]
        password = creds["password"]
        hostname = creds["hostname"]
        port = creds["port"]
        name = creds["name"]
    else:
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD', '')
        hostname = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        name = os.getenv('DB_DBNAME')

    return username, password, hostname, port, name


DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_PORT, DB_NAME = get_db_info()
SQLALCHEMY_DATABASE_URI = get_sql_uri()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'secret-for-dev-only'
LOGGING_LEVEL = logging.INFO
