# -*- coding=utf-8 -*-
import urllib2
import urllib
import bs4
from bs4 import BeautifulSoup
import logging
import os
import time
import glob
import codecs

logging.basicConfig(level=logging.INFO)

def timestamp():
    return time.asctime(time.localtime(time.time()))

def parse_html(html):
    soup = BeautifulSoup(html,"lxml")
    logging.debug(soup.prettify())
    rating_entries = soup.find_all('div',class_='rating')
    download_list = []
    for e  in rating_entries:
        selected = e.find('li',class_='selected')
        if not selected:
           continue
        rating = selected.find('span').getText()
        if rating == "A":
            #http://www.xeno-canto.org/sounds/uploaded/ZWAQHOJFLZ/XC347629-161219-Malcoha%20a%CC%80%20bec%20jaune%40Banco.mp3
            
            p =  e.find_parent('td')
            logging.debug(p)
            ahref =  p.select('a')[0]
            mp3_name = ahref.get('download')
            url = "http://www.xeno-canto.org"+ahref.get('href')
            logging.debug(ahref)
            logging.info(u"rating:{},{}:{}".format(rating,mp3_name,url))
            download_list.append((mp3_name,url))
    return download_list

def download(url,local_path):
    
    logging.info(u"{} downloading {}: {}  ...".format(timestamp(), local_path,url))
    urllib.socket.setdefaulttimeout(300)
    if os.path.exists(local_path):  
        logging.info(u"skip existed :{}".format(local_path))
    else:
        for i in range(10):
            try:
               urllib.urlretrieve(url, local_path)
               break
            except:
               time.sleep(60)
               if i == 9:
                  logging.info(u"downloading failed due to timeout:{}".format(local_path))




def test():
    url = "http://www.xeno-canto.org/explore?dir=0&order=xc&pg=1"
    html_reponse = urllib2.urlopen(url).read()
    mp3_urls = parse_html(html_reponse)
    logging.debug(mp3_urls)
    mp3_url = "http://www.xeno-canto.org/347641/download"
    #download(mp3_url,'aaa.mp3') 

def generate_media_playlist(media_dir,playlist):
    mp3_list = glob.glob(media_dir)
    with codecs.open(playlist,'w',encoding='utf-8') as fd:
        fd.write("""
    <?wpl version="1.0"?>
<smil>
    <head>
        <meta name="Generator" content="Microsoft Windows Media Player -- 12.0.14393.447"/>
        <meta name="ItemCount" content="0"/>
        <author/>
        <title>{}</title>
    </head>
    <body>
        <seq>
""".format(playlist))
        for e in mp3_list:
            line = u"""      <media src="{}"/>\n""".format(e)
            logging.debug(line)
            fd.write(line,)       
        fd.write("""
        </seq>
    </body>
</smil>
""")


def download_from_xeno_canto():
   """
   http://www.xeno-canto.org/explore?dir=0&order=xc
   http://www.xeno-canto.org/explore?dir=0&order=xc&pg=2
   """
   url_prefix = "http://www.xeno-canto.org/explore?dir=0&order=xc&pg="
   dst_dir = u"D:\\bird_xeno-canto"
   for page_index in xrange(6000,11183):
       logging.info("{} begin downloading on Page : {} ".format(timestamp(),page_index))
       url = u"{}{}".format(url_prefix,page_index)
       for i in range(10):
           try:
               html_reponse = urllib2.urlopen(url).read()
               break
           except:
               pass
       mp3_list = parse_html(html_reponse)
       for mp3 in mp3_list:
           #("name","url")
           download( mp3[1], os.path.join(dst_dir,mp3[0]))
      
def main():
    generate_media_playlist(u"D:\\bird_xeno-canto\\*.mp3","bird.wpl")     

#test()
main()
