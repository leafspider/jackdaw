from typing import Dict, List, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class OpsCostsInput(BaseModel):
    text: str = Field(description="should be a chunk of text")

class OpsCostsResults(BaseTool):

    name: str = "ops_costs"
    description: str = (
        "An api tool for querying operational costs data. "
        "Input should be a text query."
    )
    args_schema: Type[BaseModel] = OpsCostsInput

    def _run(
            self,
            text: str,
    ) -> Union[List[Dict], str]:
        try:            
            print(f"TOOL: ops_costs with: {text}")
            txt = "Over the past two months factory labour costs have increased by 7%, the cost of parts has gone down by 2%, and building rental costs have not changed. "
            return [{"results":txt}]
        except Exception as e:
            return repr(e)
