# deploy_both.py
import sys
sys.path.append('/Users/Dev/tabpy')  # Add path to find your modules

from tabpy.tabpy_tools.client import Client

# Import both functions
from chat_gpt_query import chat_gpt_query
from sentiment_analysis import sentiment_analysis

# Create client
client = Client('http://localhost:9004/')

# Deploy both functions
print("Deploying chat_gpt_query...")
client.deploy('chat_gpt_query', chat_gpt_query, 'Queries ChatGPT using OpenAI API', override=True)

print("Deploying sentiment_analysis...")
client.deploy('sentiment_analysis', sentiment_analysis, 'Returns sentiment score of text', override=True)

print("Both functions deployed successfully!")