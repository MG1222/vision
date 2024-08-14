from django.shortcuts import render
from django.http import JsonResponse


import os
import time
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import ImageCapture
from utils.connexion_tcp import ConnexionTCP
from utils.connexion_ftp import ConnexionFTP


def test_connection(request):
    tcp_conn = ConnexionTCP()
    tcp_conn.start_connexion()

    if tcp_conn.is_open():
        tcp_conn.stop_connexion()
        return JsonResponse({"status": "success", "message": "Connexion réussie à la caméra"})
    else:
        return JsonResponse({"status": "error", "message": "Connexion à la caméra échouée"})


def capture_image(request):
    # Initialize TCP connection
    tcp_conn = ConnexionTCP()
    tcp_conn.start_connexion()

    if tcp_conn.is_open():
        try:
            # Trigger camera to capture image
            tcp_send = tcp_conn.send_data()
            time.sleep(2)
            data = tcp_conn.receive_data()
            tcp_conn.stop_connexion()
            size = len(data)

            if data:

                for line in data:
                    if b"HTTP/1.1 400 Bad Request" in line:
                        return JsonResponse({"status": "error", "message": "400 Bad Request from camera"})
                image_data = data[0]
                image_data_size = len(image_data)
                if image_data_size == 309:
                    return JsonResponse({"status": "error", "message": "Image not captured"})
                capture_count = ImageCapture.objects.count() + 1
                filename = f'capture{capture_count:02d}.bmp'
                image_file = ContentFile(image_data, filename)

                img = ImageCapture(image=image_file)
                img.save()

                ftp_directory = os.path.join('media/', img.image.name)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(ftp_directory), exist_ok=True)

                with open(ftp_directory, 'wb') as f:
                    f.write(image_data)

                return JsonResponse({"status": "success", "image_id": img.id})
            else:
                return JsonResponse({"status": "error", "message": "No data received from camera"})
        except Exception as e:
            tcp_conn.stop_connexion()
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Connection to camera failed"})


def gallery(request):
    images = ImageCapture.objects.all()
    return render(request, 'gallery.html', {'images': images})
