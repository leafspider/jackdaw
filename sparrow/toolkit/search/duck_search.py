import os, asyncio

from bs4 import BeautifulSoup

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import json

class Websearch:

    def __init__(s):
        s.results = None

    def fetch_results(s, query, num_results=10):
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=num_results)
        results_separator = "!29!"
        search = DuckDuckGoSearchResults(api_wrapper=wrapper, results_separator=results_separator)
        s.results = search.invoke(query)

        results_list = s.results.split(results_separator)
        json_list = []
        for res in results_list:
            pos_snippet = res.index('snippet')
            pos_title = res.index('title')
            pos_link = res.index('link')
            snippet = res[pos_snippet+9:pos_title-2]
            title = res[pos_title+7:pos_link-2]
            link = res[pos_link+6:]
            json_dict = {'snippet':snippet, 'title':title, 'link':link}
            json_list.append(json_dict)

        return json_list

    def get_html(s, url):
        s.driver.get(url)
        html = s.driver.page_source
        return html

    def parse_html(s, html):
        soup = BeautifulSoup(html, 'lxml')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        return os.linesep.join([s for s in text.splitlines() if s])

    def fetch_results_json(s, query, num_results=10):

        fetch_results = s.fetch_results(query, num_results=5)
        data = {"query": query, "follow_up_questions": "None", "answer": "None", "images": "None", "results": []}
        data_results = []
        for res in fetch_results:
            data_results.append({"title": res['title'], "url": res['link'], "content": res['snippet']})
        data["results"] = data_results
        return data


if __name__ == "__main__":

    from tests.toolkit.test_google_search import test_ducksearch

    asyncio.run(test_ducksearch())

