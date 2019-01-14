import scrapy
from bs4 import BeautifulSoup

class TextsSpider(scrapy.Spider):
    name = "texts"
    start_urls = [
        'https://thehackernews.com/'
    ]

    # Executed for every url specified in url - just example to begin with
    def parse(self, response):
        # "click" every article and run parse_text_data function
        for text in response.css('div.body-post'):
            text_content = text.css(
                'a.story-link::attr("href")').extract_first()
            if text_content is not None:
                yield response.follow(text_content, self.parse_text_data)
        # get next page's articles and rerun parse for each of them
        next_page = response.css(
            'a.blog-pager-older-link-mobile::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    # Gets the title, url and content without html tags and newline characters for each article
    # to-do: remove all javascript code such as "adsbygoogle = window.adsbygoogle || []).push({})"
    #        found in every article
    def parse_text_data(self, response):
        for text in response.css('div.main-box'):          
            content = text.css('div.articlebody').extract_first()
            soup = BeautifulSoup(content, 'html.parser')
            just_text = soup.get_text().replace("\n", "") 
            yield {
                'text-title': text.css('a::text').extract_first(),
                'text-url': text.css('a::attr(href)').extract_first(),
                'text-content': just_text
            }
