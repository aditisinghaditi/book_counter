"""Live camera feed for book counting."""

import cv2
from ultralytics import YOLO

BOOK_CLASS_ID = 73


def run_camera(confidence: float = 0.3, camera_index: int = 0):
    """
    Open camera feed, detect books in real-time, and display count.

    Controls:
        - Press 'c' to capture and print the current book count.
        - Press 'q' to quit.

    Args:
        confidence: Detection confidence threshold.
        camera_index: Camera device index (0 = default webcam).
    """
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera opened. Point at a book stack.")
    print("  Press 'c' to capture count")
    print("  Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        results = model(frame, conf=confidence, verbose=False)

        # Count books in this frame
        book_count = 0
        for result in results:
            for box in result.boxes:
                if int(box.cls) == BOOK_CLASS_ID:
                    book_count += 1
                    # Draw bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf_val = float(box.conf[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"book {conf_val:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display count on frame
        cv2.putText(frame, f"Books: {book_count}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow("Book Counter - Press 'c' to capture, 'q' to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            print(f"\n>>> Captured! Books detected: {book_count}")

    cap.release()
    cv2.destroyAllWindows()
