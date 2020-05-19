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

    def add_new_server(self, server_ip, server_port, ssh_port, server_id):
        """
        This method will store into the influxDB the new server.
        The new server will be identify by its IP and its PORT.
        It will be stored also the SSH PORT used to move file into them.
        First of all the script will checkl if the server is already in the database,
        in this case will delete the old entry and upload the new one.
        """
        query = "DROP SERIES FROM servers WHERE server_ip='" + server_ip + "' AND server_port='" + server_port + "' AND ssh_port='" + ssh_port + "' AND server_id='" + server_id + "'"
        print(query)
        result_set = self.db.query(query).get_points(measurement='servers')
        print(result_set)
        for server in result_set:
            print(server)