# This program is trying to ask ChatGPT to tide the file

import subprocess
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
terminal_prompt = "chatgpt@raspberrypi:~/Downloads/documents $ "
current_working_dir = "/home/iwmain/Downloads/documents"
with open("prompt.txt", "r", encoding="utf-8") as file:
    messages = [{"role": "system", "content": file.read()},
                {"role": "user", "content": terminal_prompt}]


def run_command(command: list):
    # Only limited commands will be allowed, for safety concern
    if command[0] not in ["tree", "ls", "cp", "mv", "find", "mkdir", "sort", "uniq", "grep", "du", "df", "pwd"]:
        return "Access denied."
    for c in command:
        if c.startswith(("/", "..")):
            return "Access denied."
    try:
        result = subprocess.run(command, cwd=current_working_dir, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        return result.stdout
    except Exception as e:
        print(command)
        return str(e)


def request():
    completion = client.chat.completions.create(messages=messages, model="gpt-4")
    return completion.choices[0].message.content


def clip_message(text: str):
    # make sure that each response contains no more than 60 lines
    if text.count('\n') <= 60:
        return text
    l_index = 0
    for _ in range(30):
        l_index = text.find('\n', l_index+1)
    r_index = len(text)
    for _ in range(30):
        r_index = text.rfind('\n', 0, r_index)
    return text[:l_index] + "\n\n(abridged content)\n\n" + text[r_index:]


def remove_redundant_messages():
    while len(messages) > 20:
        for _ in range(2):
            messages.pop(1)


def test():
    print("-++" * 50)
    temp = clip_message("-++"*50)
    print(temp)



if __name__ == '__main__':
    while True:
        command = request()
        result = run_command(command.split())
        result = clip_message(result)
        result = result + "\n" + terminal_prompt
        messages.append({"role": "assistant", "content": command})
        messages.append({"role": "user", "content": result})
        remove_redundant_messages()
        for m in messages[-2:]:
            print()
            print(m["role"])
            print(m["content"])
        input()
