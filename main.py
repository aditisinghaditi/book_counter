"""CLI entry point for the book counter."""

import argparse
import sys

from counter import count_books
from camera import run_camera


def main():
    parser = argparse.ArgumentParser(description="Count books in an image or via live camera.")
    subparsers = parser.add_subparsers(dest="command")

    # Image mode
    img_parser = subparsers.add_parser("image", help="Count books from an image file")
    img_parser.add_argument("path", help="Path to the image file")
    img_parser.add_argument(
        "--confidence", type=float, default=0.3,
        help="Detection confidence threshold (0-1, default: 0.3)"
    )
    img_parser.add_argument(
        "--no-save", action="store_true",
        help="Skip saving the annotated output image"
    )

    # Camera mode
    cam_parser = subparsers.add_parser("camera", help="Count books using live camera feed")
    cam_parser.add_argument(
        "--confidence", type=float, default=0.3,
        help="Detection confidence threshold (0-1, default: 0.3)"
    )
    cam_parser.add_argument(
        "--device", type=int, default=0,
        help="Camera device index (default: 0)"
    )

    args = parser.parse_args()

    if args.command == "image":
        try:
            result = count_books(args.path, confidence=args.confidence, save_annotated=not args.no_save)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Books detected: {result['count']}")
        if result["output_path"]:
            print(f"Annotated image saved to: {result['output_path']}")

    elif args.command == "camera":
        run_camera(confidence=args.confidence, camera_index=args.device)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
