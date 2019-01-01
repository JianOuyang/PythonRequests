import requests
import json
import re
from multiprocessing import Pool
from requests.exceptions import RequestException
import pymongo

#保存到mongodb数据库相关
client = pymongo.MongoClient('localhost', 27017)
db = client.maoyan

def save_to_mongodb(content):
	try:
		if db.movies.insert(content):
			print("保存成功")
	except Exception:
		print('保存失败', content)

#得到给定url的响应
def get_one_url(url):
	headers= {
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
			+ '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
			}
	try:
		response = requests.get(url,headers=headers)
		return response.text
	except RequestException:
		print("请求失败，请重试")
		return None

#用正则表达式解析得到的响应（str格式）
def parse_html(html):
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)"'
		+'.*?data-src="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?'
		+'fraction">(.*?)</i>.*?</dd>', re.S)
	result = re.findall(pattern,html)
	for item in result:
		yield{
			'index': item[0],
			'name': item[1],
			'address':item[2].strip(),
			'stars':item[3].strip()[3:],
			'time':item[4][5:],
			'score':item[5]+item[6]
		}

#解析得到的数据储存为txt格式的文件
def write_to_file(content):
	with open('download/result.txt','a',encoding ='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False) + '\n')
		f.close()

#执行函数，根据offset进行翻页
def main(offset):	
	url = 'https://maoyan.com/board/4?offset='+ str(offset)
	html = get_one_url(url)
	result = parse_html(html)
	for item in result:
		print(item) #显示爬取结果
		#save_to_mongodb(item) #把爬取结果储存到数据库
		#write_to_file(item) #把爬取结果储存为txt文件

if __name__ == '__main__':
	for i in range(10):
		main(i*10)
	#利用多线程进行处理，提高爬虫效率
	# pool = Pool()
	# pool.map(main,[i*10 for i in range(10)])
