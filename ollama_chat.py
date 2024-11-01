from openai import OpenAI


class OllamaChat:
    def __init__(self, model: str = "qwen2.5-coder"):
        """
        Initializes an OllamaChat instance with the specified model and OpenAI client.

        The OllamaChat class is used to manage a conversation with an AI assistant,
        including adding messages to the conversation history and generating responses from the assistant.

        Args:
            model (str, optional): The name of the model to use for the AI assistant. Defaults to "qwen2.5-coder".
        """
        self.model = model
        self.client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',  # required, but unused
        )
        self.messages = [
            {
                "role": "system",
                "content": "You are a code analysis assistant."
            }
        ]

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def analyze_code(self, file_content: str, prompt: str, file_lang: str):
        """
        Analyzes the provided code and generates a response from the AI assistant.

        Args:
            file_content (str): The content of the code file to be analyzed.
            prompt (str): The prompt or question to be asked about the code.
            file_lang (str): The programming language of the code file.

        Returns:
            str: The response from the AI assistant.
        """
        self.add_message("user", prompt)

        # Create prompt with file content
        if file_content:
            self.add_message(
                "user", f"Here is the code to analyze:\n```{file_lang}\n{file_content}```")

        # Get response from LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        assistant_response = response.choices[0].message.content
        self.add_message("assistant", assistant_response)

        return assistant_response

    def clear_history(self):
        self.messages = [self.messages[0]]  # Keep only the system message
