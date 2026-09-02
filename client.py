import os
from openai import OpenAI
from dotenv import load_dotenv

# pip install openai python-dotenv

load_dotenv()  # reads AI_API_KEY from a local .env file (not committed to git)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",  # remove this line if using a real OpenAI key
    api_key=os.environ["AI_API_KEY"],
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)
