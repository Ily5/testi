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



#Connector().db_conn(
#                  s="SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '" + "70219b4a-b6cc-11ea-9ead-cb87ec06544a" + "'")
