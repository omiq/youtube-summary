import sys

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from googleapiclient.discovery import build



# Enter your YouTube api key here:
youtube = build('youtube', 'v3', developerKey="ABCDEFGHIJKLMN")

# Function to summarize the transcript
def summarize_transcript(transcript_text):

    client = OpenAI(
        # Needs API key obv
        api_key="openai_api_key",
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o",  # Use "gpt-4" or "gpt-3.5-turbo" depending on access
        messages=[
            {"role": "system", "content": "You are a teaching assistant that extracts the most important facts, tips and practical steps from video transcripts into intranet articles for busy and distracted executives."},
            {"role": "user", "content": (
                "Process the following transcript and create a balanced article in 'BBC English' focusing on key learnings or takeaways. Always include the actual information as first person teaching the reader how to do something or how to understand something. Phrases such as 'the transcript emphasizes the importance of understanding' will get the assistant into disciplinary difficulties as this is against the instructions given."
                "Never use emdash or endash. Aim for a reading age of 12 due to the distracted nature of the executives. Exclude any promotional content or giveaways:\n\n" + transcript_text
            )}
        ],
        max_tokens=500,  # Adjust based on desired summary length
        temperature=0.5
    )
    return chat_completion.choices[0].message.content



if len(sys.argv) <= 1:
    print("Enter a video ID")
    exit()
else:
    video_id = sys.argv[1]

    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    details = request.execute()

    title = details['items'][0]['snippet']['title']
    channel = details['items'][0]['snippet']['channelId']
    description = details['items'][0]['snippet']['description']

    print(f'{title} {channel}\n')
    print(f'{description}\n\n')


    # Try to get the English transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    if transcript:
        # Combine all parts of the transcript text into one string
        text_transcript = " ".join([i['text'] for i in transcript])

        # Get the summary of the transcript
        summary = summarize_transcript(text_transcript)
        print("\nSummary:\n", summary)
        #print("\Transcript:\n", transcript)
        


