import os
import logging
import json

basedir = os.path.abspath(os.path.dirname(__file__))

DB_USERNAME = ''
DB_PASSWORD = ''
DB_HOSTNAME = ''
DB_PORT = ''
DB_NAME = ''
SQLALCHEMY_DATABASE_URI = ''

def update_env_var():
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
        creds = services['cleardb'][0]['credentials']
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
    SQLALCHEMY_DATABASE_URI = connect_string.format(DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_PORT, DB_NAME)

# update enviroment var form VCAP or directly local environment
update_env_var()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'secret-for-dev-only'
LOGGING_LEVEL = logging.INFO
