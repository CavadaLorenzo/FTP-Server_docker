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
from database import Database
from reader_thread import Reader

"""
DIR = os.environ['LOG_DIR']
ID = os.environ['ID']
SERVER_IP = os.environ['SERVER_IP']
SERVER_PORT = os.environ['SERVER_PORT']
SSH_PORT = os.environ['SSH_PORT']
"""

# only for debug

DIR = "./logviewer_env"
ID = "server1"
SERVER_IP = "192.168.1.188"
SERVER_PORT = "3001"
SSH_PORT = "3022"


def create_thread():
    """
    This method will create and return an array of thread. Each thread regards a specific
    log file, the thread will read from the file in real time.
    Each file is identified by its name and the file itself.
    """
    threads = []

    control = True
    while control:
        files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        for file_name in files:
            if file_name == "vsftpd.log":
                file = (open((DIR + str(file_name)), "r"))
                threads.append(Reader(ID, file))
                control = False

    return threads

def add_info_to_db():
    """
    This method will add this new server to the measurement which tracks all the FTP servers.
    Each server will be identify throw is IP and PORT, in the database will also be added
    the SSH PORT that can be used to copy file to them. 
    """
    db = Database()
    db.add_new_server(SERVER_IP, SERVER_PORT, SSH_PORT, ID)

def main():
    """
    Main function of the script, here is where the thread will be launch.
    Here will also be added the information about this FTP server to the database.
    """
    print("Script running and waiting for new entry")

    add_info_to_db()

    print("Added information of this server to the database")
"""
    threads = create_thread()

    for thread in threads:
        thread.start()
"""

if __name__ == "__main__":
    main()
