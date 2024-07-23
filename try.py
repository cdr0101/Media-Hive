# url = 'https://youtu.be/2AbW6Wq4-LE?si=a1ytcDQZTta3ELTL'

from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


link = input("Enter the YouTube video URL: ")
Download(link)



def search_youtube_videos(singer_name, num_videos):
    print("Searching YouTube for video URLs...")
    videosSearch = VideosSearch(singer_name, limit=num_videos)
    results = videosSearch.result()
    video_urls = [video['link'] for video in results['result']]
    return video_urls

def download_videos(video_urls):
    print(f"Downloading {len(video_urls)} videos...")
    for url in video_urls:
        yt = YouTube(url)
        yt.streams.filter(only_audio=True).first().download()

def convert_to_audio():
    print("Converting videos to audio...")
    for file in os.listdir():
        if file.endswith(".mp4"):
            audio_name = os.path.splitext(file)[0] + ".mp3"
            video = AudioSegment.from_file(file)
            video.export(audio_name, format="mp3")
            os.remove(file)