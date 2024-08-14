import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading

class ConnexionFTP:
    default_host = '127.0.0.1'
    default_port = 21
    default_user = 'admin'
    default_password = 'admin'

    def __init__(self, host=None, port=None):
        self.__host = host if host is not None else ConnexionFTP.default_host
        self.__port = port if port is not None else ConnexionFTP.default_port
        self.__server = None

    def create_server(self, user=None, password=None, dir_path='FTP_folder/', allow_anonymous=False):
        try:
            user = user if user is not None else ConnexionFTP.default_user
            password = password if password is not None else ConnexionFTP.default_password

            os.makedirs(dir_path, exist_ok=True)

            print(f"Creating server with user: {user}, password: {password}, dir_path: {dir_path}")
            authorizer = DummyAuthorizer()

            authorizer.add_user(user, password, dir_path, perm="elradfmw")
            if allow_anonymous:
                authorizer.add_anonymous(dir_path)

            handler = FTPHandler
            handler.authorizer = authorizer

            self.__server = FTPServer((self.__host, self.__port), handler)
            print(f"Server created at {self.__host}:{self.__port}")

        except Exception as e:
            print(f"Error creating server: {e}")

    def start_server(self):
        if self.__server:
            try:
                print("Starting server...")
                server_thread = threading.Thread(target=self.__server.serve_forever)
                server_thread.daemon = True
                server_thread.start()
            except Exception as e:
                print(f"Error starting server: {e}")
            else:
                print("Server started successfully")

    def stop_server(self):
        if self.__server:
            try:
                print("Stopping server...")
                self.__server.close_all()
            except Exception as e:
                print(f"Error stopping server: {e}")
            else:
                print("Server stopped successfully")
