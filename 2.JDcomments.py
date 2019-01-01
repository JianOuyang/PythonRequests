import requests
from bs4 import BeautifulSoup as bs
import json
import re
import urllib

class GetCommentsFromJD(object):
	def __init__(self, url):
		self.url = url
		self.headers = {
				'authority': 'sclub.jd.com',
				'method': 'GET',
				'path': '/comment/productPageComments.action?callback=fetchJSON_comment98vv2229&productId=1263469503&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1',
				'scheme': 'https',
				'accept': '*/*',
				'accept-encoding': 'gzip, deflate, br',
				'accept-language': 'zh-CN,zh;q=0.9',
				'cookie': 'shshshfpa=a0eb0af8-87c5-6e41-cfc2-557bcf152e52-1534606807; shshshfpb=039856a77a876460360ffb9c7ab1e4941a3509e913eb589525b783dd72; __jdu=15346068071891124820695; unpl=V2_ZzNtbRZUFhJ3D0JcKx0OV2IEQF8RUEFAcgsVVClNVQA1BxBZclRCFXwURldnGlUUZwMZXEFcRhNFCHZXfBpaAmEBFl5yAR1LI1USFi9JH1c%2bbUgbF0tAHXIAQFR6EVwBZgsibUFXcxV0OEZQeRxbBGAKE1tCXksVdQtDXXgYWw1jMyJacmdzEnYNRlx6KV01ZjNQCR5XRh1zCUcZex1eAGACFVRDUUMcfQhGV34QXwRgCxZtQ2dA; __jda=122270672.15346068071891124820695.1534606807.1543322928.1545966168.4; __jdc=122270672; __jdv=122270672|google-search|t_262767352_googlesearch|cpc|kwd-296971091509_0_e2d63659a5cc46c3b63d62b1ce84c535|1545966167948; PCSYCityID=1; ipLoc-djd=1-72-2799-0; 3AB9D23F7A4B3C9B=FNZKOJ554PI5HYTIGAZ4LDWV2Z6TIG3ABGMT55XCUW3BGBNREOVOGTYPTUUSPZ4DWOJWUC6C6QVXCPUBAHIM7TO654; shshshfp=43c9f6c8707a7d1b2e8b6b0a62f5a2e0; _gcl_au=1.1.1806758888.1545966177; shshshsID=e80001f7e65b4c7d50ff4b723de535fb_5_1545966206591; __jdb=122270672.5.15346068071891124820695|4.1545966168; JSESSIONID=BD24FBA9592D291441D6B1B472DCD70E.s1',
				'referer': 'https://item.jd.com/1263469503.html',
				'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36}'
			}

	def get_one_html(self):
		response = requests.get(self.url, headers = self.headers)
		if response.status_code ==200:
			return response.text
		else:
			return None

	def parse_html(self, html):
		# pattern = re.compile(r'comments: .?csv',re.S)
		# html = re.search(pattern, html)
		html = json.loads(html[27:-2])#print(len('fetchJSON_comment98vv33640('))
		if html and 'comments' in html.keys():
			comments = html['comments']
			for comment in comments:
				print(comment['content'])

	def working(self):
		html = self.get_one_html()
		self.parse_html(html)

if __name__ == '__main__':
	#不同商品的查询参数不一样
	data = {
		'callback': 'fetchJSON_comment98vv33640',
		'productId': '4193770',
		'score': '1',
		'sortType': '5',
		'page': '1',
		'pageSize': '10',
		'isShadowSku': '0',
		'rid': '0',
		'fold': '1'
	}
	url = 'https://sclub.jd.com/comment/productPageComments.action?' + urllib.parse.urlencode(data)
	GetCommentsFromJD(url).working()