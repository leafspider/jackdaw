from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class FinCostsInput(BaseModel):
    text: str = Field(description="should be a chunk of text")

class FinCostsResults(BaseTool):

    name: str = "fin_costs"
    description: str = (
        "An api tool for querying finncial costs data. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = FinCostsInput

    def _run(
            self,
            text: str,
    ) -> Union[List[Dict], str]:
        try:            
            print(f"TOOL: fin_costs with: {text}")
            txt = "Over the past two months interest rates have increased by 0.2%, and our legal partners have increased their fees for regulatory compliance services by 1%. "
            return [{"results":txt}]
        except Exception as e:
            return repr(e)

