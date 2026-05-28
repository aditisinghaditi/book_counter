# Book Stack Counter

Counts the number of books in an image using YOLOv8 object detection.

## Setup

```bash
cd book_counter
pip install -r requirements.txt
```

## Usage

```bash
python main.py path/to/book_stack.jpg
```

Options:
- `--confidence 0.5` — adjust detection threshold (default 0.3, lower = more detections)
- `--no-save` — skip saving the annotated output image

## How it works

Uses a pre-trained YOLOv8 model (COCO dataset) which includes "book" as one of its 80 object classes. The model detects individual books in the image and returns the total count. An annotated image with bounding boxes is saved alongside the input.

## Notes

- The model downloads automatically on first run (~6MB).
- Works best with clearly visible book spines/covers. Tightly packed stacks where individual books aren't visually distinct may undercount.
- Lower the confidence threshold if books are being missed, raise it if you get false positives.
