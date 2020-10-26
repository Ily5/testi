import psycopg2
from pymongo import MongoClient
import time
import re


class Connector:
    def __init__(self, data):
        self.conn = psycopg2.connect(database=data["database"], user=data["user"],
                                     password=data["password"], host=data["host"], port=data["port"])
        # self.conn = psycopg2.connect(database='pbx', user='postgres', password='', host='10.129.0.9', port="5436")

    def create_connect(self, data):
        self.conn = psycopg2.connect(database=data["database"], user=data["user"],
                                     password=data["password"], host=data["host"], port=data["port"])
        # print("connected to {db} at port {host}".format(db=data["database"], host=data["host"]))

    def db_conn(self, s):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(s)
        if 'UPDATE' not in s:
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            self.conn.commit()
            cursor.close()
        # print(result)

    def cancel(self):
        self.conn.close()

    def check_call_status(self, call_id):
        timeout = time.time() + 600
        while True:
            conn = self.db_conn("SELECT result FROM calls WHERE main_id = %s" % call_id)
            if conn[0][0] == "+OK":
                break
            elif time.time() > timeout:
                raise TimeoutError
            else:
                continue

    def get_detected_speech(self, call_id):
        detected = list(self.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                                     + str(
            self.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                                     + "'")[0][0].split(" "))
        return detected

    def get_detected_speech_from_call_id(self, call_id):
        detected = list(
            self.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and call_id = '"
                         + str(self.db_conn("SELECT id FROM calls WHERE main_id = %s" %
                                            str(call_id))[0][0]) + "'")[0][0].split(" "))
        return detected

    def get_project_data(self, project_id):
        return list(self.db_conn("SELECT * from projects where id = %s" % str(project_id)))

    def change_project_data(self, column, data, project_id):
        # print(self.conn)
        return self.db_conn(
            "UPDATE projects SET {column}={data} where id = {id}".format(column=column, data=data, id=project_id))

    def change_pool_id(self, data, project_id):
        # print("change_pool_id connection %s" % self.conn)
        return self.db_conn(
            "UPDATE projects SET pool_id = 2 where id = 214")

    def select_data(self, table, column, sdata, data):
        return self.db_conn(
            "select {sdata} from {table} where {column} = '{data}'".format(table=table, sdata=sdata, column=column,
                                                                           data=data))
        # return self.db_conn("select pool_id from projects where id = 214")

# select id from server_pools where name = main_pool


class MongoConnector:
    def __init__(self, data):
        self.cluster = MongoClient(data)
        self.db = self.cluster["pbx"]
        self.collection = self.db["statistic"]

    def check_value(self, dict, row, value):
        result = None
        while result is None:
            result = self.request(dict)
            time.sleep(1)
        while result[row] != value:
            result = self.request(dict)
            time.sleep(1)
        return result

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
