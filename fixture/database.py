import psycopg2
from pymongo import MongoClient
import re


class Connector:
    def __init__(self, data):
        self.conn = psycopg2.connect(database=data["database"], user=data["user"],
                                     password=data["password"], host=data["host"], port=data["port"])
        # self.conn = psycopg2.connect(database='pbx', user='postgres', password='', host='10.129.0.9', port="5436")

    def create_connect(self, data):
        self.conn = psycopg2.connect(database=data["database"], user=data["user"],
                                     password=data["password"], host=data["host"], port=data["port"])

    def db_conn(self, s):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(s)
        result = cursor.fetchall()
        # print(result)
        cursor.close()
        return result

    def cancel(self):
        self.conn.close()

    def check_call_status(self, call_id):
        while True:
            conn = self.db_conn("SELECT result FROM calls WHERE main_id = %s" % str(call_id))
            if conn[0][0] == "+OK":
                break
            else:
                continue

    def get_detected_speech(self, call_id):
        detected = list(self.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                                     + str(
            self.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                                     + "'")[0][0].split(" "))
        return detected

    def get_project_data(self, project_id):
        return list(self.db_conn("SELECT * from projects where id = %s" % str(project_id)))


class MongoConnector:
    def __init__(self):
        self.cluster = MongoClient('mongodb://10.129.0.9:27017/')
        self.db = self.cluster["pbx"]
        self.collection = self.db["statistic"]

    def request(self, dict):
        # results = self.collection.find(dict)
        # global r
        results = self.collection.find(dict)
        r = None
        for result in results:
            r = result
        return r

    def parse(self, result, array, key, value):
        if array is not None:
            result = result[str(array)]
        else:
            result = result
        for select in result:
            if key in select.values():
                return select[value]

    def cancel(self):
        self.cluster.close()
