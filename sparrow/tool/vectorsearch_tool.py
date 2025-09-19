from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from sparrow.toolkit.db.vectordb import VectorDb
from sparrow.toolkit.embed.embedder import Embedder


class VectorsearchInput(BaseModel):

    query: str = Field(description="should be a text query")


class VectorsearchResults(BaseTool):

    name: str = "sparrow_vectorsearch"
    description: str = (
        "An API tool for contextual information. "
        "Useful for finding up-to-date information about context. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = VectorsearchInput

    def _run(
            self,
            query: str
    ) -> Union[List[Dict], str]:
        try:
            db = VectorDb()            
            db.connect()

            embedder = Embedder()
            vector = embedder.create_embedding(query)
            
            # doc_id = db.insert(
            #     text=query, 
            #     embedding=vector
            # )
            
            data = {}
            # rows = db.search_by_id(doc_id, num_results=10)
            rows = db.search_by_embedding(vector)
            for row in rows:
                id = row[0]
                # text = db.fetch_text(id)[:100]
                val = db.select(id, db.table, {'id', db.text_column})
                data.put(val[0][0], val[0][1])
                print(val)            

            print(data)

            return data #fs.fetch_json(query)
        except Exception as e:
            return repr(e)

