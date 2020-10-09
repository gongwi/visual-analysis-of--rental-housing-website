from spider import MultiThreadedSpider
from pyquery import PyQuery as pq
import pandas as pd

class HouseSpider(MultiThreadedSpider):
    start_urls = ['https://gz.centanet.com/zufang/']
    
    def on_start(self):
        self.data = []


    def process(self, response):
        response.doc.make_links_absolute(base_url="https://gz.centanet.com/")
        for a in response.doc(".house-title a").items():
            self.crawl({
                "url": a.attr("href"),
                
            }, self.detail)
        for a in response.doc(".pager-inner a").items():
            self.crawl(a.attr("href"))
            
    def detail(self, responses):
        data = {
            "租金": responses.doc("#sidefixedbox > div.infotop.infotopB > p > b").text(),
            "使用面积": responses.doc("#sidefixedbox > div.infomid > p.big > span.m_2").text(),
            "朝向": responses.doc("#sidefixedbox > div.infomid > p.small > span.m_1").text(),
            "户型": responses.doc("#sidefixedbox > div.infomid > p.big > span.m_1").text(),
            "装修情况": responses.doc("#sidefixedbox > div.infomid > p.small > span.m_2").text(),
            "年份": responses.doc("#sidefixedbox > div.infomid > p.small > span.m_3").text(),
            "车位": responses.doc("body > div.section-wrap.section-detailbox > div > div.housedetail-main > div.baseinflayer > div > ul > li:nth-child(5) > span.td").text(),
            "电梯": responses.doc("body > div.section-wrap.section-detailbox > div > div.housedetail-main > div.baseinflayer > div > ul > li:nth-child(7) > span.td").text(),
            "区域": responses.doc("body > div.section-wrap.section-breadcrumb.visible-desktop > div > a:nth-child(5)").text(),
            "小区": responses.doc("body > div.section-wrap.section-breadcrumb.visible-desktop > div > a:nth-child(9)").text()
        }
        if responses.data:
            data.update(responses.data)
        self.data.append(data)

    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("zhongyuan.xlsx")

HouseSpider().start()