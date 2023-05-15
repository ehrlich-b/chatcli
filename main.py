import os
import requests
import json
import argparse
import sys
import signal
from dotenv import load_dotenv
import openai

load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")

messages = []


load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")
openai.api_key = API_KEY  # Set the API key for the OpenAI library

messages = []

def performRequestWithStreaming(model, messages):
    reqBody = {
        "model": model,
        "messages": messages,
        "stream": True,
    }
    response = openai.ChatCompletion.create(**reqBody)  # Use OpenAI library to make the API call
    response_message = ""
    try:
        for chunk in response:
            if 'choices' in chunk and 'delta' in chunk['choices'][0] and 'content' in chunk['choices'][0]['delta']:
                message_chunk = chunk['choices'][0]['delta']['content']
                print(message_chunk, end="", flush=True)
                response_message += message_chunk
    except KeyboardInterrupt:
        # Handle Ctrl+C press
        pass
    print("\n")
    return response_message.strip()

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument("-4", "--gpt4", action="store_true", help="Use GPT-4 instead of default GPT-3.5-turbo")
    args = parser.parse_args()

    model = "gpt-4" if args.gpt4 else "gpt-3.5-turbo" # Set the model based on the command line argument
    print("Using model: " + model)
    while True:
        try:
            text = input("Person> ")
            print("GPT> ", end="")
            messages.append({"role": "user", "content": text})
            response = performRequestWithStreaming(model, messages)
            messages.append({"role": "system", "content": response})
        except EOFError:
            break
