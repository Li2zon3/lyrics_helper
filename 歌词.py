import os
import re
import hashlib
import random
import json
from bs4 import BeautifulSoup
import requests
from pygtrans import Translate

print('短时间内请求太多次可能被封锁ip，请过一段时间采尝试，或者更换ip\nRequests too many times in a short period of time may be blocked, so please try after a while, or change the IP')
newline = os.linesep
path = input('请输入存储路径：(绝对路径)\n为了复用时避免重复输入，可注释掉本行，并将代码第150行path变量替换为您自己的存储路径\nPlease enter the storage path: (absolute path)\nTo avoid retyping when reusing, you can comment out this line and replace the path variable on line 150 of the code with your own storage path')
title = str(input('请输入歌曲标题：(为限缩检索范围，可附带歌曲其他特征[如歌手]，或者附带网易云、酷我、uta-net等音乐源)\nPlease enter the title of the song: (to narrow the search scope, you can attach other characteristics of the song [such as singer], or attach music sources such as NetEase Cloud, Kuwo, UTA-Net, etc.)'))
lyric = str(input('是否检索歌词？(输入序号，如不检索直接按回车)\n1.百度\n2.谷歌(须挂梯子)\n3.Genius(须自备genius api)\nDo you want to search for lyrics? (Enter serial number, if not searching, press enter directly) \n1. Baidu \n2. Google \n3. Genius (requires self-provided Genius API)'))
if lyric == '1':
    url = 'https://www.baidu.com/s'
    params = {
        "wd": title
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.find_all('h3', class_='t')
    # summaries = soup.find_all('div', class_='c-abstract')
    dic = {}
    for name in names:
        # f'{titles.index(title)}.{title}'
        t = re.compile(r'blank">.+').findall(str(name))
        t1 = re.sub(r'</a></h3>|blank">|<em>|</em>|<!--s-text-->|<!--/s-text-->', '', t[0])
        print(f'{names.index(name) + 1}.{t1}')
        dic[f'{names.index(name) + 1}'] = t1
        print(f"url={name.a['href']}")
        # print(f'简介：{summaries[titles.index(title)]}')
        print('')
    urls = [name.a['href'] for name in names]

    num = int(input('输入序号：(支持网易云音乐、酷我音乐)\nEnter the serial number: (support NetEase Cloud Music, Kuwo Music)'))
    url_ = urls[num - 1]
    resp = requests.get(url=url_, headers=headers)
    soup_ = BeautifulSoup(resp.text, 'html.parser')
    if '网易' in dic[str(num)]:
        url__ = soup_.find(name='link')['href']
        song_id = re.sub(r'https://music.163.com/song\?id=', '', url__)
        url_2 = 'http://music.163.com/api/song/lyric?' + 'id=' + song_id + '&lv=1&kv=1&tv=-1'
        r = requests.get(url_2, headers=headers, allow_redirects=False)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        json_obj = json.loads(r.text)
        lrc = json_obj["lrc"]["lyric"]
        regex = re.compile(r'\[.*\]')
        final_lyric = re.sub(regex, '', lrc)
        if final_lyric:
            print(final_lyric)
        else:
            print('未检索到歌词，请尝试其他来源或自行获取歌词\nNo lyrics were retrieved, try a different source or get the lyrics yourself')

    elif '酷我' in dic[str(num)]:
        ids = soup_.find_all(name='link', attrs={'data-n-head': "ssr"})
        url_kuwo = str(ids[-1])
        kuwo_id = re.sub(r'.+play_detail/|" rel=.+', '', url_kuwo)
        url_3 = f"http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={kuwo_id}"
        r = requests.get(url=url_3, headers=headers).json()
        lrc_list = r.get('data', {}).get('lrclist', [{1: '无歌词', 2: '0'}])
        final_lyric = ''
        if lrc_list:
            for l in lrc_list:
                final_lyric += l['lineLyric'] + '\n'
            print(final_lyric)
        else:
            print('未检索到歌词，请尝试其他来源或自行获取歌词\nNo lyrics were retrieved, try a different source or get the lyrics yourself')

elif lyric == '2':
    url = f"http://google.com/search?q={title}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    gs = soup.find_all('div', class_='g')
    for g in gs:
        anchors = g.find_all('a')
        if anchors:
            if 'href' in anchors[0].attrs:
                link = anchors[0]['href']
                title_list = list(g.find_all('h3'))
                if len(title_list) > 0:
                    title_str = title_list[0]
                    title_soup = BeautifulSoup(str(title_str), 'html.parser')
                    title_text = title_soup.get_text()
                    print(f'{gs.index(g) + 1}.{title_text}')
                    print(f'url={link}')
                    title_soup.clear()
                    item = {
                        "title": title_text,
                        "link": link
                    }
                    results.append(item)

    num = int(input('输入序号：(支持uta-net)\nEnter serial number: (supports uta-net)'))
    if 'uta-net' in results[num - 1]["link"]:
        response = requests.get(url=results[num - 1]["link"], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        lyric = soup.find(attrs={'id': "kashi_area"})
        lyric_ = re.sub(r'<div id="kashi_area" itemprop="text">|</div>', '', str(lyric))
        final_lyric = re.sub(r'<br/>', '\n', lyric_)
        print(final_lyric)

elif lyric == '3':
    print('为避免重复输入，可注释掉代码第114、115行，并将第124行genius_api变量替换为您个人的数据\nTo avoid re-entry, you can comment out lines 114 and 115 of the code and replace the variables genius_api line 124 with your personal data')
    genius_api = str(input('请输入genius api:'))
    url = ' https://api.genius.com/search'
    params = {
        "q": title
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Host': 'api.genius.com',
        'Authorization': f'Bearer {genius_api}'
    }
    respon = requests.get(url=url, params=params, headers=headers)
    songs = json.loads(respon.text)
    song_search_result = songs['response']['hits']
    for i in song_search_result:
        number = song_search_result.index(i) + 1
        api_path = i['result']['api_path']
        artist_names = re.sub(r'\\u200b', '', i['result']['artist_names'])
        full_title = re.sub(r'\\u200b', '', i['result']['full_title'])
        full_title = re.sub(r'\\xa0', ' ', full_title)
        print(f'{number}.{full_title}\nurl=https://api.genius.com{api_path}')
    number_ = input('请输入序号：\nPlease enter the serial number:')
    song_path = song_search_result[int(number_) - 1]['result']['path']
    song_url = 'https://genius.com' + song_path
    respo = requests.get(url=song_url)
    html = BeautifulSoup(respo.text, 'html.parser')
    lyrics = html.find_all(attrs={'data-lyrics-container': "true"})
    final_lyric = ''
    for i in lyrics:
        i = re.sub(r'.+data-lyrics-container="true">|</div>', '', str(i))
        i = re.sub(r'<br/>', '\n', i)
        final_lyric += i
    print(final_lyric)

text = str(input('请输入格式调整好的歌词：(若无，不必输入，直接按回车；使用已检索到的、格式调整好的[!]歌词则输入1)\nPlease enter the formatted lyrics: (If none, do not enter, press enter directly; if using the retrieved and formatted [!] lyrics, enter 1)'))
file = open(f'{path}/{title}.txt', 'w')
if text == '1':
    print(final_lyric, file=file)
    file.close()
elif text:
    print(text, file=file)
    file.close()
else:
    text0 = str(input('请输入原歌词：（每行一句歌词；使用已检索到的歌词则输入1）\nPlease enter the original lyrics: (Each line has one lyric; if using retrieved lyrics, enter 1)'))
    if text0 == '1':
        text0 = final_lyric
    text1 = text0.split(newline)
    text2 = str(input('请输入翻译歌词：(每行一句歌词；若无，不必输入，直接按回车)\nPlease enter the translated lyrics: (Each line has one lyric; if not, do not enter, press enter directly)'))
    if text2:
        text3 = text2.split(newline)
    else:
        n = str(input('请选择翻译引擎：1.百度（须自备api账号密钥） or 2.谷歌(须挂梯子)\n可复选(但挂梯子时有可能无法链接百度翻译)，即输入12\nPlease select the translation engine: 1.Baidu (you must bring your own API account key) or 2.Google\nYou can select both, that is, enter 12'))
        print("if you want to translate lyrics into English instead of Chinese, change 'zh' in lines 170,199 of the code to 'en'")
        if '2' in n:
            client = Translate()
            text3 = client.translate(text1, target='zh') # if you want to translate lyrics into English instead of Chinese, change 'zh' here to 'en'
        if '1' in n:
            print('为了复用时避免重复输入，可注释掉代码第170-173行，并将代码第194、199、201行appid,key变量替换为您自己的数据\nTo avoid repeated input, you can comment out lines 170-173 of the code and replace the appid and key variables on lines 194, 199, and 201 with your own data')
            appid = input('输入百度翻译appid\nEnter the Baidu Translate appid')
            key = input('输入百度翻译key\nEnter the Baidu Translate key')

    for i in range(len(text1)):
        print(text1[i], file=file)
        if text2:
            print(text3[i], file=file)

        if '2' in n:
            text4 = re.sub('[^\u4e00-\u9fa5]+', '', str(text3[i]))
            print(text4, file=file)

        if '1' in n:
            def generate_sign(appid, q, salt, key):
                str1 = appid + q + salt + key
                sign = hashlib.md5(str1.encode("utf-8")).hexdigest()
                return sign


            def get_res_from_baidu():
                salt = str(random.randint(1, 1000))
                QUERY = text1[i]
                sign = generate_sign(str(appid), QUERY, salt, str(key))
                params = {
                    'q': QUERY,
                    'from': 'auto',
                    'to': 'zh', # if you want to translate lyrics into English instead of Chinese, change 'zh' here to 'en'
                    'appid': int(appid),  # 此处'appid'是整数类型，不是字符串类型！！！
                    'salt': salt,
                    'key': str(key),
                    'sign': sign
                }
                res = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', params=params)
                res.raise_for_status()
                return res


            def parse_content(json_str):
                a_dic = json.loads(json_str)
                trans_result = a_dic['trans_result']
                dst = trans_result[0]['dst']
                return dst


            try:
                # time.sleep(1) 如果百度翻译非高级用户，每次请求须间隔1秒
                res = get_res_from_baidu()
                content = parse_content(res.text)
                print(content, file=file)

            except:
                print('', file=file)

        print('', file=file)

    file.close()
print('任务完成，感谢使用\nTask completed. Thank you for using it')
