"""Book counting module using YOLOv8 object detection."""

from pathlib import Path
from ultralytics import YOLO


# COCO class index for "book" is 73
BOOK_CLASS_ID = 73


def count_books(image_path: str, confidence: float = 0.3, save_annotated: bool = True) -> dict:
    """
    Detect and count books in an image.

    Args:
        image_path: Path to the input image.
        confidence: Minimum confidence threshold for detections.
        save_annotated: Whether to save an annotated image with bounding boxes.

    Returns:
        Dictionary with 'count' and 'output_path' (if saved).
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    model = YOLO("yolov8n.pt")  # Downloads automatically on first run

    results = model(str(image_path), conf=confidence, verbose=False)

    # Filter detections for "book" class only
    book_count = 0
    for result in results:
        for box in result.boxes:
            if int(box.cls) == BOOK_CLASS_ID:
                book_count += 1

    output_path = None
    if save_annotated and book_count > 0:
        output_path = image_path.parent / f"{image_path.stem}_counted{image_path.suffix}"
        # Filter results to only show book detections
        annotated = results[0].plot()
        from PIL import Image
        Image.fromarray(annotated).save(str(output_path))

    return {"count": book_count, "output_path": str(output_path) if output_path else None}
