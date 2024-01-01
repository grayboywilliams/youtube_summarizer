
# YouTube Summarizer

This tool will take a YouTube URL and max tokens as inputs and return a summary of the video within the token limit.

It performs 3 steps:
1. download the audio of the video
2. transcribe the audio
3. summarize the transcription.

Each of these are stored in a local directory created for the video.
Once the audio or transcription have been saved, they aren't regenerated on subsequent calls, but the summary is.

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

First prompt will ask for the YouTube URL.
Second prompt will ask for the max tokens (or default).
