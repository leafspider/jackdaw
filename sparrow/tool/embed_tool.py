from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from sparrow.toolkit.embed.embedder import Embedder


class EmbedInput(BaseModel):

    text: str = Field(description="should be a chunk of text")


class EmbedResults(BaseTool):

    name: str = "sparrow_embed"
    description: str = (
        "An api tool for extracting word embedding vectors from text. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = EmbedInput

    def _run(
            self,
            text: str,
    ) -> Union[List[Dict], str]:
        try:            
            embedder = Embedder()
            results = embedder.create_embedding(text)
            return results
        except Exception as e:
            return repr(e)

