from celery import Celery
from .db import insert_image, delete_task, get_image
from .utils import load_image, compute_statistics, UPLOAD_DIR
import os
import json
from celery.utils.log import get_task_logger

celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
logger = get_task_logger(__name__)  


@celery.task
def process_image(filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        logger.info(file_path)
        image = load_image(file_path)
        stats = compute_statistics(image)
        metadata = {
            'dimensions': [i for i in image.shape],
            'itemsize': image.itemsize,
            'size': image.size,
            'type': str(image.dtype)
        }
        insert_image(filename, json.dumps(metadata), json.dumps(stats))
        delete_task(filename)
    except Exception as e:
        return {'error': True, 'message': str(e)}
    return {'error': False, 'success': True, 'message': 'Succesfully processed the image'}