import os
import numpy as np
import tifffile as tiff
from sklearn.decomposition import PCA
from skimage.filters import threshold_otsu
import tempfile
from .db import insert_image, init_db, get_image
import json

init_db()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


def load_image(file_path):
    return tiff.imread(file_path)


def extract_slice(filename, z=None, time=None, channel=None):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)

        if not os.path.exists(file_path):
            return {"error": "No file found"}
        image = load_image(file_path)
        return image[:, :, z, time, channel]
    except Exception as e:
        return image

def compute_pca(image, n_components=3):
    reshaped = image.reshape(-1, image.shape[-1])
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(reshaped)
    return reduced.reshape(image.shape[:-1] + (n_components,))

def compute_statistics(image):
    try:
        return {
            "mean": np.mean(image, axis=(0, 1, 2)).tolist(),
            "std": np.std(image, axis=(0, 1, 2)).tolist(),
            "min": np.min(image, axis=(0, 1, 2)).tolist(),
            "max": np.max(image, axis=(0, 1, 2)).tolist()
        }
    except Exception as e:
        # if the image is single channeled
        
        return {
            "mean": np.mean(image, axis=(0, 1)).tolist(),
            "std": np.std(image, axis=(0, 1)).tolist(),
            "min": np.min(image, axis=(0, 1)).tolist(),
            "max": np.max(image, axis=(0, 1)).tolist()
        }

def process_image(filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        image = load_image(file_path)
        stats = compute_statistics(image)
        metadata = {
            'dimensions': [i for i in image.shape],
            'itemsize': image.itemsize,
            'size': image.size,
            'type': str(image.dtype)
        }
        insert_image(filename, json.dumps(metadata), json.dumps(stats))
    except Exception as e:
        return {'error': True, 'message': str(e)}
    return {'error': False, 'success': True, 'message': 'Succesfully processed the image'}

def segment_image(image):
    threshold = threshold_otsu(image)
    return (image > threshold).astype(int)


def get_data(filename, ftype='meta'):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            return {"error": "No file found"}
        data = get_image(filename)
        if not data.get('data'):
            return {"message": "Data not found"}
        if ftype != 'meta':
            return {"stats": data.get('data')[1]}
        return {"metadata": data.get('data')[0]}
    except Exception as e:
        return {"error": "No data found"}
    
def analyze_pca(filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "No file found"}
    image = load_image(file_path)
    return {"pca_results": compute_pca(image).tolist()}