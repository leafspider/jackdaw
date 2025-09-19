import pytest, asyncio
from sparrow.toolkit.search.google_search import Websearch



@pytest.mark.asyncio
async def test_google_search():

    ds = Websearch()

    search_query = "top 5 countries with highest gross happiness index"
    results = ds.fetch_results_json(search_query, num_results=5)

    assert len(results['results']) > 0

    print(results)

    # search_query = input("Enter your search query: ")
    # results = gs.fetch_results(search_query, num_results=5)

    # for idx, result in enumerate(gs.results, 1):
        # print(f"{idx}. {result}")
        # html = gs.get_html(result)
        # print( gs.parse_html(html) )

    # for result in results:
    #    print( result.title )


if __name__ == '__main__':

    asyncio.run(test_google_search())