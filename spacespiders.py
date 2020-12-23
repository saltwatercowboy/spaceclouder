import scrapy
from scrapy.crawler import CrawlerProcess
import re
from wordcloudmaker import make_cloud, wordcloud, mask

#asks user for search input and assigns to variable
print('What would you like to word cloud? \ne.g.: SpaceX, Exoplanet, JPL')
searchquery = input('> ')

#defines spider name and pages to crawl
#google news spider
class Googlenewsspider(scrapy.Spider):
    name = 'google_spider'
    allowed_domains = ['news.google.com']
    #concatenates scrapy urls to search with user query, passes to spider
    url_dict = {'start' : 'https://news.google.com/search?q=',
                  'end' : '&hl=en-US&gl=US&ceid=US%3Aen'}
    new_urls = str(url_dict['start'] + searchquery + str(url_dict['end']))
    start_urls = [new_urls]

    #searches the page for the headline html class, creates dictionary generator with yield 
    def parse(self, response):
        global titles
        titles = re.findall(r'<h3 class="[^"]+?"><a[^>]+?>(.+?)</a>', response.text)
        yield {'titles' : titles}

#space.com spider
class space_spider(scrapy.Spider):
    name = 'space_spider'
    allowed_domains = ['space.com']
    url_dict = {'start' : 'https://www.space.com/search?searchTerm='}
    new_urls = str(url_dict['start'] + searchquery)
    start_urls = [new_urls]
    
    def parse(self, response):
        global sa_responses
        sa_responses = response.xpath('//*[@id="content"]/section/div/div/a/article/div/header/h3/text()').getall()
        yield {'sa_responses' : sa_responses}

#wired.com spider        
class wired_spider(scrapy.Spider):
    name = 'wired_spider'
    allowed_domains = ['wired.com']
    url_dict = {'start' : 'https://www.wired.com/search/?q=',
                'end' : '&page=1&sort=score'}
    new_urls = str(url_dict['start'] + searchquery + str(url_dict['end']))
    start_urls = [new_urls]
    
    def parse(self, response):
        global wired_responses
        wired_responses = response.xpath('//*[@id="app-root"]/div/div/div/div/div/div/ul/li/div/a/h2/text()').getall()
        yield {'wired_responses' : wired_responses}

#vox.com spider       
class vox_spider(scrapy.Spider):
    name = 'vox_spider'
    allowed_domains = ['vox.com']
    url_dict = {'start' : 'https://www.vox.com/search?q='}
    new_urls = str(url_dict['start'] + searchquery)
    start_urls = [new_urls]
    
    def parse(self, response):
        global vox_responses
        vox_responses = response.xpath('/html/body/div/section/div/div/div/div/div/div/h2/a/text()').getall()
        yield {'vox_responses' : vox_responses}

#writes to .txt file and fixes broken parsing
class fixer_writer:
    #replaces broken apostrophe parsing, search query, other undesirables and saves in a new .txt file
    def replace_breaks(self):
        replace1 = str(searchquery + 's')
        replace2 = str(searchquery + "'s")
        replace3 = str.casefold(searchquery)
        toreplace = {'&#39;' : "'",
                     'Business Insider' : '',
                     replace1 : '',
                     replace2 : '',
                     replace3 : '',
                     searchquery : ''
                     }
        #opens file, reads and replaces, then saves as new file
        with open('titles.txt') as infile, open('titlesfixed.txt', 'w+') as outfile:
            for line in infile:
                for inp, outp in toreplace.items():
                    line = line.replace(inp, outp)
                outfile.write(line)
    #writes scrapy responses to file
    def write_to_file(self):
        with open('titles.txt', 'w') as f:
            for i in titles:
                f.write(i + '\n')

            for i in sa_responses:
                f.write(i + '\n')
            
            for i in wired_responses:
                f.write(i + '\n')
                
            for i in vox_responses:
                f.write(i + '\n')
        
#runs QuoteSpider crawler from .py instead of shell
if __name__ == '__main__':
    fixwri = fixer_writer()
    process = CrawlerProcess()
    process.crawl(Googlenewsspider)
    process.crawl(space_spider)
    process.crawl(wired_spider)
    process.crawl(vox_spider)
    process.start()
    fixwri.write_to_file()
    fixwri.replace_breaks()
    make_cloud(wordcloud)
