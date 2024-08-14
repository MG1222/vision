import configparser

config_dynamic = configparser.ConfigParser()
config_dynamic.read('config.ini')


class Logger:
    @staticmethod
    def info(msg):
        print("INFO:", msg)

    @staticmethod
    def error(msg):
        print("ERROR:", msg)

    @staticmethod
    def exception(msg):
        print("EXCEPTION:", msg)

    @staticmethod
    def warning(msg):
        print("WARNING:", msg)


logger = Logger()
