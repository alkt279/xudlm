# -*- coding: utf-8 -*-
#by  htlnb
import sys
import json
import time
import hashlib
import os
import requests
from datetime import datetime
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ym_cache.json")

    def __init__(self):
        self._cache = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            except:
                self._cache = {}

    def save_cache(self):
        try:
            with open(self.CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, ensure_ascii=False)
        except:
            pass

    def getCache(self, key):
        return self._cache.get(key)

    def setCache(self, key, value):
        self._cache[key] = value
        self.save_cache()

    def delCache(self, key):
        if key in self._cache:
            self._cache.pop(key)
            self.save_cache()

    def init(self, extend):
        js1 = json.loads(extend)
        self.host = js1['host']
        self.username = ""
        self.password = ""

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
    }

    def homeContent(self, filter):
        data = self.fetch(f"{self.host}/api/v1/video/categories", headers=self.headers).json()
        return {'class': data['data']}

    def homeVideoContent(self):
        data = self.fetch(f"{self.host}/api/v1/content/slides", headers=self.headers).json()
        videos = []
        for i in data['data']:
            id = i['vod_id']
            name = i['title']
            pic = i['image_url']
            video = {"vod_id": id, "vod_name": name, "vod_pic": pic}
            videos.append(video)
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        params = {'type_id': tid, 'page_size': '18', 'page': pg, 'order': 'time'}
        data = self.fetch(f"{self.host}/api/v1/video/list", params=params, headers=self.headers).json()
        return data['data']

    def detailContent(self, ids):
        data = self.fetch(f"{self.host}/api/v1/video/detail/{ids[0]}", headers=self.headers).json()
        return {'list': [data['data']]}

    def searchContent(self, key, quick, pg="1"):
        params = {'keyword': key, 'page_size': '18', 'page': pg}
        data = self.fetch(f"{self.host}/api/v1/video/search", params=params, headers=self.headers).json()
        return {'list': [data['data']['list']], 'page': pg}

    def str_to_timestamp(self, time_str):
        if not time_str:
            return 0
        try:
            import re
            time_str = re.sub(r'\.\d+', '', time_str)
            dt = datetime.fromisoformat(time_str)
            return int(dt.timestamp())
        except:
            return 9999999999

    def generate_random_username(self):
        return hashlib.md5(str(time.time()).encode()).hexdigest()[:10]

    def register(self):
        username = self.generate_random_username()
        password = "ym666666"
        url = f"{self.host}/api/v1/auth/register"
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/json", "User-Agent": self.headers['User-Agent']}
        res = self.post(url, json=data, headers=headers).json()

        token = res["data"]["token"]
        token_exp = res["data"]["expires_at"]
        vip_exp = res["data"]["user"]["vip_expires_at"]

        self.setCache("auth_token", f"Bearer {token}")
        self.setCache("token_expires_at", token_exp)
        self.setCache("vip_expires_at", vip_exp)

        return f"Bearer {token}"

    def get_token(self):
        now = int(time.time())
        auth_token = self.getCache("auth_token")
        token_exp_str = self.getCache("token_expires_at")
        vip_exp_str = self.getCache("vip_expires_at")

        if not auth_token:
            return self.register()

        token_exp = self.str_to_timestamp(token_exp_str)
        vip_exp = self.str_to_timestamp(vip_exp_str)

        if token_exp > now and vip_exp > now:
            return auth_token

        try:
            self.delCache("auth_token")
            self.delCache("token_expires_at")
            self.delCache("vip_expires_at")
        except:
            pass

        return self.register()

    def playerContent(self, flag, id, vipFlags):
        self.headers["authorization"] = self.get_token()
        data = self.fetch(f"{self.host}/api/v1/content/parse?url={id}&no_dash=1", headers=self.headers).json()
        return {"parse": 0, "playUrl": "", "url": self.decrypt(data['data']['url']), "header": self.headers}

    def localProxy(self, param):
        pass

    def decrypt(self, encrypted_data_b64):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        import base64
        key = b"YeCat2026AesKey!"
        encrypted_data = base64.b64decode(encrypted_data_b64)
        iv = encrypted_data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size).decode('utf-8')