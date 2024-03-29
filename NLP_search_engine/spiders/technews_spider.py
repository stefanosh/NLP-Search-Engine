import scrapy
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
import re


class TechnewsSpider(scrapy.Spider):
    name = "technews"
    start_urls = [
        'https://www.technewsworld.com/'
    ]
    max_requests = 50
    requests_done = 0

    # Executed for every url specified in url - just example to begin with
    def parse(self, response):
        domain = "https://www.technewsworld.com"

        # "click" every article and run parse_text_data function
        for text in response.css('div.story-list'):
            text_content = text.css('a::attr("href")').extract_first()
            if text_content is not None:
                text_content = domain + text_content
                if(self.requests_done < self.max_requests):
                    yield response.follow(text_content, self.parse_text_data)
                    self.requests_done += 1
        # get next page's articles and rerun parse for each of them
        next_page = response.css(
            '#earlier a::attr("href")').extract_first()
        if next_page is not None:
            next_page = domain + next_page
            if(self.requests_done < self.max_requests):
                yield response.follow(next_page, self.parse)
    # Gets the title, url and content without html tags and newline characters for each article

    def parse_text_data(self, response):
        for text in response.css('#story'):          
            
            # Getting all content(paragraphs) of the article excluding the article 
            # containing the bio of author as it is useless for indexing
            content_list = text.xpath("//div[@id ='story-body']/descendant::text()[not(ancestor::p/@id='story-authorbio')]").extract()
            content_text = ''
            
            # Concatenating each paragraph(<p>) to the final article text
            for p in content_list:  # extracts all <p> inside content list
                content_text = content_text + p      
            soup = BeautifulSoup(content_text, 'html.parser')

            just_text = soup.get_text().encode('ascii', 'replace').decode('utf-8')
            just_text = re.sub(r'[^a-zA-Z0-9]'," ", just_text)    
           
            title = text.css('h1.title::text').extract_first()
                 
            conn = sqlite3.connect(
                str(Path(__file__).parent.parent) + '/database/crawler_db.sqlite', timeout=10)
            cursor = conn.cursor() 
            cursor.execute('''INSERT INTO ARTICLES (title,url,text) 
                          VALUES (?,?,?)''',
                          (title,response.request.url,just_text))
            conn.commit()  
            conn.close()
            