import { _ } from 'assets://js/lib/cat.js';

let host = 'https://www.mgtv.com';

async function request(url, timeout = 10000) {
    let res = await req(url, {
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': host
        },
        timeout: timeout
    });
    return res.content;
}

async function init(cfg) {}

async function home(filter) {
    const classes = [
        { type_id: '3', type_name: '4K❂电影' },
        { type_id: '2', type_name: '4K❂电视剧' },
        { type_id: '1', type_name: '4K❂综艺' },
        { type_id: '50', type_name: '4K❂动漫' },
        { type_id: '10', type_name: '4K❂少儿' }
    ];
    return JSON.stringify({ class: classes });
}

/**
 * 详情页：解决搜索不调用解析的核心
 */
async function detail(id) {
    // 1. 统一 ID 格式：无论搜索还是分类，先提取出纯数字部分
    let video_id = id.toString().replace('.html', '').split('/').pop();

    let getList = async (vid) => {
        let res = await request(`https://pcweb.api.mgtv.com/episode/list?page=1&size=100&video_id=${vid}`);
        return JSON.parse(res);
    };

    let json = await getList(video_id);

    // 2. 关键：如果搜索到的 ID 拿不到列表，强制通过 H5 页面转换
    if (!json.data || (!json.data.list && !json.data.series)) {
        let html = await request(`https://www.mgtv.com/b/${video_id}.html`);
        // 尝试从源码抠出真正的 video_id
        let idMatch = html.match(/video_id[:\s"']+(\d+)/i) || html.match(/vid[:\s"']+(\d+)/i) || html.match(/\/b\/(\d+)\//);
        if (idMatch) {
            video_id = idMatch[1];
            json = await getList(video_id);
        }
    }

    let list = json.data.list || json.data.series || [];
    let vod = { 
        vod_id: id, 
        vod_play_from: '芒果TV',
        vod_content: '官方源解析'
    };

    // 3. 提取剧集大标题
    if (json.data && json.data.info) {
        vod.vod_name = json.data.info.title || json.data.info.pcName;
        vod.vod_pic = json.data.info.thumb || json.data.info.img;
        vod.vod_content = json.data.info.desc || '';
    }

    // 4. 【彻底修复】强制将所有播放链接转为解析接口识别的完整 URL
    if (list.length > 0) {
        if (!vod.vod_name) vod.vod_name = list[0].pcName || list[0].t4;
        
        vod.vod_play_url = list.map((it) => {
            let name = it.t4 || it.title || it.t2 || '正片';
            let link = it.url;
            // 只要不是 http 开头，全部重组为标准 B 站播放页格式
            if (!link.startsWith('http')) {
                // 如果 link 包含 / 就直接拼，否则按 ID 格式拼
                link = link.startsWith('/') ? `https://www.mgtv.com${link}` : `https://www.mgtv.com/b/${link}.html`;
            }
            // 最后的安全检查，确保没有 // 这种重叠
            link = link.replace(/([^:])\/\//g, '$1/');
            return `${name}$${link}`;
        }).join('#');
    } else {
        // 搜索结果完全无列表时的兜底：强制发送完整 URL
        let finalUrl = id.startsWith('http') ? id : `https://www.mgtv.com/b/${id}.html`;
        vod.vod_play_url = `正片$${finalUrl}`;
        if (!vod.vod_name) vod.vod_name = "搜索资源";
    }

    return JSON.stringify({ list: [vod] });
}

/**
 * 搜索功能：确保搜索出的 vod_id 干净、可传递
 */
async function search(wd, quick, pg) {
    let url = `https://mobileso.bz.mgtv.com/msite/search/v2?q=${encodeURIComponent(wd)}&pn=${pg || 1}&pc=10`;
    let res = await request(url);
    let json = JSON.parse(res);
    let videos = [];
    _.each(json.data.contents, (content) => {
        if (content.type === 'media' && content.data) {
            let item = content.data[0];
            let vidMatch = item.url.match(/\/(.*?)\.html/);
            if (vidMatch) {
                videos.push({
                    vod_id: vidMatch[1], // 传给 detail 的原始 ID
                    vod_name: item.title.replace(/<\/?[^>]+>/g, ''),
                    vod_pic: item.img,
                    vod_remarks: (item.desc || []).join('/')
                });
            }
        }
    });
    return JSON.stringify({ list: videos });
}

async function category(tid, pg, filter, extend) {
    let url = `https://pianku.api.mgtv.com/rider/list/pcweb/v3?platform=pcweb&channelId=${tid}&pn=${pg}&pc=20&hudong=1&kind=a1&area=a1`;
    let res = await request(url);
    let json = JSON.parse(res);
    let videos = _.map(json.data.hitDocs, (it) => {
        return {
            vod_id: (it.videoId || it.playPartId).toString(), 
            vod_name: it.title,
            vod_pic: it.img,
            vod_remarks: it.updateInfo || (it.rightCorner ? it.rightCorner.text : '')
        };
    });
    return JSON.stringify({ page: parseInt(pg), list: videos });
}

async function play(flag, id, flags) {
    const parseApis = ['内置解析还不完善'];
    for (let api of parseApis) {
        try {
            // 这里收到的 id 已经是 detail 处理过的完整 https 地址
            let target = api + encodeURIComponent(id);
            let res = await req(target, {
                headers: { 'User-Agent': 'okhttp/4.12.0', 'Referer': host },
                timeout: 10000 
            });
            let content = typeof res === 'object' ? res.content : res;
            let json = JSON.parse(content);
            let playUrl = json.url || (json.data ? json.data.url : null) || json.vurl;
            
            if (playUrl && playUrl.startsWith('http')) {
                return JSON.stringify({ 
                    parse: 0, 
                    url: playUrl, 
                    header: { 'User-Agent': 'Mozilla/5.0', 'Referer': host } 
                });
            }
        } catch (e) {}
    }
    return JSON.stringify({ parse: 1, url: id, jx: 1 });
}

export function __jsEvalReturn() {
    return { init: () => {}, home, category, detail, play, search };
}