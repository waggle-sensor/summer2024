import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

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

def main():
    filename = 'caption.txt'
    sentence = read_file(filename)

    sentiment = analyze_sentiment(sentence)
    print(f"Sentiment: {sentiment}")

    negative_words = ["flame", "car crash", ""]
    if check_negative_words(sentence, negative_words):
        print("Alert: negative sentiment.")
    else:
        print("No alert.")

if __name__ == "__main__":
    main()
