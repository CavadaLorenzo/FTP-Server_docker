from influxdb import InfluxDBClient
import os

try: DB_IP = os.environ['DB_IP']
except: DB_IP = "192.168.1.188"
try: DB_PORT = os.environ['DB_PORT']
except: DB_PORT = "8089"
try: DB_NAME = os.environ['DB_NAME']
except: DB_NAME = "db0"


class InfluxDB_database:

    def __init__(self):
        """
        Create an object Database which connect to the default database: firstDB
        """
        self.db = InfluxDBClient(DB_IP, DB_PORT)
        self.db.switch_database(DB_NAME)

    def add_request_database(self, name, req):
        """
        This method will store the request into a InfluxDB database.
        The entry will have this format:
        time   hostIp   filePath   logName
        """
        query = "request host_ip=\"" + req.req_json["host_ip"] + "\",file_path=\"" + req.req_json[
            "file_path"] + "\",logviewer_id=\"" + name + "\"" + ",username=\"" + req.req_json["username"] + "\""

        self.db.write([query], {'db': DB_NAME}, 204, 'line')
