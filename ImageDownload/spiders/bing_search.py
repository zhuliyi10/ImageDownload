# 美桌 抓取bing搜索图片

import scrapy
import json
import time
from ImageDownload.items import ImagedownloadItem

class BingSearch(scrapy.Spider):
    name = 'bing_search'
    word="苍井空"
    page_num=0
    page_count=25
    main_url="https://cn.bing.com"
    page_url="https://cn.bing.com/images/api/custom/search?q={0}&id=88B083730BB7407A9B0B414F4DE653463CD2C1AB&preserveIdOrder=1&count=25&offset={1}&skey=9YDqrnxwleAyF_tM1baJDFCU1uawiYJBeZAvcFe_n5c&safeSearch=Strict&IG=43B809AC4CF3451BB419D4305F6F2A8C&IID=idpfs&SFX=1"
    # start_urls = [
    #     page_url.format(word,page_num*page_count)
    # ]
    start_url=page_url.format(word,page_num*page_count)
    cookie='MMCA=ID=709A5400E72D4E8589F395E695E26A77; _IDET=NVNoti=1&MIExp=0&InsSte=0110001; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=463CC12121EE4D289CE9CF25145798C1&dmnchg=1; _EDGE_V=1; MUID=36CD135CA3596D4D2A151E41A2776C3B; MUIDB=36CD135CA3596D4D2A151E41A2776C3B; _ITAB=STAB=TR; ENSEARCH=BENVER=1; ULC=P=7A57|1:1&H=7A57|1:1&T=7A57|1:1; SRCHUSR=DOB=20190312&T=1552487956000; SRCHHPGUSR=CW=925&CH=888&DPR=1&UTC=480&WTS=63688084725; _SS=SID=394950C46034692825685DE1611A6872; _EDGE_S=SID=394950C46034692825685DE1611A6872'

    lines=cookie.split(';')
    cookies={}
    for line in lines:
        key,value=line.split('=',1)
        cookies[key.strip()]=value
    print(cookies)
    
    def start_requests(self):
        yield scrapy.Request(self.start_url,dont_filter=True,cookies=self.cookies)

    def parse(self, response):
        self.page_num=self.page_num+1
        print("正在执行"+str(self.page_num)+"次")
        datas=json.loads(response.text)
        data=datas['value']
        if data:
            for item in data:
                
                image_url=item['contentUrl']
                item = ImagedownloadItem()
                img_urls = []
                img_urls.append(image_url)
                item['image_urls'] = img_urls
                item['name']=self.word
                yield item

        if (self.page_num<150):
            next_page_url=self.page_url.format(self.word,self.page_num*self.page_count)
            print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse,cookies=self.cookies)

