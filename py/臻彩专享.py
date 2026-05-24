# coding=utf-8
# !/usr/bin/python

import requests
from base.spider import Spider
import sys

sys.path.append('..')
xurl = "http://sspa8.top:9999"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

class Spider(Spider):
    global xurl
    global headerx
    global pm

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeVideoContent(self):
        pass

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "15449825732514818", "type_name": "臻彩电影"},
                            {"type_id": "15449368595744258", "type_name": "臻彩剧集"},
                            {"type_id": "15451230911645698", "type_name": "臻彩动漫"},
                            {"type_id": "15444397385394434", "type_name": "臻彩综艺"},
                            {"type_id": "16017792290330370", "type_name": "臻彩纪录片"}
                            ],
                  }

        return result

    def categoryContent(self, cid, pg, filter, ext):
        res=requests.get(f'{xurl}/category?cid={cid}&pg={pg}').json()
        return res

    def detailContent(self, ids):
        result = {}
        videos = []
        did = ids[0]
        res = requests.get(f'{xurl}/detail?ids={did}').json()
        return res


    def playerContent(self, flag, id, vipFlags):
        res = requests.get(f'http://sspa8.top:8100/suisui.php?url={id}')
        if res.status_code == 200:
            kjson = res.json()
            url = kjson['url']
            result = {}
            result["parse"] = 0
            result["playUrl"] = ''
            result["url"] = url
            return result
        return res

    def searchContentPage(self, key, quick, page):
        res = requests.get(f'{xurl}/search?key={key}&page={page}').json()
        return res

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')


    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None