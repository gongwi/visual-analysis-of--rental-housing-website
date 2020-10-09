from spider import Spider, MultiThreadedSpider
import pandas as pd

class FangSpider(MultiThreadedSpider):
    start_urls = ["https://gz.zu.fang.com"]

    
    def on_start(self):
        self.data = []
            
    def process(self, response):
        
        url_1 = "https://gz.zu.fang.com"
        url_2 = '/house/i3'
        for pageNum in range (2,101):

            href = url_1 + url_2 + str(pageNum) + '/'
            self.crawl(href)
            
            for list in response.doc(".list").items():
           
                房子标题 = list(".title a").text()
                detail = list(".rel .bold").text()
                出租方式, 户型, 面积字段, 朝向 = detail.split('|')
                面积 = 面积字段.split('�')[0]
                价格 = list(".mt5").text()
                地址 = list(".gray6").text().split('  ')[0]
                self.data.append({
                    "房源": '房天下',
                    "房子标题": 房子标题,
                    "出租方式": 出租方式,
                    "户型": 户型,
                    "面积": 面积,
                    "朝向": 朝向,
                    "价格": 价格,
                    "地址": 地址
                    })
            
    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("Fang.xlsx")
        print(self)

FangSpider().start()