import os
from werkzeug.utils import secure_filename


def save_uploaded_file(file_storage, upload_folder):
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file_storage.filename)
    file_path = os.path.join(upload_folder, filename)
    file_storage.save(file_path)
    return file_path
