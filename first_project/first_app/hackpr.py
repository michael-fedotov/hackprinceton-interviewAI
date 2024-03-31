import requests
import os
from os import listdir

# Constants
ENDPOINT_COMPLETIONS = "https://api.openai.com/v1/chat/completions"

# Global variables
API_KEY = input("Enter API key:")
job_role = input("What job title are you applying for?")

job_description = input("What is it's job description?")

prompt = f"Give 5 behavioural interview questions for the role of {job_role} with the following job description: {job_description}. Answer them too. Questions in single quotes and Answers in double quotes"
GPT3 = "gpt-3.5-turbo"
    
# Sends the request to the API
response = requests.post(
    ENDPOINT_COMPLETIONS,
        json={
            "model": GPT3,
            "messages": [{"role": "user", "content": prompt}]
        },
        headers={
            "Content-type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
)
    
# Extracts the data from the response
data = response.json()

sections = data["choices"][0]["message"]["content"].split('\n\n')  # Assuming each section is separated by two newline characters
qa_pairs = {}
for section in sections:
    if section.strip():  # Ignore empty sections
        lines = section.split('\n')
        question = lines[0].strip()
        answer = '\n'.join(lines[1:]).strip()
        qa_pairs[question] = answer


for question, answer in qa_pairs.items():
    print("Question:", question)
    print("Answer:", answer)
    print()
    