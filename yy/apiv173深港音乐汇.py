# coding=utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import urljoin
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import concurrent.futures
import urllib.request
import urllib.parse
import threading
import datetime
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://www.45hk.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1'
          }

class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "/list/new@play_list", "type_name": "丢丢🌠新歌榜"},
                            {"type_id": "/list/top@play_list", "type_name": "丢丢🌠TOP榜单"},
                            {"type_id": "/list/djwuqu@play_list", "type_name": "丢丢🌠DJ舞曲"},
                            {"type_id": "/singerlist/index/index/index/index@singer_list", "type_name": "丢丢🌠歌手"},
                            {"type_id": "/playtype/index@video_list", "type_name": "丢丢🌠歌单"},
                            {"type_id": "/radiolist/index@video_list", "type_name": "丢丢🌠电台"},
                            {"type_id": "/mvlist/index@video_list", "type_name": "丢丢🌠高清MV"}],
                 }

        return result

    def homeVideoContent(self):
        videos = []

        detail = requests.get(url=xurl, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="ilingkuplay_list")

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                names = vod.find('div', class_="name")
                name = names.text.strip()

                id = names.find('a')['href']

                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg9.png"

                remark = "丢丢▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        fenge = cid.split("@")
        url = f'{xurl}{fenge[0]}/{str(page)}.html'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_=fenge[1])

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                names = vod.find('div', class_="name")
                name = names.text.strip()

                id = names.find('a')['href']

                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg9.png"

                remark = "丢丢▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''

        if 'http' not in did:
            did = xurl + did

        if all(kw not in did for kw in ['singer', 'playlist', 'radio']):
            res = requests.get(url=did, headers=headerx)
            res.encoding = "utf-8"
            res = res.text

            url = './qyg6.txt'
            response = requests.get(url)
            response.encoding = 'utf-8'
            code = response.text
            name = self.extract_middle_text(code, "s1='", "'", 0)
            Jumps = self.extract_middle_text(code, "s2='", "'", 0)

            content = '丢丢🎉为您介绍剧情📢' + self.extract_middle_text(res,'温馨提示：','</div>', 0)

            if name not in content:
                bofang = Jumps
                xianlu = '1'
            else:
                bofang = did
                xianlu = '丢丢音乐专线'

                videos.append({
                    "vod_id": did,
                    "vod_content": content,
                    "vod_play_from": xianlu,
                    "vod_play_url": bofang
                             })

        else:
            if 'singer' not in did:
                res = requests.get(url=did, headers=headerx)
                res.encoding = "utf-8"
                res = res.text

                url = './qyg6.txt'
                response = requests.get(url)
                response.encoding = 'utf-8'
                code = response.text
                name = self.extract_middle_text(code, "s1='", "'", 0)
                Jumps = self.extract_middle_text(code, "s2='", "'", 0)

                content = '丢丢🎉为您介绍剧情📢' + self.extract_middle_text(res,'温馨提示：','</div>', 0)

                if name not in content:
                    bofang = Jumps
                    xianlu = '1'
                else:
                    doc = BeautifulSoup(res, "lxml")

                    soups = doc.find('div', class_="play_list")

                    soup = soups.find_all('li')

                    for sou in soup:

                        ids = sou.find('div', class_="name")
                        id = xurl + ids.find('a')['href']

                        name = sou.text.strip()

                        bofang = bofang + name + '$' + id + '#'

                    bofang = bofang[:-1]

                    xianlu = '丢丢音乐专线'

                    videos.append({
                        "vod_id": did,
                        "vod_content": content,
                        "vod_play_from": xianlu,
                        "vod_play_url": bofang
                                  })

            else:
                vod_id = did
                vod_content = ""
                vod_play_from = ""
                play_urls = []
                fenge1 = did.split("/")
                fenge = fenge1[4].split(".")

                def fetch_page(page):
                    url = f"https://www.45hk.com/singer/{fenge[0]}/{page}.html"
                    try:
                        res = requests.get(url=url, headers=headerx, timeout=10)
                        res.encoding = "utf-8"
                        res_text = res.text

                        if '特定的不存在标识' in res_text or res_text.strip() == '':
                            return None

                        return res_text
                    except:
                        return None

                all_pages_content = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_page = {executor.submit(fetch_page, page): page for page in range(1, 26)}

                    for future in concurrent.futures.as_completed(future_to_page):
                        content = future.result()
                        if content:
                            all_pages_content.append(content)
                for res in all_pages_content:
                    doc = BeautifulSoup(res, "lxml")

                    url = './qyg6.txt'
                    response = requests.get(url)
                    response.encoding = 'utf-8'
                    code = response.text
                    name = self.extract_middle_text(code, "s1='", "'", 0)
                    Jumps = self.extract_middle_text(code, "s2='", "'", 0)

                    content = '丢丢为您介绍剧情' + self.extract_middle_text(res, '温馨提示：', '</div>', 0)

                    if name not in content:
                        bofang = Jumps
                        xianlu = '1'

                        if Jumps:
                            play_urls.append(Jumps)
                    else:
                        soups = doc.find('div', class_="play_list")
                        play_list = doc.find('div', class_="play_list")
                        if not play_list:
                            continue
                        soup = soups.find_all('li')

                        for sou in soup:
                            ids = sou.find('div', class_="name")
                            id = xurl + ids.find('a')['href']
                            name = sou.text.strip()
                            play_urls.append(f"{name}${id}")

                        xianlu = '丢丢音乐专线'
                        if not vod_content:
                            vod_content = content
                        if not vod_play_from:
                            vod_play_from = xianlu

                vod_play_url = "#".join(play_urls)

                if vod_id and vod_play_url:
                    videos.append({
                        "vod_id": vod_id,
                        "vod_content": vod_content if vod_content else "暂无剧情介绍",
                        "vod_play_from": vod_play_from if vod_play_from else "默认线路",
                        "vod_play_url": vod_play_url
                    })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        headerz = {
            'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
            'referer': id
                  }

        if 'mp3' in id:
            id = id.replace('https://www.45hk.com/mp3/', '').replace('.html', '')
            payload = {"id": id, "type": "music"}
            response = requests.post(xurl + "/js/play.php", headers=headerz, data=payload)
            if response.status_code == 200:
                response_data = response.json()
                url = response_data.get('url')

        else:
            detail = requests.get(url=id, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            url1 = xurl + self.extract_middle_text(res, "',url:'", "'", 0).replace('\\', '')
            response = requests.get(url1, headers=headerz, allow_redirects=False)
            if response.status_code == 302:
                url = response.headers['Location']

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, pg):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        url = f'{xurl}/so/{key}/{str(page)}.html'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="play_list")

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                na = vod.find("div", class_="mv")
                if na:
                    names = vod.find("div", class_="name")
                    name = names.text.strip()

                    id = na.find('a')['href']

                else:
                    names = vod.find("div", class_="name")
                    name = names.text.strip()

                    id = names.find('a')['href']

                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg9.png"

                remark = "丢丢▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

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







