from flask import Blueprint, request, redirect, url_for

from config.settings import UPLOAD_FOLDER
from services.file_service import save_uploaded_file


upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            save_uploaded_file(file, UPLOAD_FOLDER)
        return redirect(url_for('home.home'))
    return '<form method="post" enctype="multipart/form-data"><input type="file" name="file"><button type="submit">Upload</button></form>'
