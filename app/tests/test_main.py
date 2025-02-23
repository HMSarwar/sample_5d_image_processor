import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

TEST_FILE = "sample.TIFF"
TEST_FILE_PATH = os.path.join(os.path.dirname(__file__), TEST_FILE)


def test_upload_image():
    with open(TEST_FILE_PATH, "rb") as f:
        files = {"file": f}
        response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"

def test_get_metadata():
    response = client.get(f"/metadata?filename={TEST_FILE}")
    assert response.status_code == 200
    assert "metadata" in response.json()

def test_get_slice():
    response = client.get(f"/slice?filename={TEST_FILE}&z=0&time=0&channel=0")
    assert response.status_code == 200
    assert "slice" in response.json() or "message" in response.json()

def test_analyze_image():
    response = client.post(f"/analyze?filename={TEST_FILE}")
    assert response.status_code == 200
    assert "pca_results" in response.json()

def test_get_statistics():
    response = client.get(f"/statistics?filename={TEST_FILE}")
    assert response.status_code == 200
    assert "stats" in response.json()
