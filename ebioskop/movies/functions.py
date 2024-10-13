import os
from flask import current_app
from werkzeug.utils import secure_filename


# Funkcija za čuvanje slike
def save_image(file, filename):
    if file and file.filename:
        filename = secure_filename(filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'movies')
        
        # Kreiranje foldera ako ne postoji
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return os.path.join('static', 'img', 'movies', filename)
    else:
        print(f'debug: nije učitan fajl za {filename}!')
    return None