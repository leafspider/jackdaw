from sparrow.agent.model import *
from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class TeamInput(BaseModel):
    text: str = Field(description="should be a chunk of text")

class TeamResults(BaseTool):

    name: str = "team"
    description: str = (
        "An api tool for sending a query to a team. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = TeamInput

    def _run(
            self,
            text: str,
    ) -> Union[List[Dict], str]:
        try:            
            print(f"TOOL: assistant with: {text}")
            txt = "Over the past two months subscription rates have increased by 2%, average subscription value has fallen by 3%. "
            return [{"results":txt}]
        except Exception as e:
            return repr(e)

