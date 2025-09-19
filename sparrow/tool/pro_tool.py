from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class ProCostsInput(BaseModel):
    text: str = Field(description="should be a chunk of text")

class ProCostsResults(BaseTool):

    name: str = "pro_costs"
    description: str = (
        "An api tool for querying promotional costs data. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = ProCostsInput

    def _run(
            self,
            text: str,
    ) -> Union[List[Dict], str]:
        try:            
            print(f"TOOL: pro_costs with: {text}")
            txt = "Over the past two months subscription rates have increased by 2%, average subscription value has fallen by 3%. "
            return [{"results":txt}]
        except Exception as e:
            return repr(e)

