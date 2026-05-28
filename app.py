"""FastAPI web app for book counting via phone camera."""

import io
import base64
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from ultralytics import YOLO

BOOK_CLASS_ID = 73

app = FastAPI(title="Book Counter")
model = YOLO("yolov8n.pt")


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("templates/index.html").read_text()


@app.post("/count")
async def count_books(image: UploadFile = File(...), confidence: float = 0.3):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    results = model(img, conf=confidence, verbose=False)

    book_count = 0
    for result in results:
        for box in result.boxes:
            if int(box.cls) == BOOK_CLASS_ID:
                book_count += 1

    # Generate annotated image as base64
    annotated = results[0].plot()
    annotated_img = Image.fromarray(annotated)
    buffer = io.BytesIO()
    annotated_img.save(buffer, format="JPEG", quality=85)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {"count": book_count, "annotated_image": img_base64}
