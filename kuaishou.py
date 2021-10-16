import asyncio
import json
import re
import time

import aiohttp


async def download_video(video_url: str):
    print(f'Downloading from url: {video_url}')

    async with aiohttp.ClientSession() as client:
        async with client.get(video_url) as page:
            page.raise_for_status()
            with open(f'{int(time.time_ns())}.mp4', 'wb') as f:
                while True:
                    chunk = await page.content.read(1024 ** 4)
                    if not chunk:
                        break
                    f.write(chunk)


class KuaiShouScrapy:
    def __init__(self):
        self.base_url = 'https://www.kuaishou.com/graphql'
        self.payload = "{\"operationName\":\"sameCityDataQuery\"," \
                       "\"variables\":{\"semKeyword\":\"\"," \
                       "\"semCrowd\":\"\",\"utmSource\":\"\"," \
                       "\"utmMedium\":\"\",\"page\":\"nearby\"}," \
                       "\"query\":\"" \
                       "fragment feedContent on Feed {\\n  type\\n  " \
                       "author {\\n    id\\n    name\\n    " \
                       "headerUrl\\n    following\\n    " \
                       "headerUrls {\\n      url\\n     " \
                       " __typename\\n    }\\n    " \
                       "__typename\\n  }\\n  photo " \
                       "{\\n    id\\n    duration\\n    " \
                       "caption\\n    likeCount\\n    " \
                       "realLikeCount\\n    coverUrl\\n    " \
                       "photoUrl\\n    coverUrls {\\n      " \
                       "url\\n      __typename\\n    }\\n    " \
                       "timestamp\\n    expTag\\n    " \
                       "animatedCoverUrl\\n    distance\\n   " \
                       " videoRatio\\n    liked\\n    " \
                       "stereoType\\n    __typename\\n  }\\n  " \
                       "canAddComment\\n  llsid\\n  status\\n  " \
                       "currentPcursor\\n  __typename\\n}\\n\\n" \
                       "fragment photoResult on PhotoResult " \
                       "{\\n  result\\n  llsid\\n  expTag\\n  " \
                       "serverExpTag\\n  pcursor\\n  feeds {\\n    " \
                       "...feedContent\\n    __typename\\n  }\\n  " \
                       "webPageArea\\n  __typename\\n}\\n\\nquery " \
                       "sameCityDataQuery($pcursor: String, " \
                       "$semKeyword: String, $semCrowd: String, " \
                       "$utmSource: String, $utmMedium: String, " \
                       "$page: String) {\\n  " \
                       "sameCityData(pcursor: $pcursor, semKeyword: $semKeyword, " \
                       "semCrowd: $semCrowd, utmSource: $utmSource, " \
                       "utmMedium: $utmMedium, page: $page) " \
                       "{\\n    ...photoResult\\n    __typename\\n  }\\n}\\n\"}"

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.114 Safari/537.36',
            'dnt': '1',
            'Referer': 'https://www.kuaishou.com/brilliant'
        }

    async def get_video_url_list(self):
        async with aiohttp.ClientSession() as client:
            async with client.post(self.base_url, headers=self.headers, data=json.loads(self.payload)) as page:
                json_data = await page.json()
                feeds_data = json_data['data']['sameCityData']['feeds']

                video_list_temp = []
                for element in feeds_data:
                    video_list_temp.append(element['photo']['photoUrl'])

                video_list = [re.sub(r'&tt=.*?$', '', x) for x in video_list_temp]

        return video_list


async def main():
    b = KuaiShouScrapy()
    video_list = await b.get_video_url_list()
    video_list = video_list[:30]

    tasks = []

    start_time = time.time()
    for element in video_list:
        tasks.append(download_video(element))

    await asyncio.gather(*tasks)

    print(f'下载完成（视频条数：{len(video_list)}，用时：{time.time() - start_time:.2f}s')


if __name__ == '__main__':
    asyncio.run(main())
