import uuid
from datetime import datetime


def get_name_of_file(instance, file):
    ext = file.split('.')[-1]
    new_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4()}.{ext}"
    return f"user_uploads/{new_filename}"
