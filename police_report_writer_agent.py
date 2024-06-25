import ollama
from colorama import Fore, Style
import sys
import speech_recognition as sr

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
    prompt = f'{report_writing_standards} #### Create a report based on the transcript provided. <transcript>{transcript}</transcript>'

    print(f"{Fore.RED}<agent-01> Prompt: {prompt}{Style.RESET_ALL}")
    print("\n\n")
    print(f"{Fore.GREEN}<agent-01> Generating a response...{Style.RESET_ALL}")

    # get the response from the first agent
    response = ollama.chat(model="llama3", messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": prompt
      }
    ])
    print(response)

def transcribe_audio(audio_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        # Read the audio data
        audio = recognizer.record(source)

    try:
        # Perform speech recognition using Google Speech Recognition
        transcription = recognizer.recognize_google(audio)
        return transcription
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from speech recognition service; {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python police_report_writer_agent.py <audio_file_path>")
        exit(1)
    
    audio_file_path = sys.argv[1]
    transcript = transcribe_audio(audio_file_path)
    print("Transcription completed successfully.")
    run_report_writer_agent(transcript)

if __name__ == "__main__":
    main()
