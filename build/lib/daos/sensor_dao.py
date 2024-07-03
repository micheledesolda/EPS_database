# src/daos/sensor_dao.py
import pymongo
from typing import List, Dict, Optional, Union, Tuple, Any
import os
import sys
import csv
import json
import gridfs
from nptdms import TdmsFile
import matplotlib.pyplot as plt
from daos.base_dao import BaseDao

# MongoDB connection details
url = os.getenv("MONGO_URL") or "mongodb://localhost:27017/"
db_name = os.getenv("DB_NAME") or "EPS"
sensors_collection_name = os.getenv("COLLECTION_SENSORS") or "Sensors"

class SensorDao(BaseDao):
    
    def __init__(self):
        """Initialize the SensorDao class with a connection to the MongoDB database."""
        super().__init__()
        self.collection_name = sensors_collection_name
        
    def create(self, sensor_id: str, sensor_type: str, model: str, resonance_frequency: float, properties: Dict[str,Any]) -> None:
        """Create a new sensor in the database."""
        conn, collection = self._get_connection(self.collection_name)

        sensor = {
                 "_id": sensor_id, 
                 "sensor_type": sensor_type,
                 "model": model, 
                 "resonance_frequency": resonance_frequency, 
                 "properties": properties
        }
        try:
            collection.insert_one(sensor)
            print(f"Sensor {sensor_id} added to database.")
        except Exception as err:
            print(f"Error: '{err}'")
        finally:
            conn.close()
            
    def initialize_inventory(self) -> None:
        """Initialize the sensor inventory in the database."""
        conn, collection = self._get_connection(self.collection_name)

        try:
            for sensor in self.available_sensors:
                collection.update_one({"_id": sensor["_id"]}, {"$set": sensor}, upsert=True)
            print("Sensor inventory initialized.")
        except Exception as err:
            print(f"Error: '{err}'")
        finally:
            conn.close()

    def find_sensor_by_id(self, _id: str) -> Optional[Dict]:
        """Retrieve sensor details by sensor ID."""
        conn, collection = self._get_connection(self.collection_name)

        try:
            sensor = collection.find_one({"_id": _id})
            return sensor
        except Exception as err:
            print(f"Error: '{err}'")
            return None
        finally:
            conn.close()
