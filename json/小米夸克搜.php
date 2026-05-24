<?php
// 获取用户通过 'wd' 参数传递的搜索文本
// 获取用户通过 'wd' 参数传递的搜索文本
$userSearchText = isset($_GET['wd']) ? $_GET['wd'] : '';

// 准备POST数据
$postData = array(
    'page' => 1,
    'q' => $userSearchText, // 使用用户通过 'wd' 参数传递的搜索文本
    'user' => '',
    'format' => [
        '.mp4', '.mkv', '.flv', '.rmvb', '.wmv', '.3gp', '.mov', '.m4v', '.swf', '.f4v',
        '.webm', '.ogg', '.ogv', '.m3u8', '.mpd', '.avi', '.mpg', '.mpeg', '.mpe', '.mpv',
        '.m2v', '.mxf', '.3g2', '.f4p', '.f4a', '.f4b'
    ],
    'share_time' => '',
    'size' => 5, // 最多返回5个结果
    'type' => 'QUARK'
);

// 将数据编码为JSON格式
$postDataJson = json_encode($postData);

// 设置POST请求的URL
$url = 'https://www.misou.fun/v1/search/disk';

// 初始化cURL会话
$ch = curl_init($url);

// 设置cURL选项
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postDataJson);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Content-Length: ' . strlen($postDataJson))
);

// 执行cURL请求并获取返回的数据
$response = curl_exec($ch);

// 关闭cURL会话
curl_close($ch);

// 解析JSON数据
$data = json_decode($response, true);

// 获取 "list" 部分的内容
$list = isset($data['data']['list']) ? $data['data']['list'] : [];

// 循环遍历 "list"，将 "disk_name" 键名替换为 "vod_name"，将 "shared_time" 键名替换为 "vod_remarks"，将 "link" 键名替换为 "vod_id"，并设置 "disk_type" 替换为 "vod_pic"
foreach ($list as &$item) {
     $item['vod_name'] = str_replace(['<em>', '</em>'], '', $item['disk_name']);
    unset($item['disk_name']);
    
    $item['vod_remarks'] = '上传日期: ' . $item['shared_time'];
    unset($item['shared_time']);
    
    $item['vod_id'] = 'push://' . $item['link'];
    unset($item['link']);
    
    $item['vod_pic'] = "http://pic.uzzf.com/up/2023-7/20237261437483499.png";
    unset($item['disk_type']);
}

// 更新 "list" 部分的内容
$data['data']['list'] = $list;

// 输出更新后的JSON数据
echo json_encode(['list' => $list]);
?>
