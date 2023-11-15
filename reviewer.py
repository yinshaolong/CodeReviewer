
import openai
from dotenv import load_dotenv
import os
import argparse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

model = {3: "gpt-3.5-turbo", 4: "gpt-4-1106-preview"}

def parse_args():
    parser = argparse.ArgumentParser(description="Conversation with a chatbot")
    parser.add_argument("-m", default = '4',type=str, help="determines the gpt model the user would like to use")
    parser.add_argument("-f", default = "node_reviewed_code.js", type=str, help="determines the file the user would like to review")
    return parser.parse_args()

def get_file_contents(file):
    prompt_string = ['"""']
    with open(file, "r") as f:
        prompt_string.append(f.read())
    prompt_string.append('"""')
    return "".join(prompt_string)

def get_prompt(file="prompt.txt"):
    return get_file_contents(file).replace("\n", "")

def chat(prompt = get_prompt()):
    args = parse_args()
    for data in client.chat.completions.create(
    model = model[int(args.m)],
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Code review the following file: {get_file_contents(args.f)}"}
    ],
    stream = True,
    ):
        yield data.choices[0].delta.content

def generate_code_review():
    reply = chat()
    messages = []
    with open("review.txt", "w") as f:
        f.write('')
    for message in reply:
        print(message, end="", flush=True)
        with open("review.txt", "a") as f:
            f.write(message) if message != None else f.write("")
    return "".join(messages)

def main():
    messages = generate_code_review()
if __name__ == "__main__":
    main()