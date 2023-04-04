import collections
import pymongo
import certifi
import urllib.parse
from .dbconfig import *
from config.logger import *

ca = certifi.where()

logger = logging.getLogger('dbconfig')
setup_logger(logger,'logs/nosql_dbconfig.logs')

class Cnxn():

    def mongodb_conn():
        A=Read_Config()
        db_config = A.read_config('mongodb')
        username = urllib.parse.quote_plus(db_config['id'])
        pwd = urllib.parse.quote_plus(db_config['pwd'])

        try:
            cloud_client = pymongo.MongoClient("mongodb+srv://"+username+":"+pwd+"@cluster0.fbdmddg.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
            # tls=True,tlsAllowInvalidCertificates=True
            db = cloud_client.test
            collection=db[db_config['database']]
            logger.info("Connection established for mongo database")
            return cloud_client,db,collection
        except Exception as e:
            logger.error(f"Error while connecting the mongo database.{e}")
            return "Error while connecting the mongo database"