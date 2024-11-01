# Download Ollama
curl https://ollama.ai/install.sh | sh

# Get ollama running
mkdir -p ~/log
ollama serve > ~/log/ollama.log 2> ~/log/ollama.err &

# Download the model
ollama pull qwen2.5-coder

# Setup Environment
# python -m venv .venv # Uncomment if running locally
# source .venv/bin/activate # Uncomment if running locally

pip install -r requirements.txt