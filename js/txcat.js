import { load, _ } from 'assets://js/lib/cat.js';

const host = 'https://v.qq.com';
const apihost = 'https://pbaccess.video.qq.com';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36';

let danmakuAPI = '';

async function init(cfg) {
    danmakuAPI = cfg.ext || '';
}

async function request(baseUrl, apiPath, params = {}, method = 'get') {
    const url = `${baseUrl}/${apiPath}`;
    let reqOptions = {
        method: method,
        headers: {
            'User-Agent': UA,
            'Referer': host,
            'Origin': host
        }
    };

    if (method.toLowerCase() === 'get') {
        const queryString = Object.entries(params)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('&');
        reqOptions.url = queryString ? `${url}?${queryString}` : url;
    } else {
        reqOptions.body = JSON.stringify(params);
        reqOptions.headers['Content-Type'] = 'application/json';
        reqOptions.url = url;
    }

    try {
        const res = await req(reqOptions.url, reqOptions);
        return res.content ? JSON.parse(res.content) : {};
    } catch (e) {
        return {};
    }
}

async function home() {
    const classes = [
        { type_id: '100113', type_name: '电视剧' },
        { type_id: '100173', type_name: '电影' },
        { type_id: '100109', type_name: '综艺' },
        { type_id: '100105', type_name: '纪录片' },
        { type_id: '100119', type_name: '动漫' },
        { type_id: '100150', type_name: '少儿' },
        { type_id: '110755', type_name: '短剧' }
    ];
    return JSON.stringify({ class: classes });
}

async function homeVod() {
    return JSON.stringify({ list: [] });
}

async function category(tid, pg, filter, extend) {
    const url = `trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData?video_appid=1000005&vplatform=2&vversion_name=8.9.10`;
    const sdk_page_ctx = { "page_offset": pg, "page_size": 1, "used_module_num": Number(pg) + 1 };

    const res = await request(apihost, url, {
        "page_params": {
            "channel_id": tid,
            "filter_params": "sort=75&itype=-1&ipay=-1&iarea=-1&iyear=-1",
            "page_type": "channel_operation",
            "page_id": "channel_list_second_page"
        },
        "page_context": {
            "sdk_page_ctx": JSON.stringify(sdk_page_ctx),
            "page_index": pg
        }
    }, "POST");

    let result = [];
    try {
        result = res.data.module_list_datas[0].module_datas[0].item_data_lists.item_datas.filter(item => item.item_type === "2");
    } catch (e) {}

    return JSON.stringify({
        page: parseInt(pg) || 1,
        list: (result || []).map(i => ({
            vod_id: i.item_params.cid + "&&&" + i.item_params.title + "&&&" + (i.item_params.second_title || ""),
            vod_name: i.item_params.title,
            vod_pic: i.item_params.new_pic_vt,
            vod_year: i.item_params.year,
            vod_remarks: i.item_params.second_title
        }))
    });
}

async function detail(id) {
    let [cid, title, second_title] = id.split("&&&");
    let next_page_context = "";
    const url = "trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData?video_appid=3000010&vplatform=2";
    const allData = [];

    while (true) {
        const requestData = {
            "page_params": {
                "req_from": "web_vsite",
                "page_id": "vsite_episode_list",
                "page_type": "detail_operation",
                "id_type": "1",
                "cid": cid,
                "page_context": next_page_context,
                "detail_page_type": "1"
            }
        };

        const res = await request(apihost, url, requestData, "POST");
        try {
            const currentPageData = res.data.module_list_datas[0].module_datas[0].item_data_lists.item_datas;
            allData.push(...currentPageData);
            next_page_context = res.data.module_list_datas[0].module_datas[0].module_params.next_page_context;
            if (!next_page_context) break;
        } catch (e) {
            break;
        }
    }

    const playUrl = allData
        .filter(item => item.item_params && item.item_params.play_title && !item.item_params.play_title.includes("预"))
        .map(item => {
            const ep_title = item.item_params.title;
            const ep_url = `https://v.qq.com/x/cover/${cid}/${item.item_id}.html`;
            return `${ep_title}$${ep_url}`;
        }).join('#');

    return JSON.stringify({
        list: [{
            vod_id: cid,
            vod_name: title,
            vod_content: second_title || '',
            vod_play_from: '腾讯视频',
            vod_play_url: playUrl
        }]
    });
}

// ==================== 内置解析核心（替换你原来的 play）====================
async function play(flag, id, flags) {
    try {
        // 这里换成你想用的解析接口 ↓↓↓
        let api = `${encodeURIComponent(id)}`;
        let res = await req(api, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'Referer': 'https://v.qq.com'
            },
            timeout: 15000
        });
        let json = JSON.parse(res.content);
        let playUrl = json.url || json.data || json.m3u8;

        if (playUrl) {
            return JSON.stringify({
                parse: 0,
                url: playUrl,
                header: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                    'Referer': 'https://v.qq.com'
                }
            });
        }
    } catch (e) {}

    // 解析失败兜底
    return JSON.stringify({
        jx: 1,
        url: id,
        danmaku: danmakuAPI ? danmakuAPI + id : ""
    });
}

// ====================================================================

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (Math.random() * 16) | 0, v = c == 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

async function search(wd, quick) {
    let url = "trpc.videosearch.mobile_search.MultiTerminalSearch/MbSearch?vplatform=2";
    const uuid = uuidv4().toUpperCase();
    const res = await request(apihost, url, {
        "query": wd,
        "pagenum": 0,
        "pagesize": 30,
        "uuid": uuid,
        "extraInfo": { "isNewMarkLabel": "1" }
    }, "POST");

    let result = [...(res.data.normalList?.itemList || [])];
    if (res.data.areaBoxList) {
        result = res.data.areaBoxList.reduce((acc, box) => acc.concat(box.itemList || []), result);
    }

    let vod = result
        .filter(i => i.doc && i.doc.dataType === 2)
        .map(i => ({
            vod_id: i.doc.id + "&&&" + i.videoInfo.title + "&&&" + (i.videoInfo.descrip || ""),
            vod_name: i.videoInfo.title,
            vod_pic: i.videoInfo.imgUrl,
            vod_remarks: i.videoInfo.descrip
        }));

    return JSON.stringify({ list: vod });
}

export function __jsEvalReturn() {
    return { init, home, homeVod, category, detail, play, search };
}
