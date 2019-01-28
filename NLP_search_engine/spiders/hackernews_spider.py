import scrapy
import lxml.etree
import lxml.html
import sqlite3
from pathlib import Path
import re


class HackernewsSpider(scrapy.Spider):
    name = "hackernews"
    start_urls = [
        'https://thehackernews.com/'
    ]
    maxRequests = 50
    requestsDone = 0

    # Executed for every url specified in url - just example to begin with
    def parse(self, response):
        # "click" every article and run parse_text_data function
        for text in response.css('div.body-post'):
            text_content = text.css(
                'a.story-link::attr("href")').extract_first()
            if text_content is not None:
                if self.requestsDone < self.maxRequests:
                    yield response.follow(text_content, self.parse_text_data)
                    self.requestsDone += 1
        # get next page's articles and rerun parse for each of them
        next_page = response.css(
            'a.blog-pager-older-link-mobile::attr("href")').extract_first()
        if next_page is not None:
            if self.requestsDone < self.maxRequests:
                yield response.follow(next_page, self.parse)

    # Gets the title, url and content without html tags and newline characters for each article
    # Refactored and used lxml to remove all html etc as in answer of paul trmbrth here: https://stackoverflow.com/questions/17721782/is-it-possible-that-scrapy-to-get-plain-text-from-raw-html-data-directly-instead
    def parse_text_data(self, response):
        for text in response.css('div.main-box'):
            content = text.css('div.articlebody').extract_first()
            root = lxml.html.fromstring(content)

            # remove tags that are not usually rendered in browsers
            # javascript, HTML/HEAD, comments, add the tag names you dont want at the end
            lxml.etree.strip_elements(
                root, lxml.etree.Comment, "script", "head")

            # convert html to string
            just_text = lxml.html.tostring(
                root, method="text", encoding="unicode")
            
            just_text = just_text.encode('ascii', 'replace').decode('utf-8')
            just_text = re.sub(r'[^a-zA-Z0-9]'," ", just_text)

            title = text.css('a::text').extract_first()
            url = text.css('a::attr(href)').extract_first()
            
            conn = sqlite3.connect(
                str(Path(__file__).parent.parent) + '/database/crawler_db.sqlite', timeout=10)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO ARTICLES (title,url,text)
                          VALUES (?,?,?)''',
                           (title, url, just_text))
            conn.commit()
            conn.close()
