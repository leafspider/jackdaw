import pytest, asyncio
from sparrow.toolkit.search.fin_search import YahooFinanceSearch


@pytest.mark.asyncio
async def test_finsearch():

    fs = YahooFinanceSearch()

    ticker = "GOOG"
    start_date = "2024-04-01"
    end_date = "2024-05-01"

    from datetime import date

    start_date = date(2024, 4, 1)
    end_date = date(2024, 5, 1)
    data = fs.fetch_json(ticker, start_date, end_date)
    print(data)

    assert len(data) > 0


if __name__ == '__main__':

    asyncio.run(test_finsearch())