# 抓取百度图片
import scrapy
from ImageDownload.items import ImagedownloadItem
import json
import time

class BaiduImg(scrapy.Spider):
    name = 'baidu_img'
    word="迪丽热巴"
    page_num=0
    page_count=30
    page_url="http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}&cl=2&lm=-1&hd=&latest=&copyright=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word={0}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&pn={1}&rn=30&gsm=5a&1552479745395="
    start_urls = [
        page_url.format(word,page_num*page_count)
    ]

    

    def parse(self, response):
        self.page_num=self.page_num+1
        print("正在执行"+str(self.page_num)+"次")
        next_page_url=self.page_url.format(self.word,self.page_num*self.page_count)
        if (self.page_num<100):
            yield scrapy.Request(next_page_url, callback=self.parse)
        datas=json.loads(response.text)
        data=datas['data']
        if data:
            for item in data:
                url_list=item['replaceUrl']
                if len(url_list)>1:
                    image_url=url_list[1]['ObjURL']
                    # image_url=item['middleURL']
                    title=item['fromPageTitleEnc']
                    item = ImagedownloadItem()
                    img_urls = []
                    img_urls.append(image_url)
                    item['image_urls'] = img_urls
                    item['name']=title
                    yield item
                    
        
        
        
        
        
