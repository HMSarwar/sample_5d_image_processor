
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, BackgroundTasks
import os
import uvicorn
import tempfile
from .utils import process_image, get_data, extract_slice, analyze_pca

app = FastAPI()
os.makedirs("uploads", exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"uploads/{file.filename}"
    with open(filename, "wb") as buffer:
        buffer.write(await file.read())
    process_image(file.filename)
    return {"message": "File uploaded successfully"}

@app.get("/metadata")
async def get_metadata(filename: str):
    return get_data(filename)

@app.get("/slice")
async def get_slice(filename: str, z: int, time: int, channel: int):
    sliced = extract_slice(filename, z, time, channel)
    if type(sliced) == dict:
        return sliced
    return {"slice": sliced.tolist()}

@app.post("/analyze")
async def analyze_image(filename: str):
    return analyze_pca(filename)

@app.get("/statistics")
async def get_statistics(filename: str):
    return get_data(filename, ftype='stats')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)