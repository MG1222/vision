# camera/utils/connexion_tcp.py
import socket
import configparser
import config


class ConnexionTCP:
    default_host = '127.0.0.1'
    default_port = 8080
    section_name = 'tcp_settings'

    def __init__(self):
        self.__host = ConnexionTCP.default_host
        self.__port = ConnexionTCP.default_port
        self.__connexion = None
        self.__open = False
        self.init_connexion_param()

    def init_connexion_param(self):
        """Init param from config file"""
        if not config.config_dynamic.has_section(ConnexionTCP.section_name):
            config.config_dynamic.add_section(ConnexionTCP.section_name)

        try:
            self.__host = config.config_dynamic.get(ConnexionTCP.section_name, 'host')
        except configparser.NoOptionError:
            self.set_host(ConnexionTCP.default_host)

        try:
            port_str = config.config_dynamic.get(ConnexionTCP.section_name, 'port')
            self.__port = int(port_str)
        except (configparser.NoOptionError, ValueError):
            self.set_port(ConnexionTCP.default_port)

    def start_connexion(self):
        """Start the connexion"""
        try:
            self.stop_connexion()
            self.set_connexion(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            self.get_connexion().connect((self.get_host(), self.get_port()))
            self.get_connexion().settimeout(2)
            msg = f"La connexion avec la caméra a réussi. Host: {self.get_host()} Port: {self.get_port()}"
            config.logger.info(msg=msg)
            self.set_open(True)
        except socket.error:
            msg = f"La connexion avec la caméra a échoué. Host: {self.get_host()} Port: {self.get_port()}"
            config.logger.error(msg=msg)
        except Exception as exp:
            config.logger.exception("Exception non gérée dans le démarrage de la connexion.")

    def send_data(self):
        """Send data to the camera"""
        if self.is_open():
            try:
                data = "||>TRIGGER ON\r\n"
                self.get_connexion().sendall(bytes(data, 'UTF-8'))
                config.logger.info(f"Sent data: {data}")
                return True
            except ConnectionResetError as exp:
                msg = "La caméra ne communique plus"
                config.logger.warning(msg=msg)
                self.stop_connexion()
        return False

    def receive_data(self):
        """Get the data from the camera"""
        try:
            msg_received = self.__connexion.recv(2048)
            if len(msg_received) == 0:
                self.stop_connexion()
                return None
            config.logger.info(f"Received data: {msg_received.decode('UTF-8')}")
            return [msg_received]
        except socket.timeout:
            config.logger.warning("Timeout while receiving data")
            return None

    def stop_connexion(self):
        """Ferme la connexion"""
        if self.is_open():
            self.set_open(False)
            self.get_connexion().close()

    def get_connexion(self):
        """Getter pour __connexion"""
        return self.__connexion

    def set_connexion(self, connexion):
        """Setter pour __connexion"""
        self.__connexion = connexion

    def set_open(self, open_flag):
        """Setter pour l'état de la connexion"""
        self.__open = open_flag

    def is_close(self):
        """Teste si la connexion est fermée"""
        return not self.__open

    def is_open(self):
        """Teste si la connexion est ouverte"""
        return self.__open

    def get_host(self):
        """Getter pour __host"""
        return self.__host

    def set_host(self, host):
        """Setter pour __host"""
        self.__host = host
        config.config_dynamic.set(ConnexionTCP.section_name, 'host', host)

    def get_port(self):
        """Getter pour __port"""
        return self.__port

    def set_port(self, port):
        """Setter pour __port"""
        self.__port = port
        config.config_dynamic.set(ConnexionTCP.section_name, 'port', str(port))
