from sparrow.toolkit.embed.embedder import Embedder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def parse_text(text: str) -> list[str]:
    
    embedder = Embedder()
    
    results = embedder.create_embedding(text)


if __name__ == "__main__":
    
    text = "Trout is a wonderfully flavoured fish when it's on your plate. However, when it's in the river it's a voracious predator."
    res: List[str] = parse_text(text)    
    
