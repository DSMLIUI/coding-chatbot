from openai import OpenAI


class OllamaChat:
    def __init__(self, model: str = "qwen2.5-coder"):
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
        self.add_message("user", prompt)

        if file_content:
            self.add_message(
                "user", f"Here is the code to analyze:\n```{file_lang}\n{file_content}```")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        assistant_response = response.choices[0].message.content
        self.add_message("assistant", assistant_response)

        return assistant_response

    def clear_history(self):
        self.messages = [self.messages[0]]  # Keep only the system message
