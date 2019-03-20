# 美桌 抓明星图片
import scrapy
from ImageDownload.items import ImagedownloadItem

class Win4000(scrapy.Spider):
    name = 'win4000'
    start_urls = [
        "http://www.win4000.com/mt/dilireba.html"
    ]

    def parse(self, response):
        list = response.xpath("//div[@class='Left_bar']//div[@class='tab_box']//li")
        next_page_url = response.xpath("//div[@class='pages']//a[text()='下一页']/@href").extract_first()
        for li in list:
            detail_url = li.xpath(".//a/@href").extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_detail)

        if (next_page_url):
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_detail(self, response):
        item = ImagedownloadItem()
        img_urls = []
        current_page=response.xpath("//div[@class='ptitle']/span/text()").extract_first()
        total_page=response.xpath("//div[@class='ptitle']/em/text()").extract_first()
        next_page_url = response.xpath("//div[@class='pic-next-img']/a/@href").extract_first()
        img_url = response.xpath("//div[@id='pic-meinv']/a/img/@url").extract_first()
        img_urls.append(img_url)
        item['image_urls'] = img_urls
        item['name'] = response.xpath(
            "//div[@class='ptitle']/h1/text()").extract_first()
        yield item
        if (next_page_url and current_page!=total_page):
            yield scrapy.Request(next_page_url, callback=self.parse_detail)