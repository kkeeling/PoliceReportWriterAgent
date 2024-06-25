import ollama
from colorama import Fore, Style
import sys
import os
import subprocess
import whisper
from pydub import AudioSegment

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
    with open("report.txt", "w") as report_file:
        report_file.write(response["message"]["content"])
    print("Response written to report.txt")

def transcribe_audio(audio_file_path):
    # Check if the file exists
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"The file {audio_file_path} does not exist.")

    # Get the file extension
    _, file_extension = os.path.splitext(audio_file_path)

    # If the file is not in WAV format, convert it using FFmpeg
    if file_extension.lower() != '.wav':
        output_path = audio_file_path.rsplit('.', 1)[0] + '.wav'
        
        try:
            # Use FFmpeg to convert the audio to WAV format
            subprocess.run(['ffmpeg', '-i', audio_file_path, '-acodec', 'pcm_s16le', '-ar', '16000', output_path], 
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise RuntimeError("Error occurred while converting the audio file.")
        
        audio_file_path = output_path

    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio
    result = model.transcribe(audio_file_path)

    # Clean up the temporary WAV file if it was created
    if output_path and os.path.isfile(output_path):
        os.remove(output_path)

    # Return the transcription
    return result["text"]

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
