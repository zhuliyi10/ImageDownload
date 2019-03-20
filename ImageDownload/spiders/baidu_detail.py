import requests
import re
import time
import os
import urllib.parse
from lxml import etree
import json
page_num=30
photo_dir="D:\\data\\pic\\face\\photo"


def getDetailImage(word):
    num=0
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={0}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={1}&rn="+str(page_num)+"&gsm=1e&1552975216767="
    while num<50:

        page_url=url.format(urllib.parse.quote(word),num*page_num)
        print(page_url)
        response=requests.get(page_url)
       
        regex = re.compile(r'\\(?![/u"])')
        json_data=json.loads(regex.sub(r"\\\\", response.text))#问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误
        for item in json_data['data']:
            try :
                params={
                    "word":word,
                    "di":item['di'],
                    "tn":"baiduimagedetail",
                    "cs":item['cs'],
                    "os":item['os'],
                }
                detail_url="http://image.baidu.com/search/detail"
                response=requests.get(detail_url,params=params)
                selector = etree.HTML(response.text)
                pic_url=selector.xpath("//img[@id='hdFirstImgObj']/@src")[0]
                print(pic_url)
                name=pic_url.split('/')[-1]
                headers={
                    "Referer":page_url,
                }
            
                html=requests.get(pic_url,headers=headers)
                with open(os.path.join(word_dir,name),'wb')as f:
                    f.write(html.content)
            except:
                pass
            
        num=num+1
        

if __name__ == "__main__":
    word = input("请输入搜索关键词(可以是人名，地名等): ")
    word_dir=os.path.join(photo_dir,word)
    if not os.path.exists(word_dir):
        os.mkdir(word_dir)
    getDetailImage(word)
    
                

