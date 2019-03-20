import requests
import re
import time
import os
import urllib.parse
from lxml import etree
import json
page_num=25
photo_dir="D:\\data\\pic\\face\\photo"


def getDetailImage(word):
    num=0
    url = "https://cn.bing.com/images/api/custom/search?q={0}&id=88B083730BB7407A9B0B414F4DE653463CD2C1AB&preserveIdOrder=1&count=25&offset={1}&skey=9YDqrnxwleAyF_tM1baJDFCU1uawiYJBeZAvcFe_n5c&safeSearch=Strict&IG=43B809AC4CF3451BB419D4305F6F2A8C&IID=idpfs&SFX=1"
    cookie='MMCA=ID=709A5400E72D4E8589F395E695E26A77; _IDET=NVNoti=1&MIExp=0&InsSte=0110001; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=463CC12121EE4D289CE9CF25145798C1&dmnchg=1; _EDGE_V=1; MUID=36CD135CA3596D4D2A151E41A2776C3B; MUIDB=36CD135CA3596D4D2A151E41A2776C3B; _ITAB=STAB=TR; ENSEARCH=BENVER=1; ULC=P=7A57|1:1&H=7A57|1:1&T=7A57|1:1; SRCHUSR=DOB=20190312&T=1552487956000; SRCHHPGUSR=CW=925&CH=888&DPR=1&UTC=480&WTS=63688084725; _SS=SID=394950C46034692825685DE1611A6872; _EDGE_S=SID=394950C46034692825685DE1611A6872'

    lines=cookie.split(';')
    cookies={}
    for line in lines:
        key,value=line.split('=',1)
        cookies[key.strip()]=value
    print(cookies)
    while num<100:

        page_url=url.format(word,num*page_num)
        print(page_url)
        response=requests.get(page_url,cookies=cookies)
       
        datas=json.loads(response.text)
        for item in datas['value']:
            try :
                pic_url=item['contentUrl']
                print(pic_url)
                if not (pic_url.endswith('.jpg') or pic_url.endswith('.jpeg') or pic_url.endswith('.png')):
                    pic_url=pic_url+".jpg"
                name=pic_url.split('/')[-1]
                html=requests.get(pic_url)
                with open(os.path.join(word_dir,name),'wb')as f:
                    f.write(html.content)
                time.sleep(1)
            except:
                pass
            
        num=num+1
        

if __name__ == "__main__":
    word = input("请输入搜索关键词(可以是人名，地名等): ")
    word_dir=os.path.join(photo_dir,word)
    if not os.path.exists(word_dir):
        os.mkdir(word_dir)
    getDetailImage(word)
    
                

