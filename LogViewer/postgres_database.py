import psycopg2, os


# default value is used when KeyError exception is raised
try:    POSTGRES_IP =  os.environ['POSTGRES_IP'] 
except:    POSTGRES_IP = '192.168.1.188'
try:    POSTGRES_PORT = os.environ['POSTGRES_PORT'] 
except:    POSTGRES_PORT = '54320'
try:    POSTGRES_USER = os.environ['POSTGRES_USER'] 
except:    POSTGRES_USER = 'admin'
try:    POSTGRES_DB_NAME = os.environ['POSTGRES_DB_NAME'] 
except:    POSTGRES_DB_NAME = 'servers'
try:    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD'] 
except:    POSTGRES_PASSWORD = 'POSTGRES_PASSWORD'

class PostgresDB:
    def __init__(self):
        """
        Create an object PostgreDB which connect to the given database. 

        :param host: is the database IP
        :param database: is the name of the database
        :param user: is the user used to connect to the database
        :param password: is the password used to connect to the database
        :param port: is the port used to connecto to the database
        """
        self.conn = psycopg2.connect(host = POSTGRES_IP, 
                                    database = POSTGRES_DB_NAME, 
                                    user = POSTGRES_USER, 
                                    password = POSTGRES_PASSWORD,
                                    port = POSTGRES_PORT) 

    def add_new_server(self, server_ip, server_port, ssh_port, server_id):
        """
        Add the info of a new FTP server to the database.

        :param server_ip: is the IP of the new FTP server
        :param server_port: is the port of the new FTP server
        :param ssh_port: is the SSH port used to move file to the FTP server
        :param server_id: is the unique id which identify each FTP server
        """
        query  = f'INSERT INTO servers(server_id, server_ip, server_port, server_ssh_port) VALUES (\'{server_id}\', \'{server_ip}\', \'{server_port}\', \'{ssh_port}\')'
        cursor = self.conn.cursor()
        cursor.execute(query)

    def check_existence_server(self, server_id):
        """
        This method will check if a specif server is already in the servers database.
        This is to prevent the insert of a server multiple times

        :param server_id: the id of the new FTP server
        """
        select_all_query = f"SELECT * FROM \"Servers\" WHERE server_name = \'{server_id}\'"
        cursor = self.conn.cursor()
        cursor.execute(select_all_query)
        return len(cursor.fetchall()) > 0
