from spider import MultiThreadedSpider
import pandas as pd


class LianjiaSpider(MultiThreadedSpider):
    start_urls = ["https://gz.lianjia.com/zufang/"]

    def on_start(self):
        self.data = []

    def process(self, response):
        for a in response.doc(".content__list--item--title.twoline a").items():
            if a.text().split("·")[0] == "整租" or a.text().split("·")[0] == "合租":
                self.crawl(a.attr("href"), self.process_detail)
        for i in range(2, 100):
            link = "https://gz.lianjia.com/zufang/pg" + str(i) + "/#contentList"
            self.crawl(link)

    def process_detail(self, response):
        district = response.doc("p.bread__nav__wrapper.oneline > a:nth-child(2)").text()[:2] + "区"
        price = response.doc("div.content__aside--title > span").text()
        rent_way = response.doc("p.content__title").text().split(" ")[0].split("·")[0]
        address = response.doc("p.content__title").text().split(" ")[0].split("·")[1]
        house_type = response.doc("p.content__title").text().split(" ")[1]
        orientation = response.doc("#info > ul:nth-child(2) > li:nth-child(3)").text().split("：")[1]
        area = response.doc("#info > ul:nth-child(2) > li:nth-child(2)").text().split("：")[1]
        floor = response.doc("#info > ul:nth-child(2) > li:nth-child(8)").text().split("：")[1]
        with_elevator = response.doc("#info > ul:nth-child(2) > li:nth-child(9)").text().split("：")[1]
        self.data.append({
            "房源": "链家网",
            "区域": district,
            "具体位置": address,
            "房型": house_type,
            "面积": area,
            "租房方式": rent_way,
            "朝向": orientation,
            "价格": price,
            "楼层": floor,
            "有无电梯": with_elevator
        })

    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("lianjia.xlsx")


LianjiaSpider().start()
