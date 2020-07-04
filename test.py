import requests, re
share = '#这条街最亮的仔 https://v.douyin.com/JL4b4Ff/ 复制此链接，打开【抖音短视频】，直接观看视频！'
pat = '(https://v.douyin.com/.*?/)'
url = re.compile(pat).findall(share)[0]  #正则匹配分享链接
headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3904.108 Safari/537.36'
}
r = requests.get(url, headers=headers)
print(r.text)
# pat = 'playAddr: "(.*?)",'
# play = re.compile(pat).findall(r.text)[0].replace("playwm", "play")
# headers = {
# 	'user-agent': 'Android',
# }
# r = requests.get(play, headers=headers, allow_redirects=False)
# playurl = r.headers['location']
# print("\n视频地址：" + playurl)



