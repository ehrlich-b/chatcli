import os
import argparse
import sys
import signal
from dotenv import load_dotenv
import openai
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from rich.live import Live
from rich.markdown import Markdown

load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")

messages = []


load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")
openai.api_key = API_KEY  # Set the API key for the OpenAI library

messages = []

def handle_ctrl_c():
    try:
        input("Click Ctrl+C again to exit, press enter to continue...")
    except KeyboardInterrupt:
        print('\n')
        os._exit(0)  # If Ctrl+C is pressed again, we will exit the program

def performRequestWithStreaming(model, messages):
    reqBody = {
        "model": model,
        "messages": messages,
        "stream": True,
    }
    response = openai.ChatCompletion.create(**reqBody)  # Use OpenAI library to make the API call
    response_message = ""

    # Create a Live context manager for updating the console
    with Live(auto_refresh=False) as live:
        try:
            for chunk in response:
                if 'choices' in chunk and 'delta' in chunk['choices'][0] and 'content' in chunk['choices'][0]['delta']:
                    message_chunk = chunk['choices'][0]['delta']['content']
                    response_message += message_chunk
                    # Update the Live display with the current response_message
                    live.update(Markdown("GPT> " + response_message))
                    live.refresh()  # Manually refresh the display
        except KeyboardInterrupt:
            # Handle Ctrl+C press
            pass
    return response_message.strip()

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    sys.exit(0)

kb = KeyBindings()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument("-4", "--gpt4", action="store_true", help="Use GPT-4 instead of default GPT-3.5-turbo")
    parser.add_argument("-ctrl", "--ctrl", action="store_true", help="Require Ctrl+Enter to send input")
    args = parser.parse_args()

    # Ctrl+Enter to confirm input if -ctrl flag is set
    if args.ctrl:
        @kb.add(Keys.ControlJ)
        def _(event):
            event.current_buffer.validate_and_handle()

    model = "gpt-4" if args.gpt4 else "gpt-3.5-turbo" # Set the model based on the command line argument
    print("Using model: " + model)
    while True:
        try:
            text = prompt('You> ', multiline=args.ctrl, key_bindings=kb)
            messages.append({"role": "user", "content": text})
            response = performRequestWithStreaming(model, messages)
            messages.append({"role": "system", "content": response})
        except KeyboardInterrupt:
            handle_ctrl_c()
        except SystemExit:
            break
