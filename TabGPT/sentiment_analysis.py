# sentiment_analysis.py - ONLY the function
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download only if not already available
try:
    # Test if vader_lexicon is available
    SentimentIntensityAnalyzer()
except LookupError:
    # Download only if needed
    nltk.download('vader_lexicon', quiet=True)

def sentiment_analysis(text):
    """Returns sentiment score of text"""
    try:
        # Create a SentimentIntensityAnalyzer object
        sia = SentimentIntensityAnalyzer()
        
        # Get the sentiment scores for the text
        sentiment = sia.polarity_scores(str(text))
        
        return sentiment
    except Exception as e:
        return {"error": str(e)}