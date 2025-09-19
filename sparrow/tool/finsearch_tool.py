from typing import Dict, List, Optional, Type, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from sparrow.toolkit.search.fin_search import YahooFinanceSearch
from datetime import date


class FinsearchInput(BaseModel):

    ticker: str = Field(description="should be a ticker symbol")
    start_date: date = Field(description="should be a date in ISO format")
    end_date: date = Field(description="should be a date in ISO format")


class FinsearchResults(BaseTool):

    name: str = "sparrow_finsearch"
    description: str = (
        "An API tool for searching corporate financial data. "
        "Only useful for finding historical company stock prices. "
        "Input should be a ticker symbol, a start date and an end date."
    )
    args_schema: Type[BaseModel] = FinsearchInput

    def _run(
            self,
            ticker: str,
            start_date: date,
            end_date: date
    ) -> Union[List[Dict], str]:
        try:
            fs = YahooFinanceSearch()
            return fs.fetch_json(ticker, start_date, end_date)
        except Exception as e:
            return repr(e)

