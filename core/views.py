# views.py

from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def initialize_twilio_client():
    # Initialize Twilio client
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    return client

def make_call():
    try:
        # Initialize Twilio client
        client = initialize_twilio_client()
        
        call = client.calls.create(
            twiml='<Response><Say>Hello there! What do you think about our product.</Say><Record /></Response>',
            to=settings.TO_NUMBER,
            from_=settings.FROM_NUMBER
        )
        
        return call.sid
    
    except Exception as e:
        return str(e)

def fetch_transcript():
    try:

        client = initialize_twilio_client()
        recording_sid = client.recordings.list()[0].sid
        recording = client.recordings(recording_sid).fetch()
        transcript = recording.transcription_text
        
        return transcript
    
    except Exception as e:
        return str(e)

def perform_sentiment_analysis(text):

    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        sentiment_label = 'Positive'
    elif compound_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return sentiment_label

def execution_method(request):
    try:

        call_sid = make_call()
        transcript = fetch_transcript()
        sentiment = perform_sentiment_analysis(transcript)
        
        return JsonResponse({'call_sid': call_sid, 'transcript': transcript, 'sentiment': sentiment})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
