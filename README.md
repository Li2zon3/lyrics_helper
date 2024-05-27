一、功能：

1.歌词翻译与排版

许多歌词为外文，即使自行翻译，也不便实现一行歌词一行译文的排版效果。

通过本脚本，输入以每行一句的格式排版的歌词，可以将其翻译为中文（支持百度、谷歌翻译）,并实现一行歌词+一行译文的排版效果。

注：

百度翻译须自备api及密钥，免费注册即可（http://api.fanyi.baidu.com/api/trans/product/index/）。

谷歌翻译无须api，但须挂梯子。

2.检索、爬取歌词

输入歌曲标题，可在百度、谷歌、genius检索歌曲，

在百度检索到歌曲后，进一步爬取网易云、酷我两个音乐源的歌词；

在谷歌检索到歌曲后，进一步爬取uta-net音乐源的歌词；

在genius检索到歌曲后，进一步爬取该音乐源的歌词。

注：

之所以要通过百度、谷歌检索，而不是直接在网易云、酷我等音乐源检索，是因为歌曲id不易爬取，要借助百度、谷歌检索作为中介获取歌曲id。

为方便检索，在通过百度检索时，可输入“歌曲标题+网易云/酷我”；在通过谷歌检索时，可输入“歌曲标题+uta-net”。

genius须自备api，免费注册即可（https://genius.com/developers）。

3.后续将加入更多音乐源，将引入gui。

二、使用：

1.下载必要的库：requests,bs4,pygtrans,json,random,hashlib,re,os。

2.运行py文件。


