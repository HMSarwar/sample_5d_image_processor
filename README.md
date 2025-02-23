# Sample 5D Image Processor

This repository provides a FastAPI-based application for processing 5D image files (TIFF format). It includes endpoints for uploading images, extracting slices, computing PCA, and analyzing statistics.

## Prerequisites

Ensure the following dependencies are installed before running the application:

- **Python 3.8 or higher**
- **Redis** (for Celery task processing)

## Installation

### Clone the Repository
```bash
git clone https://github.com/HMSarwar/sample_5d_image_processor.git
cd sample_5d_image_processor
```

### Set Up a Virtual Environment
```bash
# On Unix/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```


## Running the Application

### Start Redis Server
```bash
redis-server
```

### Start Celery Worker
```bash
celery -A app.tasks worker --loglevel=info
```

### Run the FastAPI Application
```bash
uvicorn app.main:app
```

The API will be accessible at `http://127.0.0.1:8000`.

## API Documentations
http://127.0.0.1:8000/docs/

## API Endpoints


### Upload an Image
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@path_to_image.tif"
```

### Get Image Metadata
```bash
curl -X GET "http://127.0.0.1:8000/metadata?file_path=uploads/image.tif"
```

### Extract an Image Slice
```bash
curl -X GET "http://127.0.0.1:8000/slice?file_path=uploads/image.tif&z=0&time=0&channel=0"
```

### Analyze Image
```bash
curl -X POST "http://127.0.0.1:8000/analyze" -d "file_path=uploads/image.tif"
```

### Get Image Statistics
```bash
curl -X GET "http://127.0.0.1:8000/statistics?file_path=uploads/image.tif"
```


