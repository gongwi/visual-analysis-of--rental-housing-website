#import requests
#from pyquery import PyQuery as pq
#lis=[''];lis2=[]
#for i in range(2,21):
#    lis.append(f'_{i}')
#for page in lis:
#    html=requests.get(f'http://www.weather.com.cn/index/lssj/index{page}.shtml').content.decode("utf-8")
#    doc=pq(html)
#    lis2.append(doc)
#for item in lis2:
#    for i in item('ul.newList li ').items():
#        with open ('title.txt','a+') as file:
#            file.write(i.text()+'\n')

#通用做法
#from spider import Spider,MultiThreadedSpider
#
#class WestherSpider(MultiThreadedSpider):
#    start_urls=['https://www.webscraper.io/test-sites/e-commerce/static/computers/laptops']
#    
#    
#    def process(self,response):        
#        page_number=response.doc('.caption .active').text()
#        for href in response.doc('.caption a').items():
#            self.crawl({
#                    'url':href.attr('href'),
#                    'page':page_number},
#            self.process_detail)
#            
#        for page in response.doc('.pagination a').items():
#            self.crawl(page.attr('href'))
#            
#    def process_detail(self,response):
#        title=response.doc('div.caption > h4:nth-child(2)').text() 
#        price=response.doc('.price').text()
#        print(title,price)
#        
#WestherSpider().start()

#爬Q房
from spider import MultiThreadedSpider
import pandas as pd
import re

class WestherSpider(MultiThreadedSpider):
    start_urls=['https://guangzhou.qfang.com/rent/f2']
    def on_start(self):
        self.data=[]
    
    def process(self,response):        
        page_number=response.doc('div.page-turning-wrap.page-turning-center.fr.clearfix > p > a.cur').text()
        for href in response.doc('div.list-main-header.clearfix > a').items():
            self.crawl({
                    'url':href.attr('href'),
                    'page_number':page_number
                    },
            self.process_detail)
            
        for page in response.doc('body > div.main-wrap > div > div.main-left.fl > div.main-bottom.clearfix > div.page-turning-wrap.page-turning-center.fr.clearfix > p').items() and response.doc(' div.page-turning-wrap.page-turning-center.fr.clearfix > a.btn-page-turning-next ').items():
            if page.attr('href') != 'javascript:;':
                
                self.crawl(page.attr('href'))
            
    def process_detail(self,response):
        position= re.match('\w{2}',response.doc('body > div.detail-guide.clearfix > div > div > div:nth-child(5) > a').text()).group() + re.match('\w{2}',response.doc('body > div.detail-guide.clearfix > div > div > div:nth-child(7) > a').text()).group()
        garden=response.doc(' ul > li:nth-child(1) > div.text.fl > a').text()
        room=response.doc('div.house-info.clearfix > ul > li:nth-child(1) > .text ').text()
        floor=response.doc('div.house-info.clearfix > ul > li:nth-child(2) > .text ').text()
        square=response.doc('div.house-info.clearfix > ul > li:nth-child(3) > .text ').text()
        structure=response.doc('div.house-info.clearfix > ul > li:nth-child(4) > .text ').text()
        orientation=response.doc('div.house-info.clearfix > ul > li:nth-child(5) > .text ').text()
        decoration=response.doc('div.house-info.clearfix > ul > li:nth-child(6) > .text ').text()
        built=response.doc('div.house-info.clearfix > ul > li:nth-child(7) > .text ').text()
        num=response.doc('div.house-info.clearfix > ul > li:nth-child(8) > .text ').text()
        equipment=response.doc('div.house-info.clearfix > ul > li:nth-child(9) > .text ').text()
        cost=response.doc('div.head-side-top.clearfix > div.head-side-price.fl > span').text() 
        way=response.doc('div.head-side-meta.fl > div:nth-child(1)').text() 
        
        self.data.append({
                '位置':position,
                '小区':garden,
                '房屋户型':room,
                '所在楼层':floor,
                '建筑面积':square,
                '户型结构':structure,
                '房屋朝向':orientation,
                '装修情况':decoration,
                '建筑年代':built,
                '房源编号':num,
                '配备电梯':equipment,
                "租金/元":cost,
                "出租方式":way
                        })
      
       
    def on_end(self):
        df=pd.DataFrame.from_dict(self.data)
        df.to_excel('Q房.xlsx')
        
WestherSpider().start()