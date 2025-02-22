import os
import numpy as np
import tifffile as tiff
from sklearn.decomposition import PCA
from skimage.filters import threshold_otsu
import tempfile
from db import insert_image, init_db, get_image
import json

init_db()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


def load_image(file_path):
    return tiff.imread(file_path)


def extract_slice(image, z=None, time=None, channel=None):
    try:
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
        print(stats, metadata)
        insert_image(filename, json.dumps(metadata), json.dumps(stats))
        print(get_image(filename))
    except Exception as e:
        raise e
        return {'error': True, 'message': str(e)}
    return {'error': False, 'success': True, 'message': 'Succesfully processed the image'}

def segment_image(image):
    threshold = threshold_otsu(image)
    return (image > threshold).astype(int)

process_image('MODAL2_M_AER_RA_2016-09-01_rgb_1440x720.TIFF')
