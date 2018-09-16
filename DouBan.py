# @Author  : ShiRui

import requests
from bs4 import BeautifulSoup
import re


class Spider(object):

	# 初始话变量
	def __init__(self):

		self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
		}
		self.data_short = []
		self.data_praise = []

	# 1.获取页面resource
	def getHtmlResourceByUrl(self, url):

		html = requests.get(url, self.header).text
		soup = BeautifulSoup(html, 'lxml')
		return soup

	# 2.解析页面、提取信息
	def analysisHtml(self, url):

		soup = self.getHtmlResourceByUrl(url)
		short = soup.select('.short')
		for each in short:
			each = str(each)
			pattern = re.compile(r'<span class="short">(.*?)</span>', re.S)
			text = re.findall(pattern, each)[0]
			self.data_short.append(text)

		praise = soup.find_all(attrs={'class': 'votes'})
		pattern = re.compile(r'<span class="votes">(.*?)</span>', re.S)
		for p in praise:
			p = str(p)
			num = re.findall(pattern, p)[0]
			self.data_praise.append(num)

	# 3.保存数据
	def writeData(self):

		for keys, values in zip(self.data_short, self.data_praise):
			with open("info.txt", 'a', encoding="utf-8") as f:
				f.write("短评：%s 点赞数为：%s" % (keys, values))
				f.write("\n")

if __name__ == '__main__':

	spider = Spider()
	for i in range(0, 10):

		url = "https://movie.douban.com/subject/26336252/comments?start={}&limit=20&sort=new_score&status=P".format(i*20)
		spider.analysisHtml(url)
		print("正在爬取第%s页数据" % (i+1))
		spider.writeData()
