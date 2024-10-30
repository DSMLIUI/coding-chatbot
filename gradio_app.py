import gradio as gr
from ollama_chat import OllamaChat


def chat_with_file(message, history, file):
    chat_bot = OllamaChat()

    # Restore chat history
    for human, assistant in history:
        chat_bot.add_message("user", human)
        chat_bot.add_message("assistant", assistant)

    # Handle file if provided
    if file:
        file_content = file.decode('utf-8')
        response = chat_bot.analyze_code(file_content, message)
    else:
        # Regular chat without file
        chat_bot.add_message("user", message)
        response = chat_bot.analyze_code("", message)

    # Return the message pair format that Gradio expects: [user_message, assistant_response]
    history.append((message, response))
    return history


# Create the Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        label="Chat with Code Assistant",
        height=600
    )

    with gr.Row():
        txt = gr.Textbox(
            label="Type your message",
            placeholder="Ask me about your code...",
            scale=4
        )
        file_upload = gr.File(
            label="Upload Code File (optional)",
            file_types=[".py", ".js", ".java", ".cpp", ".txt"],
            scale=1
        )

    clear = gr.ClearButton([txt, chatbot, file_upload])

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
