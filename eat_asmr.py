import re
from typing import Union

import requests
from lxml import etree

class EastAsmr:
    def __init__(self, key_word: str):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.212 Safari/537.36',
            'referer': 'https://eatasmr.com',
            'origin': 'https://eatasmr.com'
        }
        self.login_url = 'https://eatasmr.com/wp-admin/admin-ajax.php'

        self.Session = requests.Session()
        self.auth()

        self.search_url = f'https://eatasmr.com/?s={key_word}'
        self.search_result = []


    def auth(self):
        payload = {
            'lwa': 1,
            'log': 'remiliacn',
            'pwd': 'cF5)9vXHSB3o',
            'lwa_profile_link': 0,
            'login-with-ajax': 'login'
        }
        self.Session.post(self.login_url, data=payload, headers=self.headers)

    def get_search_result(self):
        page = self.Session.get(self.search_url, headers=self.headers)
        # e = etree.HTML(page.text)
        # result = e.xpath(
        #     '/html/body/div/div[1]/div/div/div/div[1]'
        #     '/div/section/article/section/div[2]/header'
        #     '/div/h2/a/text()'
        # )

        search_result = re.findall(
            r'<a class="czr-title" href="(.*?)".*?title=".*?">(.*?)</a>',
            page.text
        )

        self.search_result = search_result


    def get_info(self, index: Union[str, int]):
        if isinstance(index, str):
            if not index.isdigit():
                raise TypeError('Invalid index number.')

        index = int(index)
        index -= 1

        if index >= len(self.search_result):
            raise ValueError('index greater than search reuslt')

        result = self.search_result[index]
        url = result[0]

        page = self.Session.get(url, headers=self.headers)
        info = re.findall(
            r'<a style="text-decoration.*?>(.*?)</a>',
            page.text
        )

        play_data = re.findall('<div data-play="[{&quot;b&quot;:&quot;BV1w5411L7N9&quot;},{&quot;b&quot;:&quot;BV13T4y1F7BT&quot;}]"')



if __name__ == '__main__':
    api = EastAsmr('耳舔')
    api.get_search_result()
    api.get_info(1)