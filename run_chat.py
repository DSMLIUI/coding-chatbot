from ollama_chat import OllamaChat
# Create the chat instance
chat = OllamaChat()

# Read the file
with open('path/to/your/file.py', 'r') as file:
    file_content = file.read()

# Analyze the code
result = chat.analyze_code(
    file_content,
    "Please review this code and suggest improvements"
)
print(result)
