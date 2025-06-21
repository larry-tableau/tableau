import chat_gpt_query
from tabpy.tabpy_tools.client import Client

client = Client('http://localhost:9004/')

with open('/Users/Dev/tabpy/chat_gpt_query.py', 'r') as file:
    tabpy_script = file.read()

client.deploy('chat_gpt_query', chat_gpt_query, 'Queries ChatGPT using OpenAI API', override=True)