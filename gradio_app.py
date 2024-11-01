import gradio as gr
from ollama_chat import OllamaChat

"""
Handles the chat interaction between the user and the AI assistant,
including the ability to analyze code files provided by the user.

Args:
    message (str): The user's message to the chat assistant.
    history (list): The chat history, represented as a list of (user_message, assistant_response) tuples.
    file (gradio.File): An optional file uploaded by the user, which will be analyzed by the AI assistant.

Returns:
    list: The updated chat history, including the assistant's response to the user's message.
"""


def chat_with_file(message, history, file):

    chat_bot = OllamaChat()

    # Restore chat history
    for human, assistant in history:
        chat_bot.add_message("user", human)
        chat_bot.add_message("assistant", assistant)

    # Handle file if provided
    if file:
        file_content = file.name
        # Get file extension and map to language
        file_extension = file_content.split('.')[-1].lower()
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'java': 'java',
            'cpp': 'cpp',
            'txt': 'text',
            'sh': 'bash'
        }
        file_language = language_map.get(file_extension, 'text')

        with open(file_content, 'r') as f:
            file_content = f.read()
        response = chat_bot.analyze_code(file_content, message, file_language)
    else:
        # Regular chat without file
        chat_bot.add_message("user", message)
        response = chat_bot.analyze_code("", message, "")

    # Return the message pair format that Gradio expects
    history.append((message, response))
    return history


# Create the Gradio interface
"""
Displays a Gradio chatbot interface that allows users to chat with an AI assistant and optionally upload code files for analysis.

The chatbot interface includes:
- A Chatbot widget to display the conversation history
- A Textbox widget for the user to enter their message
- A File upload widget to allow the user to upload a code file
- A ClearButton to reset the chat history and input fields

When the user submits a message or uploads a file, the `chat_with_file` function is called to handle the interaction. This function restores the chat history, analyzes any uploaded code file, and generates a response from the AI assistant. The updated chat history is then returned to be displayed in the Chatbot widget.
"""
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        label="Chat with Code Assistant",
        height=600
    )

    # Chat boxes
    with gr.Row():
        txt = gr.Textbox(
            label="Type your message",
            placeholder="Ask me about your code...",
            scale=4
        )
        file_upload = gr.File(
            label="Upload Code File (optional)",
            file_types=[".py", ".js", ".java", ".cpp", ".txt", ".sh"],
            scale=1
        )
    clear = gr.ClearButton([txt, chatbot, file_upload])

    # What to do when the user presses `Enter`
    txt_msg = txt.submit(
        chat_with_file,
        inputs=[txt, chatbot, file_upload],
        outputs=[chatbot],
        queue=False
    )

    txt_msg.then(lambda: "", None, txt)
    txt_msg.then(lambda: None, None, file_upload)

# Launch the app
if __name__ == "__main__":
    demo.launch()
