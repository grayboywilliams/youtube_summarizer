
# YouTube Summarizer

This tool will take a YouTube URL and return a summary of the video.

It performs 3 steps:
1. download the audio of the video
2. transcribe the audio
3. summarize the transcription.

Each of these are stored in a local directory created for the video.\
Once the audio or transcription have been saved, they aren't regenerated on subsequent calls, but the summary is.

https://github.com/grayboywilliams/youtube_summarizer/assets/43975768/a7cc5ef8-873d-493e-a19e-e40b5cde6a9f

## Installation

Before using, make sure to install the required packages:

```shell
pip install -r requirements.txt
```

And be sure that your OpenAI API Key is saved to the environment variable `OPENAI_API_KEY`.

## Usage

To run the tool, follow these steps:

### Start the Application

Run the main script:

```shell
python app.py
```

First prompt will ask for the YouTube URL.\
Second prompt will ask for the max tokens (or default).
