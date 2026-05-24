# -*- coding: utf-8 -*-
import re, urllib.parse
from bs4 import BeautifulSoup
from base.spider import Spider

class Spider(Spider):
    def init(self, extend=""):
        self.host = "https://www.ht10010.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    def getName(self):
        return '枫叶影院'

    def homeContent(self, filter):
        area_opts = [{"n": a[0], "v": a[1]} for a in [("全部",""),("大陆","大陆"),("香港","香港"),("台湾","台湾"),("美国","美国"),("韩国","韩国"),("日本","日本"),("泰国","泰国"),("新加坡","新加坡"),("马来西亚","马来西亚"),("印度","印度"),("英国","英国"),("法国","法国"),("加拿大","加拿大"),("西班牙","西班牙"),("俄罗斯","俄罗斯"),("其它","其它")]]
        year_opts = [{"n": a[0], "v": a[1]} for a in [("全部",""),("2026","2026"),("2025","2025"),("2024","2024"),("2023","2023"),("2022","2022"),("2021","2021"),("2020","2020"),("2019","2019"),("2018","2018"),("2017","2017"),("2016","2016"),("2015","2015"),("2014","2014"),("2013","2013"),("2012","2012"),("2011","2011"),("2010","2010"),("2009","2009"),("2008","2008"),("2007","2007"),("2006","2006"),("2005","2005"),("2004","2004")]]
        lang_opts = [{"n": a[0], "v": a[1]} for a in [("全部",""),("国语","国语"),("英语","英语"),("粤语","粤语"),("闽南语","闽南语"),("韩语","韩语"),("日语","日语"),("法语","法语"),("德语","德语"),("其它","其它")]]
        sort_opts = [{"n": a[0], "v": a[1]} for a in [("时间","time"),("人气","hits"),("评分","score")]]
        letter_opts = [{"n": a[0], "v": a[1]} for a in [("全部",""),("A","A"),("B","B"),("C","C"),("D","D"),("E","E"),("F","F"),("G","G"),("H","H"),("I","I"),("J","J"),("K","K"),("L","L"),("M","M"),("N","N"),("O","O"),("P","P"),("Q","Q"),("R","R"),("S","S"),("T","T"),("U","U"),("V","V"),("W","W"),("X","X"),("Y","Y"),("Z","Z"),("0-9","0-9")]]
        return {"class": [
            {"type_id": "2", "type_name": "电视剧"},
            {"type_id": "1", "type_name": "电影"},
            {"type_id": "4", "type_name": "动漫"},
            {"type_id": "3", "type_name": "综艺"},
            {"type_id": "5", "type_name": "热门短剧"},
        ], "filters": {
            "2": [
                {"key": "class", "name": "类型", "value": [{"n": "全部", "v": "2"},{"n": "国产剧", "v": "13"},{"n": "日韩剧", "v": "15"},{"n": "海外剧", "v": "16"}]},
                {"key": "area", "name": "地区", "value": area_opts},
                {"key": "genre", "name": "剧情", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("古装","古装"),("战争","战争"),("青春偶像","青春偶像"),("喜剧","喜剧"),("家庭","家庭"),("犯罪","犯罪"),("动作","动作"),("奇幻","奇幻"),("剧情","剧情"),("历史","历史"),("经典","经典"),("乡村","乡村"),("情景","情景"),("商战","商战"),("网剧","网剧"),("其他","其他")]]},
                {"key": "year", "name": "年份", "value": year_opts},
                {"key": "lang", "name": "语言", "value": lang_opts},
                {"key": "letter", "name": "字母", "value": letter_opts},
                {"key": "sort", "name": "排序", "value": sort_opts},
            ],
            "1": [
                {"key": "class", "name": "类型", "value": [{"n": "全部", "v": "1"},{"n": "动作片", "v": "6"},{"n": "喜剧片", "v": "7"},{"n": "恐怖片", "v": "8"},{"n": "科幻片", "v": "9"},{"n": "爱情片", "v": "10"},{"n": "剧情片", "v": "11"},{"n": "战争片", "v": "12"},{"n": "纪录片", "v": "20"}]},
                {"key": "area", "name": "地区", "value": area_opts},
                {"key": "genre", "name": "剧情", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("喜剧","喜剧"),("爱情","爱情"),("恐怖","恐怖"),("动作","动作"),("科幻","科幻"),("剧情","剧情"),("战争","战争"),("警匪","警匪"),("犯罪","犯罪"),("动画","动画"),("奇幻","奇幻"),("武侠","武侠"),("冒险","冒险"),("枪战","枪战"),("悬疑","悬疑"),("惊悚","惊悚"),("经典","经典"),("青春","青春"),("文艺","文艺"),("微电影","微电影"),("古装","古装"),("历史","历史"),("运动","运动"),("农村","农村"),("儿童","儿童"),("网络电影","网络电影")]]},
                {"key": "year", "name": "年份", "value": year_opts},
                {"key": "lang", "name": "语言", "value": lang_opts},
                {"key": "letter", "name": "字母", "value": letter_opts},
                {"key": "sort", "name": "排序", "value": sort_opts},
            ],
            "4": [
                {"key": "class", "name": "类型", "value": [{"n": "全部", "v": "4"},{"n": "国产动漫", "v": "25"},{"n": "日韩动漫", "v": "26"}]},
                {"key": "genre", "name": "剧情", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("情感","情感"),("科幻","科幻"),("热血","热血"),("推理","推理"),("搞笑","搞笑"),("冒险","冒险"),("奇幻","奇幻"),("战斗","战斗"),("校园","校园"),("萝莉","萝莉"),("治愈","治愈"),("原创","原创"),("亲子","亲子"),("益智","益智"),("励志","励志"),("其他","其他")]]},
                {"key": "area", "name": "地区", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("大陆","大陆"),("香港","香港"),("台湾","台湾"),("美国","美国"),("韩国","韩国"),("日本","日本"),("法国","法国"),("英国","英国"),("其它","其它")]]},
                {"key": "year", "name": "年份", "value": year_opts},
                {"key": "lang", "name": "语言", "value": lang_opts},
                {"key": "letter", "name": "字母", "value": letter_opts},
                {"key": "sort", "name": "排序", "value": sort_opts},
            ],
            "3": [
                {"key": "class", "name": "类型", "value": [{"n": "全部", "v": "3"},{"n": "大陆综艺", "v": "21"},{"n": "日韩综艺", "v": "22"}]},
                {"key": "genre", "name": "剧情", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("选秀","选秀"),("情感","情感"),("访谈","访谈"),("播报","播报"),("音乐","音乐"),("美食","美食"),("旅游","旅游"),("搞笑","搞笑"),("游戏","游戏"),("亲子","亲子"),("其它","其它")]]},
                {"key": "area", "name": "地区", "value": [{"n": v[0], "v": v[1]} for v in [("全部",""),("大陆","大陆"),("香港","香港"),("台湾","台湾"),("美国","美国"),("韩国","韩国"),("日本","日本"),("英国","英国"),("其它","其它")]]},
                {"key": "year", "name": "年份", "value": year_opts},
                {"key": "lang", "name": "语言", "value": lang_opts},
                {"key": "letter", "name": "字母", "value": letter_opts},
                {"key": "sort", "name": "排序", "value": sort_opts},
            ],
        }}

    def homeVideoContent(self):
        html = self._fetch('/')
        return {"list": self._parse_video_list(html)}

    def categoryContent(self, tid, pg, filter, extend):
        f = {}
        if isinstance(filter, dict):
            f = {k: v for k, v in filter.items() if v}
        if extend and isinstance(extend, dict):
            for k in ['class', 'tid', 'type']:
                if extend.get(k):
                    f['class'] = str(extend[k])
                    break
        route_tid = f.get('class', str(tid))
        area = f.get('area', '')
        genre = f.get('genre', '')
        year = f.get('year', '')
        lang = f.get('lang', '')
        letter = f.get('letter', '')
        sort = f.get('sort', '')
        if not area and not genre and not year and not lang and not letter and not sort:
            url = f'/cupfox-list/{route_tid}--------{pg}---.html'
            html = self._fetch(url)
            items = self._parse_video_list(html)
            page = int(pg)
            soup = BeautifulSoup(html, 'html.parser')
            pagecount = page
            for a in soup.select('a.page-link'):
                if a.text == '尾页':
                    m = re.search(r'---(\d+)---', a.get('href', ''))
                    if m:
                        pagecount = int(m.group(1))
                    break
            if not items:
                pagecount = 0
            return {"list": items, "page": page, "pagecount": pagecount, "limit": 36, "total": 9999}
        params = [route_tid, area, sort, genre, lang, letter, '', '', year]
        url = '/cupfox-list/' + '-'.join(params) + '.html'
        html = self._fetch(url)
        items = self._parse_video_list(html)
        return {"list": items, "page": 1, "pagecount": 1, "limit": 36, "total": 9999}

    def detailContent(self, ids):
        result = {"list": []}
        vid = ids[0].split(',')[0].strip()
        try:
            html = self._fetch(f'/detail/{vid}.html')
            if not html: return result
            soup = BeautifulSoup(html, 'html.parser')
            vod_name = soup.select_one('h3.slide-info-title')
            vod_name = vod_name.text.strip() if vod_name else ''
            vod_pic = soup.select_one('img.lazy')
            vod_pic = self._fix_pic(vod_pic.get('data-src', '')) if vod_pic else ''
            vod_director = ''
            vod_actor = ''
            for el in soup.select('.slide-info'):
                text = el.get_text(' ').strip()
                if text.startswith('导演：'):
                    vod_director = text.replace('导演：', '').strip()
                elif text.startswith('演员：'):
                    vod_actor = text.replace('演员：', '').strip()
            vod_content = soup.select_one('#height_limit')
            vod_content = vod_content.get_text(' ', strip=True) if vod_content else ''
            play_from, play_url = [], []
            for tab in soup.select('.anthology-tab a.swiper-slide'):
                src_name = re.sub(r'<[^>]+>', '', str(tab)).strip() or tab.get_text(' ', strip=True).strip()
                if src_name:
                    play_from.append(src_name)
            tab_blocks = soup.select('.anthology-list-box')
            for i, block in enumerate(tab_blocks):
                ep_list = []
                for a in block.select('li a'):
                    href = a.get('href', '')
                    m = re.search(r'/play/(.*?)\.html', href)
                    if m:
                        ep_list.append(f'{a.text.strip()}${vid}-{m.group(1)}')
                ep_list.reverse()
                if ep_list and i < len(play_from):
                    play_url.append('#'.join(ep_list))
            valid_from = [pf for i, pf in enumerate(play_from) if i < len(play_url)]
            result["list"].append({
                "vod_id": vid, "vod_name": vod_name, "vod_pic": vod_pic,
                "vod_director": vod_director, "vod_actor": vod_actor,
                "vod_content": vod_content,
                "vod_play_from": "$$$".join(valid_from),
                "vod_play_url": "$$$".join(play_url),
            })
        except:
            pass
        return result

    def searchContent(self, key, quick, pg="1"):
        try:
            decoded = urllib.parse.unquote(key)
        except:
            decoded = key
        html = self._fetch(f'/cupfox-search/{urllib.parse.quote(decoded)}----------{pg}---.html')
        items = self._parse_search_list(html)
        return {"list": items, "page": int(pg), "pagecount": 1, "limit": 36, "total": len(items)}

    def playerContent(self, flag, id, vipFlags):
        try:
            url = id if id.startswith('http') else f'{self.host}/play/{id}.html'
            html = self._fetch(url)
            if html:
                m = re.search(r'var\s+player_aaaa\s*=\s*(\{.*?\});', html, re.S)
                if m:
                    import json
                    try:
                        pd = json.loads(m.group(1))
                        pu = pd.get('url', '')
                        if pu and (pu.endswith('.m3u8') or pu.endswith('.mp4')):
                            return {"parse": 0, "url": pu, "header": self.headers}
                        if pu and pu.startswith('http'):
                            return {"parse": 1, "url": pu, "header": self.headers}
                    except:
                        pass
            return {"parse": 1, "url": url, "header": self.headers}
        except:
            return {"parse": 1, "url": id, "header": self.headers}

    def localProxy(self, param=''): return {}
    def isVideoFormat(self, url): return False
    def manualVideoCheck(self): return False

    def _fetch(self, url):
        try:
            if not url.startswith('http'):
                url = self.host + url
            rsp = self.fetch(url, headers=self.headers, verify=False)
            return rsp.text if rsp else ''
        except:
            return ''

    def _fix_pic(self, u):
        if not u: return ''
        if u.startswith('//'): return 'https:' + u
        return u.replace('&amp;', '&')

    def _parse_video_list(self, html):
        videos, seen = [], set()
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('a.public-list-exp')
        for a in cards:
            href = a.get('href', '')
            m = re.search(r'/detail/(\d+)\.html', href)
            if not m: continue
            vod_id = m.group(1)
            if vod_id in seen: continue
            seen.add(vod_id)
            vod_name = a.get('title', '') or (a.select_one('img') and a.select_one('img').get('alt', '')) or ''
            pic_el = a.select_one('img')
            vod_pic = self._fix_pic(pic_el.get('data-src', '')) if pic_el else ''
            remark_el = a.select_one('.ft2') or a.select_one('.public-list-prb')
            vod_remarks = remark_el.text.strip() if remark_el else ''
            videos.append({"vod_id": vod_id, "vod_name": vod_name.strip(), "vod_pic": vod_pic, "vod_remarks": vod_remarks})
        return videos

    def _parse_search_list(self, html):
        videos, seen = [], set()
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('a.public-list-exp')
        for a in cards:
            href = a.get('href', '')
            m = re.search(r'/detail/(\d+)\.html', href)
            if not m: continue
            vod_id = m.group(1)
            if vod_id in seen: continue
            seen.add(vod_id)
            pic_el = a.select_one('img')
            vod_pic = self._fix_pic(pic_el.get('data-src', '')) if pic_el else ''
            title_el = soup.select_one(f'a.thumb-txt[href="/detail/{vod_id}.html"]')
            if title_el:
                vod_name = title_el.text.strip()
            else:
                vod_name = a.select_one('img') and a.select_one('img').get('alt', '') or ''
            remark_el = a.select_one('.public-list-prb') or a.select_one('.ft2')
            vod_remarks = remark_el.text.strip() if remark_el else ''
            videos.append({"vod_id": vod_id, "vod_name": vod_name.strip(), "vod_pic": vod_pic, "vod_remarks": vod_remarks})
        return videos