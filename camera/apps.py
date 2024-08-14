from django.apps import AppConfig

from utils.connexion_ftp import ConnexionFTP


class CameraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camera'

    def ready(self):
        ftp_conn = ConnexionFTP()
        ftp_conn.create_server(user='admin', password='admin', dir_path='media/captures')
        ftp_conn.start_server()
