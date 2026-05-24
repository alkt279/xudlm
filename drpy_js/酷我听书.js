var rule = {
  类型: '听书',
  title: '酷我听书',
  host: 'http://tingshu.kuwo.cn',
  url: '/v2/api/search/filter/albums?classifyId=fyfilter&notrace=0&source=kwplayer_ar_9.1.8.1_tvivo.apk&platform=1&kweexVersion=1.1.5&uid=2511482006&sortType=playCnt&loginUid=540339516&bksource=kwbook_ar_9.1.8.1_tvivo.apk&rn=20&categoryId=fyclass&pn=fypage',
  searchUrl: 'http://search.kuwo.cn/r.s?client=kt&all=**&ft=album&newsearch=1&itemset=web_2013&cluster=0&pn=fypage-1&rn=100&rformat=json&encoding=utf8&show_copyright_off=1&vipver=MUSIC_8.0.3.0_BCS75&show_series_listen=1&version=9.1.8.1',
  searchable: 2,
  quickSearch: 0,
  filterable:1,
  filter_url:"{{fl.class or '44'}}",
  filter:{
        "2":[{"key":"class","name":"类型","value":[{"n":"玄幻奇幻","v":"44"},{"n":"武侠仙侠","v":"48"},{"n":"穿越架空","v":"52"},{"n":"都市传说","v":"42"},{"n":"科幻竞技","v":"57"},{"n":"幻想言情","v":"169"},{"n":"独家定制","v":"170"},{"n":"古代言情","v":"207"},{"n":"影视原著","v":"213"},{"n":"悬疑推理","v":"45"},{"n":"历史军事","v":"56"},{"n":"现代言情","v":"41"},{"n":"青春校园","v":"55"},{"n":"文学名著","v":"61"}]}],
        "37":[{"key":"class","name":"类型","value":[{"n":"抖音神曲","v":"253"},{"n":"怀旧老歌","v":"252"},{"n":"创作翻唱","v":"248"},{"n":"催眠","v":"254"},{"n":"古风","v":"255"},{"n":"博客周刊","v":"1423"},{"n":"民谣","v":"1409"},{"n":"纯音乐","v":"1408"},{"n":"3D电音","v":"1407"},{"n":"音乐课程","v":"1380"},{"n":"音乐推荐","v":"250"},{"n":"音乐故事","v":"247"},{"n":"情感推荐","v":"246"},{"n":"儿童音乐","v":"249"}]}],
        "5":[{"key":"class","name":"类型","value":[{"n":"相声新人","v":"222"},{"n":"张少佐","v":"313"},{"n":"刘立福","v":"314"},{"n":"评书大全","v":"220"},{"n":"小品合辑","v":"221"},{"n":"刘兰芳","v":"309"},{"n":"连丽如","v":"311"},{"n":"田占义","v":"317"},{"n":"单口相声","v":"219"},{"n":"袁阔成","v":"310"},{"n":"孙一","v":"315"},{"n":"王玥波","v":"316"},{"n":"单田芳","v":"217"},{"n":"热门相声","v":"218"},{"n":"相声名家","v":"290"},{"n":"粤语评书","v":"320"},{"n":"关永超","v":"325"},{"n":"马长辉","v":"326"},{"n":"赵维莉","v":"327"},{"n":"单口相声","v":"1536"},{"n":"潮剧","v":"1718"},{"n":"沪剧","v":"1719"},{"n":"晋剧","v":"1720"}]}],
        "62":[{"key":"class","name":"类型","value":[{"n":"影视广播剧","v":"1485"},{"n":"影视解读","v":"1483"},{"n":"影视原著","v":"1486"},{"n":"陪你追剧","v":"1398"},{"n":"经典原声","v":"1482"}]}]
    },

  timeout: 5000,
  class_name: '有声小说&音乐&相声评书&影视原声',
  class_url: '2&37&5&62',
  play_parse: true,
  lazy: $js.toString(()=>{
        let html = request(input);
        let url = JSON.parse(html).data.url;
      input = {url: url,parse: 0}
  }),
  double: true,
 一级: $js.toString(()=>{
        let d = [];
        let html = request(input);
        let data = JSON.parse(html).data.data;
        data.forEach(it => {
            let id = 'http://search.kuwo.cn/r.s?stype=albuminfo&user=8d378d72qw28f5f4&uid=2511552006&loginUid=540129516&loginSid=958467960&prod=kwplayer_ar_9.1.8.1&bkprod=kwbook_ar_9.1.8.1&source=kwplayer_ar_9.1.8.1_tvivo.apk&bksource=kwbook_ar_9.1.8.1_tvivo.apk&corp=kuwo&albumid='+it.albumId+'&pn=0&rn=5000&show_copyright_off=1&vipver=MUSIC_8.2.0.0_BCS17&mobi=1&iskwbook=1';
            d.push({
            url:id,
            title:it.albumName,
            img:it.coverImg,
            desc:it.title,
        })
        })
       setResult(d);
    }),
    二级: $js.toString(()=>{
        let urls = [];
        let html = request(input);
        let data = JSON.parse(html).musiclist;
        data.forEach(it => {
            urls.push(it.name+'$'+'http://mobi.kuwo.cn/mobi.s?f=web&source=kwplayerhd_ar_4.3.0.8_tianbao_T1A_qirui.apk&type=convert_url_with_sign&rid='+it.musicrid+'&br=320kmp3');
        })
    VOD = {
            vod_play_from: '球球啦',
            vod_play_url: urls.join('#')
        };
    }),
  搜索: $js.toString(()=>{
        let d = [];
        log(input)
        let html = request(input);
        let data = JSON5.parse(html).albumlist;
        log(data)
        data.forEach(it => {
            let id = 'http://search.kuwo.cn/r.s?stype=albuminfo&user=8d378d72qw28f5f4&uid=2511552006&loginUid=540129516&loginSid=958467960&prod=kwplayer_ar_9.1.8.1&bkprod=kwbook_ar_9.1.8.1&source=kwplayer_ar_9.1.8.1_tvivo.apk&bksource=kwbook_ar_9.1.8.1_tvivo.apk&corp=kuwo&albumid='+it.DC_TARGETID+'&pn=0&rn=5000&show_copyright_off=1&vipver=MUSIC_8.2.0.0_BCS17&mobi=1&iskwbook=1';
            d.push({
            url:id,
            title:it.name,
            img:it.img,
        })
        })
       setResult(d);
    })
}