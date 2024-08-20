import requests
import tempfile
import os
from moviepy.editor import VideoFileClip


def generate_transcript(api_key, video_url):
    # Fixed audio filename
    audio_filename = "extracted_audio.mp3"

    # Download the video
    try:
        video_response = requests.get(video_url)
        video_response.raise_for_status()
    except requests.RequestException as e:
        return False, f"Error downloading video: {str(e)}"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_response.content)
        temp_video_path = temp_video.name

    try:
        # Extract audio from video
        video = VideoFileClip(temp_video_path)

        if video.audio is None:
            return False, "The video does not contain an audio track."

        audio = video.audio

        # Save the audio file locally
        try:
            audio.write_audiofile(audio_filename)
        except Exception as e:
            return False, f"Error extracting audio: {str(e)}"

        video.close()
        audio.close()

        # Prepare the API request
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        with open(audio_filename, "rb") as audio_file:
            files = {
                "file": audio_file,
                "model": (None, "whisper-1"),
                "language": (None, "en"),
                "response_format": (None, "text")
            }

            # Make the API request
            response = requests.post(url, headers=headers, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            return True, response.text
        else:
            return False, f"API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"

    finally:
        # Clean up the temporary video file
        if os.path.exists(temp_video_path):
            os.unlink(temp_video_path)