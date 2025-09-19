# import os, config
# from pydantic import BaseModel

from sparrow.tool.websearch_tool import WebsearchResults
sparrow_websearch = WebsearchResults()

from sparrow.tool.finsearch_tool import FinsearchResults
sparrow_finsearch = FinsearchResults()

from sparrow.tool.vectorsearch_tool import VectorsearchResults
sparrow_vectorsearch = VectorsearchResults()

from sparrow.tool.embed_tool import EmbedResults
sparrow_embed = EmbedResults()

from sparrow.tool.ops_tool import OpsCostsResults
ops_costs = OpsCostsResults()

from sparrow.tool.pro_tool import ProCostsResults
pro_costs = ProCostsResults()

from sparrow.tool.fin_tool import FinCostsResults
fin_costs = FinCostsResults()









'''---- Tavily ----
from langchain_community.tools.tavily_search import TavilySearchResults
os.environ['TAVILY_API_KEY'] = config.TAVILY_API_KEY
tavily_search = TavilySearchResults()
tavily_search.name = "tavily_search"
tavily_search.description = "Returns a list of relevant document snippets for a text query"
class TavilySearchInput(BaseModel):
    query: str = Field(description="Query to search the internet with.")
tavily_search.args_schema = TavilySearchInput
'''


'''---- REPL ----
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="Executes python code and returns the result. The code runs in a static sandbox.",
    func=python_repl.run,
)
repl_tool.name = "python_interpreter"
class ToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")
repl_tool.args_schema = ToolInput
'''

