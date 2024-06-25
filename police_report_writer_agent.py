import ollama
from colorama import Fore, Style

def run_report_writer_agent(transcript):
    system_prompt = ""
    report_writing_standards = ""

    try:
        with open("system_prompt.md", "r") as file:
            system_prompt = file.read()
        print("System prompt loaded successfully.")
    except Exception as e:
        print(f"Failed to load system prompt: {e}")
        exit(1)

    try:
        with open("report_writing_standards.md", "r") as file:
            report_writing_standards = file.read()
        print("Writing standards loaded successfully.")
    except Exception as e:
        print(f"Failed to load writing standards: {e}")
        exit(1)

    # set the prompt for the first agent
    prompt = f'{report_writing_standards} #### from these standards, identify the most important rules to follow when writing a police report.'

    print(f"{Fore.RED}<agent-01> Prompt: {prompt}{Style.RESET_ALL}")
    print("\n\n")
    print(f"{Fore.GREEN}<agent-01> Generating a response...{Style.RESET_ALL}")

    # get the response from the first agent
    response = ollama.chat(model="llama3", messages=[
      {
        "role": "user",
        "content": prompt
      }
    ])
    print(response)
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python police_report_writer_agent.py <audio_file_path>")
        exit(1)
    
    audio_file_path = sys.argv[1]
    run_report_writer_agent(audio_file_path)

if __name__ == "__main__":
    main()
