from spider import Spider, MultiThreadedSpider
import pandas as pd

class LaptopSpider(MultiThreadedSpider):
    start_urls=["http://gz.ziroom.com/z/r1/?isOpen=0"]
    
    def on_start(self):
        self.data = []
        
    def process(self, response):
        for a in response.doc("div.Z_filter > ul > li:nth-child(3) > div > a + a").items():
            self.crawl(a.attr("href"))
        for a in response.doc("div.info-box > h5 > a").items():
            price = response.doc("section > div.Z_filter > ul > li:nth-child(3) > div > a.active").text()
            page_number = response.doc("#page > a.active").text()
            self.crawl({
                    "url":a.attr("href"), 
                    "price": price,
                    "page_number": page_number
                    }, self.process_detail)
        for a in response.doc("#page > a.next").items():
                self.crawl(a.attr("href"))
                
            
    def process_detail(self, response):
        name = response.doc(".Z_name").text()
        size = response.doc("div.Z_home_b.clearfix > dl:nth-child(1) > dd").text()
        facing = response.doc("div.Z_home_b.clearfix > dl:nth-child(2) > dd").text()
        house_type = response.doc("div.Z_home_b.clearfix > dl:nth-child(3) > dd").text()
        location = response.doc("span.va > span").text()
        floor = response.doc("div.Z_home_info > ul > li:nth-child(2) > span.va").text()
        elevator = response.doc("div.Z_home_info > ul > li:nth-child(3) > span.va").text()
        build_date = response.doc("div.Z_home_info > ul > li:nth-child(4) > span.va").text()
        lock = response.doc("div.Z_home_info > ul > li:nth-child(5) > span.va").text()
        plants = response.doc("div.Z_home_info > ul > li:nth-child(6) > span.va").text()
        
        
        self.data.append({
                "房源": name,
                "价格":  response.data['price'],
                "使用面积": size,
                "朝向": facing,
                "户型": house_type,
                "位置": location,
                "楼层": floor,
                "电梯": elevator,
                "年代": build_date,
                "门锁": lock,
                "绿化": plants,
                "page_number": response.data['page_number']
                })
    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("renting.xlsx")
        
LaptopSpider().start()