# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import sys, urllib3
sys.path.append('..')
from base.spider import Spider
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Spider(Spider):
    # 对齐JS中的请求头
    headers, host = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ALN-AL00 Build/HUAWEIALN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.196 Mobile Safari/537.36',
        'X-Platform': 'web',
        'Referer': 'https://film.symx.club',
        'Accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache'
    }, 'https://film.symx.club'

    def init(self, extend=''):
        try:
            host = extend.strip().rstrip('/')
            if host.startswith('http'):
                self.host = host
                # 更新Referer
                self.headers['Referer'] = host
            return None
        except Exception as e:
            print(f'初始化异常：{e}')
            return None

    def homeContent(self, filter):
        try:
            response = self.fetch(f'{self.host}/api/category/top', headers=self.headers, verify=False).json()
            classes = []
            for i in response.get('data', []):
                if isinstance(i, dict):
                    classes.append({'type_id': i['id'], 'type_name': i['name']})
            return {'class': classes}
        except Exception as e:
            print(f'首页分类异常：{e}')
            return {'class': []}

    def homeVideoContent(self):
        try:
            response = self.fetch(f'{self.host}/api/film/category', headers=self.headers, verify=False).json()
            videos = []
            for i in response.get('data', []):
                for j in i.get('filmList', []):
                    videos.append({
                        'vod_id': j.get('id'),
                        'vod_name': j.get('name'),
                        'vod_pic': j.get('cover'),
                        'vod_remarks': j.get('doubanScore')
                    })
            return {'list': videos}
        except Exception as e:
            print(f'首页视频异常：{e}')
            return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            url = f'{self.host}/api/film/category/list?area=&categoryId={tid}&language=&pageNum={pg}&pageSize=15&sort=updateTime&year='
            response = self.fetch(url, headers=self.headers, verify=False).json()
            videos = []
            for i in response.get('data', {}).get('list', []):
                videos.append({
                    'vod_id': i.get('id'),
                    'vod_name': i.get('name'),
                    'vod_pic': i.get('cover'),
                    'vod_remarks': i.get('updateStatus')
                })
            return {'list': videos, 'page': pg, 'pagecount': response.get('data', {}).get('pages', 1)}
        except Exception as e:
            print(f'分类内容异常：{e}')
            return {'list': [], 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        try:
            url = f'{self.host}/api/film/search?keyword={key}&pageNum={pg}&pageSize=10'
            response = self.fetch(url, headers=self.headers, verify=False).json()
            videos = []
            for i in response.get('data', {}).get('list', []):
                videos.append({
                    'vod_id': i.get('id'),
                    'vod_name': i.get('name'),
                    'vod_pic': i.get('cover'),
                    'vod_remarks': i.get('updateStatus'),
                    'vod_year': i.get('year'),
                    'vod_area': i.get('area'),
                    'vod_director': i.get('director')
                })
            return {'list': videos, 'page': pg}
        except Exception as e:
            print(f'搜索异常：{e}')
            return {'list': [], 'page': pg}

    def detailContent(self, ids):
        try:
            response = self.fetch(f'{self.host}/api/film/detail?id={ids[0]}', headers=self.headers, verify=False).json()
            data = response.get('data', {})
            video, show, play_urls = {}, [], []
            for i in data.get('playLineList', []):
                show.append(i['playerName'])
                play_url = []
                for j in i.get('lines', []):
                    play_url.append(f"{j['name']}${j['id']}")
                play_urls.append('#'.join(play_url))
            video.update({
                'vod_id': data.get('id'),
                'vod_name': data.get('name'),
                'vod_pic': data.get('cover'),
                'vod_year': data.get('year'),
                'vod_area': data.get('other'),
                'vod_actor': data.get('actor'),
                'vod_director': data.get('director'),
                'vod_content': data.get('blurb'),
                'vod_score': data.get('doubanScore'),
                'vod_play_from': '$$$'.join(show),
                'vod_play_url': '$$$'.join(play_urls)
            })
            return {'list': [video]}
        except Exception as e:
            print(f'详情页异常：{e}')
            return {'list': []}

    def playerContent(self, flag, id, vipflags):
        try:
            response = self.fetch(f'{self.host}/api/line/play/parse?lineId={id}', headers=self.headers, verify=False).json()
            return {
                'jx': '0',
                'parse': '0',
                'url': response.get('data', ''),
                'header': {'User-Agent': self.headers['User-Agent']}
            }
        except Exception as e:
            print(f'播放地址解析异常：{e}')
            return {'jx': '0', 'parse': '0', 'url': ''}

    def getName(self):
        return '山木有兮'

    def isVideoFormat(self, url):
        return url.endswith(('.mp4', '.m3u8', '.flv', '.ts'))

    def manualVideoCheck(self):
        return False

    def destroy(self):
        pass

    def localProxy(self, param):
        pass
