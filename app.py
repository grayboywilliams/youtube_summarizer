from anyio import Path
from pytube import YouTube
from openai import OpenAI
import os
import re

# Constants
summary_dir = os.path.dirname(os.path.realpath(__file__)) + "\summaries"
transcription_model = "whisper-1"
summary_model = "gpt-4-1106-preview"
summary_tokens = 1000
client = OpenAI()

# Function to sanitize a string to be used as a directory name
def sanitize_title(title):
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)  # Remove invalid characters
    sanitized = sanitized.replace(' ', '_')  # Replace spaces with underscores
    return sanitized

# Function to download audio
def download_audio(yt: YouTube, save_path, file_name="audio.mp4"):
    audio_file = os.path.join(save_path, file_name)

    if os.path.exists(audio_file):
        return audio_file
    
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=save_path, filename=file_name)
    return audio_file

# Function to transcribe audio
def transcribe_audio(file_path, save_path, file_name="transcription.txt"):
    transcript_file = os.path.join(save_path, file_name)

    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as file:
            return file.read(), transcript_file
    
    response = client.audio.transcriptions.create(
        model=transcription_model,
        file=Path(file_path))
    
    with open(transcript_file, "w", encoding="utf-8") as file:
        file.write(response.text)

    return response.text, transcript_file

# Function to summarize text
def summarize_text(text, title, author, save_path, file_name="summary.txt"):
    summary_file = os.path.join(save_path, file_name)

    response = client.chat.completions.create(
        model=summary_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The following transcript is from a YouTube video called {title} by {author}. Please summarize it:\n\n{text}"}
        ],
        max_tokens=summary_tokens)
    
    
    with open(summary_file, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

    return response.choices[0].message.content

def main():
    global summary_tokens

    # Prompt for video URL
    video_url = input("Enter the YouTube video URL: ")
    tokens = input("Enter the max number of tokens in summary (or hit enter for 1000): ")
    summary_tokens = int(tokens) if tokens else summary_tokens
    
    # Create YouTube object
    yt = YouTube(
        video_url,
        use_oauth=True,
        allow_oauth_cache=True
    )

    # Get sanitized title and create directory
    sanitized_title = sanitize_title(yt.title)
    save_path = os.path.join(summary_dir, sanitized_title)
    os.makedirs(save_path, exist_ok=True)
    
    # Download audio
    audio_file = download_audio(yt, save_path)
    print(f"\nAudio downloaded: {audio_file}")

    # Transcribe audio
    transcript, transcript_file = transcribe_audio(audio_file, save_path)
    print(f"Transcription completed: {transcript_file}")

    # Summarize transcription
    summary = summarize_text(transcript, yt.title, yt.author , save_path)
    print("\nSummary:\n", summary, "\n")

if __name__ == "__main__":
    main()
