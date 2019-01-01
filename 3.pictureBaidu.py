import requests
from bs4 import BeautifulSoup as bs
import json
import re

url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%A3%8E%E6%99%AF&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E9%A3%8E%E6%99%AF&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=60&rn=30&gsm=3c&1546069469049='

#url中查询参数中有3个在变化，最后一个参数解析不了，所以目前只能爬取一页，不能迭代
data = {
	'pn':'300'
	'rn':'30'
	'gsm':'12c'
	'1546069531250':''
	}

#得到给定url的响应
def get_one_url(url):
	headers= {
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
			+ '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
			}
	response = requests.get(url,headers = headers)
	if response.status_code == 200:
		return response.text
	else:
		return None

#用Json解析得到的响应（str格式），得到json格式的数据，再处理
def parse_html_json(html):
	result = json.loads(html)
	if result and 'data' in result.keys():
		for data in result['data']:
			item = {}
			if 'middleURL' in data.keys():
				item['middleURL'] = data['middleURL']
				yield item

#把解析结果的图片储存到本地
def save_picture(url, pic_name):
	response = requests.get(url)
	with open('download/{pic_name}.jpg'.format(pic_name = pic_name), 'wb') as f:
		f.write(response.content)
		f.close()

#运行爬虫，得到响应，解析响应，得到图片url，利用url下载图片
def main():
	html = get_one_url(url)
	result = parse_html_json(html)
	i=50
	for picture in result:
		save_picture(picture['middleURL'],i)
		i+=1

if __name__ == '__main__':
	main()