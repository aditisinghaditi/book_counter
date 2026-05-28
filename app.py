"""FastAPI web app for book counting via phone camera."""

import io
import base64
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from counter import count_books

app = FastAPI(title="Book Counter")


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("templates/index.html").read_text()


@app.post("/count")
async def count_books_endpoint(image: UploadFile = File(...)):
    contents = await image.read()
    result = count_books(image_bytes=contents)

    # Send back the original image as base64 for display
    img_base64 = base64.b64encode(contents).decode()

    return {
        "count": result.get("count", 0),
        "titles": result.get("titles", []),
        "image": img_base64
    }
