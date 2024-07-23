import yt_dlp
from moviepy.editor import VideoFileClip
from flask import Flask, request, render_template, send_file
import os
import speech_recognition as sr
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/process-url', methods=['POST'])
def process_url():
    save_path = os.path.expanduser("~/Desktop")  # Use the user's Desktop directory
    url = request.form.get('youtube-url')
    
    if not url:
        return render_template('download.html', message="Please enter a URL.")
    
    print(f"Received URL: {url}")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            ydl.download([url])
            return render_template('download.html', message=f"Downloaded successfully! Video title: {video_title}")
    except Exception as e:
        print(f"Error: {e}")
        return render_template('download.html', message="Error occurred. Please check the URL and try again.")

@app.route('/convert')
def convert():
    return render_template('convert.html')


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert_video', methods=['POST'])
def convert_video():
    if 'convert-video' not in request.files:
        return render_template('home.html', message="Please upload a video and try again.")

    file = request.files['convert-video']

    if file.filename == '':
        return render_template('home.html', message="No file selected.")

    if file and file.filename.endswith(".mp4"):
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path)
            video.close()
            # Remove the original video file
            os.remove(video_path)
            
            return send_file(audio_path, as_attachment=True)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('convert.html', message="Error during conversion. Please try again.")

    return render_template('convert.html', message="Invalid file format. Please upload a .mp4 file.")

@app.route('/convert_url', methods=['POST'])
def convert_url():
    url = request.form.get('youtube-url')
    
    if not url:
        return render_template('convert.html', message="Please enter a URL.")
    
    print(f"Received URL: {url}")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        if os.path.exists(audio_file):
            return send_file(audio_file, as_attachment=True)
        else:
            return render_template('convert.html', message="Error converting the video to audio.")
    except Exception as e:
        print(f"Error: {e}")
        return render_template('convert.html', message="Error occurred. Please check the URL and try again.")

@app.route('/subtitles')
def subtitles():
    return render_template('subtitles.html')


DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

import cv2
import numpy as np
import cv2
import numpy as np

def draw_text_on_frame(frame, text, font_scale=0.6, thickness=1, font=cv2.FONT_HERSHEY_SIMPLEX):
    """Draw text on the video frame."""
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] - text_size[1] - 5  # 5 pixels from the bottom
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)

def add_subtitles_to_video(video_path, subtitles, output_path):
    """Add subtitles to video using OpenCV."""
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Read and process each frame
    frame_idx = 0
    subtitle_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Add subtitles to the frame
        if subtitle_idx < len(subtitles):
            subtitle = subtitles[subtitle_idx]
            if subtitle['start'] <= (frame_idx / fps) <= subtitle['end']:
                draw_text_on_frame(frame, subtitle['text'], font_scale=0.6, thickness=1)

            if (frame_idx / fps) > subtitle['end']:
                subtitle_idx += 1

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()


@app.route('/subtitles_video', methods=['POST'])
def subtitles_video():
    if 'video' not in request.files:
        return render_template('subtitles.html', message="No video file uploaded.")

    video_file = request.files['video']
    if video_file.filename == '':
        return render_template('subtitles.html', message="No selected file.")

    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)

    try:
        # Open and process the video file
        with VideoFileClip(video_path) as video:
            audio_path = os.path.splitext(video_path)[0] + ".wav"
            video.audio.write_audiofile(audio_path)
        
        # Process the audio file
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as audio:
            audio_data = recognizer.record(audio)
            text = recognizer.recognize_google(audio_data)
        
        # Split text into subtitles
        subtitles = []
        words = text.split()
        duration = video.duration
        words_per_subtitle = 5
        for i in range(0, len(words), words_per_subtitle):
            start_time = (i / len(words)) * duration
            end_time = ((i + words_per_subtitle) / len(words)) * duration
            subtitle_text = " ".join(words[i:i + words_per_subtitle])
            subtitles.append({"text": subtitle_text, "start": start_time, "end": end_time})
        
        # Set the output video path
        output_video_path = os.path.join(DOWNLOAD_FOLDER, f"subtitled_{video_file.filename}")
        
        # Add subtitles to the video
        add_subtitles_to_video(video_path, subtitles, output_video_path)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('subtitles.html', message="Error during subtitle processing. Please try again.")
    
    finally:
        # Clean up the uploaded video and audio files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    # Provide the video file for download directly
    return send_file(output_video_path, as_attachment=True, download_name=f"subtitled_{video_file.filename}")

if __name__ == '__main__':
    app.run(debug=True)
