import scrapy
from bs4 import BeautifulSoup

class TechnewsSpider(scrapy.Spider):
    name = "technews"
    start_urls = [
        'https://www.technewsworld.com/'
    ]
  
    # Executed for every url specified in url - just example to begin with
    def parse(self, response):
        domain = "https://www.technewsworld.com"

        # "click" every article and run parse_text_data function
        for text in response.css('div.story-list'):
            text_content = text.css('a::attr("href")').extract_first() 
            if text_content is not None:
                text_content = domain + text_content
                yield response.follow(text_content, self.parse_text_data)        
        # get next page's articles and rerun parse for each of them
        next_page = response.css(
            '#earlier a::attr("href")').extract_first()
        if next_page is not None:
            next_page = domain + next_page
            yield response.follow(next_page, self.parse)

    # Gets the title, url and content without html tags and newline characters for each article
    # to-do: remove all javascript code found in every article such as 
    #        " <!--//<![CDATA[//]]>//--><!--//<![CDATA[\r(adsbygoogle = window.adsbygoogle || []).push({});\r//]]>//-->"
    #        remove '\"'
    def parse_text_data(self, response):
        for text in response.css('#story'):          
            content = text.css('#story-body').extract_first()
            soup = BeautifulSoup(content, 'html.parser')
            just_text = soup.get_text().replace("\n", "") 
            yield {
                'text-title': text.css('h1.title::text').extract_first(),
                'text-url': response.request.url,
                'text-content': just_text
            }
