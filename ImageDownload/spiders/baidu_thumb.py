import requests
import re
import time
import os
import urllib.parse
import json

page_num=30
photo_dir="D:\\data\\pic\\face\\photo"

def getThumbImage(word):
    num=0
    url = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={0}&pn={1}"
    while num<50:

        page_url=url.format(urllib.parse.quote(word),num*page_num)
        print(page_url)
        response=requests.get(page_url)
        pic_urls=re.findall('"thumbURL":"(.*?)",',response.text,re.S)
        
        if pic_urls:
        
            for pic_url in pic_urls:
                name=pic_url.split('/')[-1]
                print(pic_url)
                headers={
                    "Referer":page_url,
                }
                html=requests.get(pic_url,headers=headers,timeout=20)
                with open(os.path.join(word_dir,name),'wb')as f:
                    f.write(html.content)
        num=num+1

def getThumb2Image(word):
    num=0
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={0}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={1}&rn="+str(page_num)+"&gsm=1e&1552975216767="
    while num<50:

        page_url=url.format(urllib.parse.quote(word),num*page_num)
        print(page_url)
        response=requests.get(page_url)
        pic_urls=re.findall('"thumbURL":"(.*?)",',response.text,re.S)
        for pic_url in pic_urls:
            name=pic_url.split('/')[-1]
            print(pic_url)
            headers={
                "Referer":page_url,
            }
            html=requests.get(pic_url,headers=headers)
            with open(os.path.join(word_dir,name),'wb')as f:
                f.write(html.content)
        num=num+1
        

if __name__ == "__main__":
    word = input("请输入搜索关键词(可以是人名，地名等): ")
    word_dir=os.path.join(photo_dir,word)
    if not os.path.exists(word_dir):
        os.mkdir(word_dir)
    getThumb2Image(word)
    
                

