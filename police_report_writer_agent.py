import ollama

with open("report_writing_standards.md", "r") as file:
    report_writing_standards = file.read()

response = ollama.chat(model="llama3", messages=[
  {
    "role": "user",
    "content": "Hello, world!"
  }
])
print(response)
