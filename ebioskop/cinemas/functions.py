import os
from flask import current_app


def save_picture(form_picture, cinema_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'representative_{cinema_id:03d}{f_ext}'
    
    # Kreiramo direktorijum ako ne postoji
    picture_dir = os.path.join(current_app.root_path, 'static', 'img', 'cinema_representative')
    os.makedirs(picture_dir, exist_ok=True)
    
    picture_path = os.path.join(picture_dir, picture_fn)
    
    # Čuvamo sliku
    form_picture.save(picture_path)
    
    return picture_fn