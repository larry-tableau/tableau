import openai
import os
from tabpy.tabpy_tools.client import Client

client = Client('http://localhost:9004/')

def chat_gpt_query(prompt):
    try:
        openai_client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            temperature=0.0,
            max_tokens=150,
            messages=[
                {"role": "system", "content": "You are TableauAI a powerful AI trained in Tableau calculations."},
                {"role": "system", "content": "Only perform what is asked of you.  Do NOT provide explanations or suggestions. Never use punctuations"},
                {"role": "system", "content": "Ensure groups, labels and other naming conventions you use are identical."},
                {"role": "user", "content": str(prompt)}
            ]
        )
        message = response.choices[0].message.content
        print(message)
        return message
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}"
# chat_gpt_query(prompt)
client.deploy('chat_gpt_query', chat_gpt_query, 'Queries ChatGPT using OpenAI API', override=True)