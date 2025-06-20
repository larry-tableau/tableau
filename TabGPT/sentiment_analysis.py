# Importing necessary libraries
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Downloading the vader_lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Defining the sentiment analysis function
def sentiment_analysis(text):
    # Create a SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Get the sentiment scores for the text
    sentiment = sia.polarity_scores(text)

    return sentiment

# Register the function for TabPy
from tabpy.tabpy_tools.client import Client
connection = Client('http://localhost:9004/')
connection.deploy('sentiment_analysis', sentiment_analysis, 'Returns sentiment score of text', override=True)
