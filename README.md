# Book Stack Counter

AI-powered book counting system that uses Google Gemini 2.5 Flash to detect and count books in images. Supports live camera feed and image upload via a web interface accessible from any device (phone/laptop).

## Features

- Upload an image or use your phone/laptop camera to scan book stacks
- AI reads spine labels and counts individual books
- Collated inventory table showing book names and quantities
- Accumulates data across multiple scans
- Mobile-friendly responsive UI

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/aditisinghaditi/book_counter.git
cd book_counter
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key

Get a free API key from https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
GEMINI_API_KEY=your-api-key-here
```

### 5. Start the server

```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```

### 6. Open in browser

- On laptop: http://localhost:5000
- On phone (same WiFi): http://<your-laptop-ip>:5000

Find your laptop IP with:

```bash
hostname -I
```

## Usage

- Click "Open Camera" to start live camera feed, then "Capture & Count" to analyze
- Click "Upload Image" to select or take a photo
- The lower half shows a collated table of detected book titles and quantities
- Scan multiple stacks — the inventory accumulates across scans
- Click "Clear" to reset the table

## Rate Limits (Free Tier)

Gemini 2.5 Flash free tier allows:
- 20 requests per day
- 5 requests per minute

## Tech Stack

- FastAPI (backend)
- Google Gemini 2.5 Flash (AI vision)
- Vanilla HTML/JS (frontend)
- Pillow (image handling)
