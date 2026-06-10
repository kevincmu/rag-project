from langchain_ollama import ChatOllama, OllamaEmbeddings

# Select the qwen3 model and embeddings from Ollama
model = ChatOllama(model="qwen3:8b")
embeddings = OllamaEmbeddings(model="qwen3-embedding:8b")