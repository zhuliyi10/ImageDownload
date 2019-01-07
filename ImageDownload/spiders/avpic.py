import scrapy

from ImageDownload.items import ImagedownloadItem


class MeiZi(scrapy.Spider):
    name = 'avpic'
    main_url = 'https://www.8898jj.com'
    start_urls = [
        "https://www.8898jj.com/html/news/69/"
    ]

    def parse(self, response):
        list = response.xpath("//li[@class='col-md-3 col-sm-6 col-xs-12 clearfix news-box']")
        next_page_url = response.xpath("//div[@class='box-page clearfix']//li/a[text()='下一页']/@href").extract_first()
        for li in list:
            detail_url = li.xpath(".//a/@href").extract_first()
            detail_url=self.main_url+detail_url
            yield scrapy.Request(detail_url, callback=self.parse_detail)

        if (next_page_url):
            next_page_url = self.main_url + next_page_url
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = ImagedownloadItem()
        img_urls = []
        list = response.xpath("//div[@class='details-content text-justify']//img")
        for li in list:
            img_url = li.xpath("./@src").extract_first()
            img_urls.append(img_url)
        item['image_urls'] = img_urls
        item['name'] = response.xpath(
            "//div[@class='news_details']/h1/text()").extract_first()
        yield item
