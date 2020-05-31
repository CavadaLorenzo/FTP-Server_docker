##
# @file
# The main class. Here is where the script will start
# First of all the script will search in a specific directory all the
# log file. For each log file it will create a thread for the reading and parsing part.
#
# Constant:
# DIR: indicates the path where the log are stored
# ID: indicates the logviewer ID
# SERVER_IP: indicates the IP of the server where the docker-compose is created
# SERVER_PORT: indicates the PORT of the server which is listening for ssh connection

import os
import os.path
from reader import Reader
from postgres_database import PostgresDB
import time


# default value is used when KeyError exception is raised
try:    DIR =  os.environ['LOG_DIR'] 
except:    DIR = "/home/lorenzo/Desktop/"
try:    ID = os.environ['ID'] 
except:    ID = "server1"
try:    SERVER_IP = os.environ['SERVER_IP'] 
except:    SERVER_IP = "192.168.1.188"
try:    SERVER_PORT = os.environ['SERVER_PORT'] 
except:    SERVER_PORT = "3001"
try:    SSH_PORT = os.environ['SSH_PORT'] 
except:    SSH_PORT = "3022"
try:    LOG_FILE_NAME = os.environ['LOG_FILE_NAME'] 
except:     LOG_FILE_NAME = "vsftpd.log"


def add_info_to_db():
    """
    First of all is checked if the server's info are already saved in the the database.
    If not, this method will add this new server to the postgresDB which tracks all the FTP servers.
    Each server will be identify throw its ID, also its IP, PORT and SSH PORT that can be used to 
    copy file to them will be added in the database.
    """
    db = PostgresDB()
    if not db.check_existence_server(ID):
        db.add_new_server(SERVER_IP, SERVER_PORT, SSH_PORT, ID)
        print(f"Server: {ID} added in the database")
    else:
        print(f"Server: {ID} is already saved in the Database")


def main():
    """
    Main function of the script, here is where the reader will be launch.
    Here will also be added the information about this FTP server to the database.
    The log file is searched in the DIR path provided as environment variable. 
    The default log name is vsftpd.log but can be changed changin the environ variable
    LOG_FILE_NAME.
    """
    print("Script running and waiting for new entry")

    add_info_to_db()

    no_file_found = True
    while no_file_found:
        if 'file' in locals():
            no_file_found = False
        else:
            files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            for file_name in files:
                if file_name == LOG_FILE_NAME:
                    file = (open((DIR + str(file_name)), "r"))
                    file = Reader(ID, file)
            print("No log file, sleeping for 5 seconds")
            time.sleep(5)

    file.read()


if __name__ == "__main__":
    main()
