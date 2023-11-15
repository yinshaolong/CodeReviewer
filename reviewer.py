
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
    parser.add_argument("-m", default = '3',type=str, help="determines the gpt model the user would like to use")
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
            messages.append(message)
    return messages

def generate_reviewed_code(messages):
    args = parse_args()
    closing_index = messages.rfind("```")
    opening_index = messages.index("```")
    reviewed_code = messages[opening_index + 3:closing_index]
    file_path = os.path.abspath(args.f)
    file_name, file_extension = os.path.splitext(file_path)

    with open(f"{file_name}_reviewed{file_extension}", "w") as f:
        f.write(reviewed_code)
def main():
    messages = generate_code_review()
    generate_reviewed_code(messages)
    print(messages)
if __name__ == "__main__":
    main()