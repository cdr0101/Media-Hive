# MediaHive
## Download , Convert , Caption!        
MediaHive is a versatile multimedia processing web application. It allows users to convert videos (mp4) to audio (mp3), download YouTube videos and insert subtitles into videos. 

### Features

1. **Download YouTube Videos**: Download videos from YouTube directly to your local machine.
2. **Convert Video to Audio**: Convert local video files or YouTube videos to audio files in MP3 format. 
3. **Insert Subtitles into Video**: Automatically generate and add subtitles to your videos using speech recognition.

### Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/mediahive.git
    cd mediahive
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    python app.py
    ```

### Usage

#### Download YouTube Videos

1. Navigate to the "Download YouTube Videos" page.
2. Enter the YouTube video URL.
3. Click "Download" to save the video to your local machine.

#### Convert Video to Audio

1. Navigate to the "Convert Video to Audio" page.
2. Upload a local video file or provide a YouTube URL.
3. Click "Convert" to download the audio file in MP3 format.

#### Insert Subtitles into Video

1. Navigate to the "Insert Subtitles into Video" page.
2. Upload a local video file.
3. Click "Process" to download the video with embedded subtitles.

### Dependencies

This project relies on the following major libraries and tools:

- Flask
- yt-dlp
- moviepy
- speech_recognition
- opencv-python

### Folder Structure

```
MediaHive/
│
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── static/               # Static CSS files
│   └── styles.css
├── templates/            # HTML templates
│   ├── home.html
│   ├── download.html
│   ├── convert.html
│   └── subtitles.html
├── uploads/              # Folder for uploaded files (Automatically generated later, if not present)
├── downloads/            # Folder for processed files (Automatically generated later, if not present)
└── README.md             # Guide
```

## License

This project is licensed under the MIT License.
