import scrapy
import urllib2
from bs4 import BeautifulSoup
from wogmascrap.items import WogmascrapItem

def getReview(path):
    try:
        response=urllib2.urlopen(path)
        Doc=response.read()
        soup = BeautifulSoup(''.join(Doc))
        value=soup.findAll("div",{"class":"review large-first-letter"})[0].get_text()
        return value
    except urllib2.HTTPError,e:
        print e.code
    except urllib2.URLError,e:
        print e.args
    return ""

def getFileName(basepath,filename):
    return basepath+''.join(c for c in filename if c.isalnum())+".txt"

def writeData(basepath,filename,content):
    with open(getFileName(basepath,filename),'w') as opf:
        opf.write(content.encode('ascii','ignore'))
        opf.close()

class WogmaSpider(scrapy.Spider):
	name="wogma"
	allowed_domains=["http://wogma.com/"]
	start_urls=[
		"http://wogma.com/movies/alphabetic/basic/"
	]
	def parse(self, response):
            baseurl="http://www.wogma.com"
            basedir="/home/distro/Desktop/wogmascrap/Data/"
            item=WogmascrapItem()
            index =2
            while True:
                try:
                    elementclass=str(response.xpath('/html/body/div[1]/div[4]/div[1]/div/div/table/tr['+str(index)+']/@class').extract()[0])
                    if elementclass=='back_to_top':
                        index+=1
                        continue
                    moviename=str(response.xpath('/html/body/div[1]/div[4]/div[1]/div/div/table/tr['+str(index)+']/td[1]/text()').extract()[0].strip())
                    wogmareviewstrip=str(response.xpath('/html/body/div[1]/div[4]/div[1]/div/div/table/tr['+str(index)+']/td[3]/div[1]/a/text()').extract()[0]).strip()
                    if wogmareviewstrip== 'wogma review':
                        item['moviename']=moviename
                        reviewurl=str(response.xpath('/html/body/div[1]/div[4]/div[1]/div/div/table/tr['+str(index)+']/td[3]/div[1]/a/@href').extract()[0]).strip()
                        content=getReview(baseurl+reviewurl)
                        if len(content.strip())!=0:
                            writeData(basedir,moviename,content)
                            item['review']=content
                            #yield item
                except UnicodeEncodeError as uee:
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print 'Error in encoding at '+str(index)
                    print uee
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                except Exception as exp:
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print 'Error in decoding at '+str(index)
                    print exp
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    break
                index+=1