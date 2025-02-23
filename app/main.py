
from fastapi import FastAPI, File, UploadFile
import os
import uvicorn
import tempfile
from .utils import get_data, extract_slice, analyze_pca
from .tasks import process_image
from .db import insert_task, get_task, init_db

app = FastAPI()
os.makedirs("uploads", exist_ok=True)
init_db()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"uploads/{file.filename}"
    with open(filename, "wb") as buffer:
        buffer.write(await file.read())
    task_id = process_image.apply_async(args=[file.filename])
    insert_task(filename, str(task_id))
    return {"message": "File uploaded successfully"}

@app.get("/metadata")
async def get_metadata(filename: str):
    if get_task(filename):
        return {'message': "File is still processing"}
    return get_data(filename)

@app.get("/slice")
async def get_slice(filename: str, z: int, time: int, channel: int):
    sliced = extract_slice(filename, z, time, channel)
    if type(sliced) == dict:
        return sliced
    return {"slice": sliced.tolist()}

@app.post("/analyze")
async def analyze_image(filename: str):
    if get_task(filename):
        return {'message': "File is still processing"}
    return analyze_pca(filename)

@app.get("/statistics")
async def get_statistics(filename: str):

    if get_task(filename):
        return {'message': "File is still processing"}
    return get_data(filename, ftype='stats')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)