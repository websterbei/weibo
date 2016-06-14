import requests
import codecs
import bs4
from lxml import etree
from PIL import Image
from io import BytesIO
import os

header = {
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Referer": "http://weibo.com/",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
"Cookie": "_T_WM=0a1e1b4580384321343b3e45e7bb6c39; ALF=1468471575; SUB=_2A256W__dDeTxGeNG4loQ8i7IwziIHXVZp4GVrDV6PUJbktBeLRfHkW1kZ54ereOQTQJxiB-04DxzJCC0qw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFf8PnSKEOl2jUn8HY7dQev5JpX5o2p5NHD95Qf1h.ReKz7ShnXWs4DqcjZHcHbMNxLM.iLIBtt; SUHB=0P1MnGsiKYOauC; SSOLoginState=1465880462"
}

zutu = ["组图共2张","组图共3张","组图共4张","组图共5张","组图共6张","组图共7张","组图共8张","组图共9张"]

url = "http://weibo.cn/caijing"

def real_url(url):
	response = session.get(url, headers = header, allow_redirects = False)
	return response.headers["Location"]

def get_page(url):
	return session.get(url, headers = header).text

def save(filename, data):
	f = codecs.open(filename, 'wb', 'utf-8')
	f.write(data)
	f.close()

def get_mp(data):
	#print(data)
	tree = etree.HTML(repr(data))
	nodes = tree.xpath(u'//input[@name = "mp"]')
	return int(nodes[0].attrib.get('value'))

def original_pic_url(data):
	result = []
	tree = etree.HTML(repr(data))
	nodes = tree.xpath(u'//a')
	for node in nodes:
		temp = []
		if node.text == "原图":
			temp.append(node.getparent().getparent().getchildren()[0].getchildren()[0].text)
			temp.append(node.getparent().getchildren()[-1].text.replace(":",""))
			temp.append(real_url(node.attrib.get('href')))
			result.append(temp)
	#print(result)
	return result

def zutu_url(data):
	result = []
	tree = etree.HTML(repr(data))
	nodes = tree.xpath(u'//a')
	for node in nodes:
		if node.text == "原图":
			result.append(real_url("http://weibo.cn" + node.attrib.get('href')))
	return result

def get_combo_url(data, results):
	tree = etree.HTML(repr(data))
	nodes = tree.xpath(u'//a')
	for node in nodes:
		if node.text in zutu:
			temp = node.getparent().getchildren()[0].text
			for i in range(len(results)):
				if temp in results[i]:
					results[i].pop()
					results[i] += zutu_url(get_page(node.attrib.get('href')).text)
	return result

session = requests.Session()
mp = get_mp(get_page(url))

if mp>20:
	mp = 20

f = codecs.open('display.html','wb','utf-8')
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")

for page in range(mp,1,-1):
	result = original_pic_url(get_page(url+"?page={}".format(str(page))))
	result = get_combo_url(page, result)
	for i in result:
		f.write(i[1]+"<br/>")
		f.write(i[0]+"<br/>")
		for j in range(2, len(i)):
			f.write("<img src={} />".format(i[j])+"<br/>"+"<br/>")

f.close()
'''		try:
			os.mkdir(i[1])
		except:
			pass
		for j in range(2, len(i)):
			print(i[j])
			r = session.get(i[j])
			image = Image.open(BytesIO(r.content))
			image.save(i[1]+"/"+str(j)+".jpg")
'''

