curl https://ollama.ai/install.sh | sh

mkdir -p ~/log
ollama serve > ~/log/ollama.log 2> ~/log/ollama.err &
# preload the model
curl http://localhost:11434/api/generate -d '{"model": "qwen2.5-coder"}'

ollama pull qwen2.5-coder