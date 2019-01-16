import scrapy
import lxml.etree
import lxml.html

# to-do: Limit crawler to only 500 texts
# to-do: Support crawling of second site (www.technewsworld.com) also


class HackernewsSpider(scrapy.Spider):
    name = "hackernews"
    start_urls = [
        'https://thehackernews.com/'
    ]
    maxRequests = 500
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

            # remove some special chars
            just_text = just_text.replace("\n", " ").replace(
                '\"', " ").replace("\t", " ").replace("\r", " ")

            yield {
                'text-title': text.css('a::text').extract_first(),
                'text-url': text.css('a::attr(href)').extract_first(),
                'text-content': just_text
            }
