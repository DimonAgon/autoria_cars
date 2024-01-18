
from bs4 import BeautifulSoup, ResultSet, Tag
import requests

from typing import Type


class AutoriaCarScrapper:

    @classmethod
    def autoria_ads_scrap(cls, search_url: str) -> Type[ResultSet]:
        ads = None

        page = 1
        while True:
            on_page_url = f'{search_url}/?page={page}'
            search_result = requests.get(on_page_url)
            if not search_result.ok: break
            search_result_text = search_result.text
            souped = BeautifulSoup(search_result_text, 'html.parser')
            page_ads = souped.find_all('section', attrs={'class': "ticket-item"})
            if ads is None:
                ads = page_ads

            ads.extend(page_ads)
            page += 1

        return ads

    @classmethod
    def autoria_ad_content_scrap(cls, ad: Type[Tag]) -> Type[Tag]:

        content = ad.find('div', attrs={'class': "content"})

        return content
