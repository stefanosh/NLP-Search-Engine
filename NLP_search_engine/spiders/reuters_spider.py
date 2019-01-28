import scrapy
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
import re


class ReutersSpider(scrapy.Spider):
    name = "reuters"
    start_urls = [
        'https://www.reuters.com/news/archive/worldNews'
    ]
    max_requests = 50
    requests_done = 0

    # Executed for every url specified in url - just example to begin with
    def parse(self, response):
        domain = "https://www.reuters.com"

        # "click" every article and run parse_text_data function
        for text in response.css('div.story-content'):
            text_content = text.css('a::attr("href")').extract_first()
            if text_content is not None:
                text_content = domain + text_content
                if(self.requests_done < self.max_requests):
                    yield response.follow(text_content, self.parse_text_data)
                    self.requests_done += 1
        # get next page's articles and rerun parse for each of them
        next_page = response.css(
            'a.control-nav-next::attr("href")').extract_first()
        if next_page is not None:
            next_page = self.start_urls[0] + next_page
            if(self.requests_done < self.max_requests):
                yield response.follow(next_page, self.parse)
    # Gets the title, url and content without html tags and newline characters for each article

    def parse_text_data(self, response):

        title = response.css('h1.ArticleHeader_headline::text').extract_first()
        url = response.request.url

        content_list = response.xpath(
            '//div[@class="StandardArticleBody_body"]/descendant::text()[not(ancestor::div/@class="Attribution_container")][not(ancestor::div/@class="StandardArticleBody_trustBadgeContainer")]').extract()
        content_text = ''

        for p in content_list:  # extracts all <p> inside content list
            content_text = content_text + p

        soup = BeautifulSoup(content_text, 'html.parser')
        just_text = soup.get_text().encode('ascii', 'replace').decode('utf-8')
        just_text = re.sub(r'[^a-zA-Z0-9]', " ", just_text)

        conn = sqlite3.connect(
            str(Path(__file__).parent.parent) + '/database/crawler_db.sqlite', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ARTICLES (title,url,text)
                          VALUES (?,?,?)''',
                       (title, url, just_text))
        conn.commit()
        conn.close()
