import scrapy

from ImageDownload.items import ImagedownloadItem


class MeiZi(scrapy.Spider):
    name = 'meizi'
    main_url = 'http://www.mmonly.cc'
    start_urls = [
        # 'http://www.mmonly.cc/gqbz/',
        # 'http://www.mmonly.cc/tag/xqx/',
        "http://www.mmonly.cc/tag/90h/"
    ]

    def parse(self, response):
        list = response.xpath("//div[@class='item masonry_brick masonry-brick']")
        next_page_url = response.xpath("//div[@class='wrappic']//li/a[text()='下一页']/@href").extract_first()
        for li in list:
            detail_url = li.xpath(".//a/@href").extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_detail)

        if (next_page_url):
            next_page_url = self.main_url + next_page_url
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = ImagedownloadItem()
        img_urls = []
        next_page_url = response.xpath("//div[@class='pages']//li[@id='nl']/a/@href").extract_first()
        list = response.xpath("//div[@class='photo']//div[@class='big-pic']//p")
        for li in list:
            img_url = li.xpath(".//img/@src").extract_first()
            img_urls.append(img_url)
        item['image_urls'] = img_urls
        item['name'] = response.xpath(
            "//div[@class='photo']/div[@class='wrapper clearfix imgtitle']/h1/text()").extract_first()
        yield item
        if (next_page_url):
            pre_url = response.url.split('/')[-1]
            pre_url = response.url[0:len(response.url) - len(pre_url)]
            next_page_url = pre_url + next_page_url
            yield scrapy.Request(next_page_url, callback=self.parse_detail)
