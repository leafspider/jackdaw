from mem0 import Memory
import os


os.environ['OPENAI_API_KEY'] = os.environ['COHERE_API_KEY1']

# Configuration to use local Neo4j instance for graph memory storage
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama2",
            "ollama_base_url": "http://localhost:11434", 
            "temperature": 0.2,
            "max_tokens": 1024,
        }
    },
    # "embedder": {
    #     "provider": "huggingface",
    #     "config": {
    #         "model": "BAAI/bge-small-en-v1.5",
    #         "huggingface_base_url": os.environ['EMBEDDING_PROTOCOL'] + "://" + os.environ['EMBEDDING_HOST'] + ":" + os.environ['EMBEDDING_PORT'] + "/embed",
    #         "embedding_dims": 1024           # Use correct dimension for your chosen model
    #     },
    # },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "ollama_base_url": "http://localhost:11434", 
            "embedding_dims": 4096           # Use correct dimension for your chosen model
        }
    },
    "enableGraph": True,  # Enable graph memory
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",  # Local Neo4j Bolt URI
            "username": "neo4j",             # Neo4j username, default 'neo4j'
            "password": "password",    # Neo4j password, set your own
        },
    },
    # Optionally configure vector and key-value stores here
    # e.g., vector_store using local in-memory or file-based storage
}

# Initialize the Memory instance with local Neo4j config
memory = Memory.from_config(config_dict=config)

# Example short-term messages
short_term_messages = [
    {"role": "user", "content": "Hi, I enjoy hiking and pizza."},
    {"role": "assistant", "content": "Got it, I will remember your preferences."}
]

# Add short term messages to store (persisted to Neo4j graph)
memory.add(short_term_messages, user_id="user_local_neo4j")

# Search long-term memories relevant to the query
search_results = memory.search(query="What are my interests?", user_id="user_local_neo4j", limit=5)

# Print the retrieved long-term memories from local Neo4j storage
for result in search_results.get("results", []):
    print("Memory:", result["memory"])
