import ollama
from colorama import Fore, Style

report_writing_standards = ""

try:
    with open("report_writing_standards.md", "r") as file:
        report_writing_standards = file.read()
    print("Writing standards loaded successfully.")
except Exception as e:
    print(f"Failed to load writing standards: {e}")

# set the prompt for the first agent
prompt_01 = f'{report_writing_standards} #### from these standards, identify the most important rules to follow when writing a police report.'

print(f"{Fore.WHITE}{prompt_01}{Style.RESET_ALL}")
print("\n\n")
print(f"{Fore.GREEN}Generating a response...{Style.RESET_ALL}")

response = ollama.chat(model="llama3", messages=[
  {
    "role": "user",
    "content": "Hello, world!"
  }
])
print(response)
