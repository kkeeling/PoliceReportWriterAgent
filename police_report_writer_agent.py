import ollama

report_writing_standards = ""

try:
    with open("report_writing_standards.md", "r") as file:
        report_writing_standards = file.read()
    print("Writing standards loaded successfully.")
except Exception as e:
    print(f"Failed to load writing standards: {e}")

# set the prompt for the first agent
prompt_01 = f'{report_writing_standards} #### from these standards, identify the most important rules to follow when writing a police report.'

response = ollama.chat(model="llama3", messages=[
  {
    "role": "user",
    "content": "Hello, world!"
  }
])
print(response)
