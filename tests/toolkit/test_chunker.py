import pytest

from typing import List
import sparrow.toolkit.kgraph.chunker as chunker


def test_chunker():
    text = "Trout is a wonderfully flavoured fish when it's on your plate. However, when it's in the river it's a voracious predator."
    chunks: List[str] = chunker.chunk(text)    
    assert len(chunks) > 0
    assert isinstance(chunks, List)
    assert isinstance(chunks[0].page_content, str)    