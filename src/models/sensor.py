# src/models/sensor.py
import os
from mongoengine import Document, StringField, FloatField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentField

sensor_collection_name = os.getenv("COLLECTION_SENSORS") or "Sensors"

class Sensor(EmbeddedDocument):
    sensor_name = StringField(required=True)
    position = DictField(required=True)
    orientation = StringField(required=True)
    calibration = StringField(required=True)
    sensor_properties = DictField(required=True)

    meta = {'collection': sensor_collection_name}