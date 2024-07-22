import gradio as gr
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def analyze_sentiment(sentence):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(sentence)
    if sentiment_scores['compound'] > 0:
        sentiment = "positive"
    elif sentiment_scores['compound'] < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment

def check_negative_words(sentence, negative_words):
    for word in negative_words:
        if word in sentence.lower():
            return True
    return False

def analyze_text(text):
    sentiment = analyze_sentiment(text)
    negative_words = ["flame", "car crash", ""]
    alert = check_negative_words(text, negative_words)
    alert_message = "Alert: negative sentiment." if alert else "No alert."
    return sentiment, alert_message

iface = gr.Interface(
    fn=analyze_text,
    inputs="text",
    outputs=["text", "text"],
    title="Sentiment Analysis",
    description="Analyze the sentiment of a given text and check for specific negative words."
)

if __name__ == "__main__":
    iface.launch()
