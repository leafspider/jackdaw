from typing import Dict, List, Optional, Type, Union
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
# from sparrow.tool.websearch.websearch_api_wrapper import WebsearchAPIWrapper
from langchain_core.utils import get_from_dict_or_env

# import json
from sparrow.toolkit.search.google_search import Websearch
# from sparrow.toolkit.search.duck_search import Websearch
# from pydantic import BaseModel, Extra, SecretStr, root_validator
from pydantic import BaseModel, SecretStr, model_validator
# import aiohttp


SPARROW_API_URL = "https://api.enodes.com"
SPARROW_API_KEY = "bobbins"

class WebsearchInput(BaseModel):
    """Input for the Websearch tool."""

    query: str = Field(description="search query to look up")


class WebsearchResults(BaseTool):
    """Tool that queries the Websearch and gets back json."""

    name: str = "sparrow_websearch"
    description: str = (
        "A search engine optimized for comprehensive, accurate, and trusted results. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    # api_wrapper: WebsearchAPIWrapper = Field(default_factory=WebsearchAPIWrapper)
    max_results: int = 5
    args_schema: Type[BaseModel] = WebsearchInput
    
    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            # return self.api_wrapper.results(
            #     query,
            #     self.max_results,
            # )    
            ws = Websearch()
            return ws.fetch_results_json(query, num_results=5)
        except Exception as e:
            return repr(e)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            # return await self.api_wrapper.results_async(
            #     query,
            #     self.max_results,
            # )        
            ws = Websearch()
            return await ws.fetch_results_json_async(query, num_results=5)
        except Exception as e:
            return repr(e)

# class WebsearchAPIWrapper(BaseModel):
#     """Wrapper for Search API."""

#     sparrow_api_key: SecretStr

#     class Config:
#         """Configuration for this pydantic object."""

#         extra = 'forbid'

# #     @root_validator(pre=True)
#     # @model_validator(mode="wrap")
#     # def validate_environment(cls, values: Dict) -> Dict:
#     #     """Validate that api key and endpoint exists in environment."""
#     #     sparrow_api_key = get_from_dict_or_env(
#     #         values, "sparrow_api_key", "SPARROW_API_KEY"
#     #     )
#     #     values["sparrow_api_key"] = sparrow_api_key

#     #     return values

#     def raw_results(
#         self,
#         query: str,
#         max_results: Optional[int] = 5,
#         search_depth: Optional[str] = "advanced",
#         include_domains: Optional[List[str]] = [],
#         exclude_domains: Optional[List[str]] = [],
#         include_answer: Optional[bool] = False,
#         include_raw_content: Optional[bool] = False,
#         include_images: Optional[bool] = False,
#     ) -> Dict:
#         params = {
#             "api_key": self.sparrow_api_key.get_secret_value(),
#             "query": query,
#             "max_results": max_results,
#             "search_depth": search_depth,
#             "include_domains": include_domains,
#             "exclude_domains": exclude_domains,
#             "include_answer": include_answer,
#             "include_raw_content": include_raw_content,
#             "include_images": include_images,
#         }
#         '''
#         response = requests.post(
#             # type: ignore
#             f"{SPARROW_API_URL}/search",
#             json=params,
#         )
#         response.raise_for_status()
#         return response.json()
#         '''
#         gs = Websearch()
#         return gs.fetch_results_json(query, num_results=5)


#     def results(
#         self,
#         query: str,
#         max_results: Optional[int] = 5,
#         search_depth: Optional[str] = "advanced",
#         include_domains: Optional[List[str]] = [],
#         exclude_domains: Optional[List[str]] = [],
#         include_answer: Optional[bool] = False,
#         include_raw_content: Optional[bool] = False,
#         include_images: Optional[bool] = False,
#     ) -> List[Dict]:
#         """Run query through Websearch and return metadata.

#         Args:
#             query: The query to search for.
#             max_results: The maximum number of results to return.
#             search_depth: The depth of the search. Can be "basic" or "advanced".
#             include_domains: A list of domains to include in the search.
#             exclude_domains: A list of domains to exclude from the search.
#             include_answer: Whether to include the answer in the results.
#             include_raw_content: Whether to include the raw content in the results.
#             include_images: Whether to include images in the results.
#         Returns:
#             query: The query that was searched for.
#             follow_up_questions: A list of follow up questions.
#             response_time: The response time of the query.
#             answer: The answer to the query.
#             images: A list of images.
#             results: A list of dictionaries containing the results:
#                 title: The title of the result.
#                 url: The url of the result.
#                 content: The content of the result.
#                 score: The score of the result.
#                 raw_content: The raw content of the result.
#         """  # noqa: E501
#         raw_search_results = self.raw_results(
#             query,
#             max_results=max_results,
#             search_depth=search_depth,
#             include_domains=include_domains,
#             exclude_domains=exclude_domains,
#             include_answer=include_answer,
#             include_raw_content=include_raw_content,
#             include_images=include_images,
#         )
#         return self.clean_results(raw_search_results["results"])


#     async def raw_results_async(
#         self,
#         query: str,
#         max_results: Optional[int] = 5,
#         search_depth: Optional[str] = "advanced",
#         include_domains: Optional[List[str]] = [],
#         exclude_domains: Optional[List[str]] = [],
#         include_answer: Optional[bool] = False,
#         include_raw_content: Optional[bool] = False,
#         include_images: Optional[bool] = False,
#     ) -> Dict:
#         """Get results from the Search API asynchronously."""

#         # Function to perform the API call
#         async def fetch() -> str:
#             params = {
#                 "api_key": self.sparrow_api_key.get_secret_value(),
#                 "query": query,
#                 "max_results": max_results,
#                 "search_depth": search_depth,
#                 "include_domains": include_domains,
#                 "exclude_domains": exclude_domains,
#                 "include_answer": include_answer,
#                 "include_raw_content": include_raw_content,
#                 "include_images": include_images,
#             }
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(f"{SPARROW_API_URL}/search", json=params) as res:
#                     if res.status == 200:
#                         data = await res.text()
#                         return data
#                     else:
#                         raise Exception(f"Error {res.status}: {res.reason}")

#         results_json_str = await fetch()
#         return json.loads(results_json_str)


#     async def results_async(
#         self,
#         query: str,
#         max_results: Optional[int] = 5,
#         search_depth: Optional[str] = "advanced",
#         include_domains: Optional[List[str]] = [],
#         exclude_domains: Optional[List[str]] = [],
#         include_answer: Optional[bool] = False,
#         include_raw_content: Optional[bool] = False,
#         include_images: Optional[bool] = False,
#     ) -> List[Dict]:
#         results_json = await self.raw_results_async(
#             query=query,
#             max_results=max_results,
#             search_depth=search_depth,
#             include_domains=include_domains,
#             exclude_domains=exclude_domains,
#             include_answer=include_answer,
#             include_raw_content=include_raw_content,
#             include_images=include_images,
#         )
#         return self.clean_results(results_json["results"])


#     def clean_results(self, results: List[Dict]) -> List[Dict]:
#         """Clean results from Search API."""
#         clean_results = []
#         for result in results:
#             clean_results.append(
#                 {
#                     "url": result["url"],
#                     "content": result["content"],
#                 }
#             )
#         return clean_results
    
# class WebsearchAnswer(BaseTool):
#     """Tool that queries the Websearch API and gets back an answer."""

#     name: str = "sparrow_answer"
#     description: str = (
#         "A search engine optimized for comprehensive, accurate, and trusted results. "
#         "Useful for when you need to answer questions about current events. "
#         "Input should be a search query. "
#         "This returns only the answer - not the original source data."
#     )
#     api_wrapper: WebsearchAPIWrapper = Field(default_factory=WebsearchAPIWrapper)
#     args_schema: Type[BaseModel] = WebsearchInput

#     def _run(
#             self,
#             query: str,
#             run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> Union[List[Dict], str]:
#         """Use the tool."""
#         try:
#             return self.api_wrapper.raw_results(
#                 query,
#                 max_results=5,
#                 include_answer=True,
#                 search_depth="basic",
#             )["answer"]
#         except Exception as e:
#             return repr(e)

#     async def _arun(
#             self,
#             query: str,
#             run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
#     ) -> Union[List[Dict], str]:
#         """Use the tool asynchronously."""
#         try:
#             result = await self.api_wrapper.raw_results_async(
#                 query,
#                 max_results=5,
#                 include_answer=True,
#                 search_depth="basic",
#             )
#             return result["answer"]
#         except Exception as e:
#             return repr(e)