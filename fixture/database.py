import psycopg2


class Connector:
    def __init__(self):
        # self.conn = psycopg2.connect(database='pbx', user='postgres', password='', host='10.129.0.9', port="5433")
        self.conn = psycopg2.connect(database='pbx', user='postgres', password='', host='10.129.0.9', port="5436")

    def db_conn(self, s):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(s)
        result = cursor.fetchall()
        #print(result)
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

    def get_detected_speech(self,call_id):
        detected = list(self.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                                   + str(self.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                                   + "'")[0][0].split(" "))
        return detected


