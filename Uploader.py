from parse_export import read_submission
import tempfile
from werkzeug.utils import secure_filename

def upload_file(request, tiger):
    f = request.files['file']
    temp_dir = tempfile.TemporaryDirectory()
    path = temp_dir.name + '/' + secure_filename(f.filename)
    f.save(path)
    read_submission(path, temp_dir.name, tiger)
    temp_dir.cleanup()