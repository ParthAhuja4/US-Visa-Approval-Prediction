import sys

from us_visa.exception import USvisaException
from us_visa.logger import logging

import os
import pymongo
import certifi

ca = certifi.where()


class MongoDBClient:
    """
    Class Name :   export_data_into_feature_store
    Description :   This method exports the dataframe from mongodb feature store as dataframe

    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    """

    client = None

    def __init__(self, database_name=os.getenv("DB_NAME")) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("DB_CONNECTION_STRING")
                if mongo_db_url is None:
                    raise Exception("Environment key: DB_CONNECTION_STRING is not set.")
                if database_name is None:
                    raise Exception("Environment key: DB_NAME is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            if database_name is None:
                raise Exception("Environment key: DB_NAME is not set.")

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise USvisaException(e, sys)
