import os

from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver

import asyncio

class Websearch:

    def __init__(s):
        s.options = webdriver.ChromeOptions()
        s.options.add_argument("--headless")
        s.driver = webdriver.Chrome(options=s.options)
        s.results = None

    def fetch_results(s, query, num_results=10):
        s.results = search(query, num_results=num_results, advanced=True)
        s.driver.quit()
        return s.results

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

    def fetch_results_json(s, query, num_results=5):

        fetch_results = s.fetch_results(query, num_results=num_results)
        data = {"query": query, "follow_up_questions": "None", "answer": "None", "images": "None", "results": []}
        data_results = []
        for res in fetch_results:
            data_results.append({"title": res.title, "url": res.url, "content": res.description})
        data["results"] = data_results
        return data
    
    async def fetch_results_json_async(s, query, num_results=5):

        fetch_results = s.fetch_results(query, num_results=num_results)
        data = {"query": query, "follow_up_questions": "None", "answer": "None", "images": "None", "results": []}
        data_results = []
        for res in fetch_results:
            data_results.append({"title": res.title, "url": res.url, "content": res.description})
        data["results"] = data_results
        return data


if __name__ == "__main__":

    gs = Websearch()

    search_query = "top 5 countries with highest gross happiness index"
    results = gs.fetch_results_json(search_query, num_results=1)
    print(results)

    #search_query = input("Enter your search query: ")
    #results = gs.fetch_results(search_query, num_results=5)

    #for idx, result in enumerate(gs.results, 1):
        #print(f"{idx}. {result}")
        #html = gs.get_html(result)
        #print( gs.parse_html(html) )

    #for result in results:
    #    print( result.title )


