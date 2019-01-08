import scrapy


class TextsSpider(scrapy.Spider):
    name = "texts"

    def start_requests(self):
        urls = [
            'https://thehackernews.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Executed for every url specified in url - just example to begin with
    # to-do: "click" every post and get its content, also "click" every next-page and get all texts same way
    def parse(self, response):
        print("response")
        print(response)
        for text in response.css('div.body-post'):
            yield {
                'text-title': text.css('h2.home-title::text').extract_first(),
                'text-url': text.css('a.story-link::attr(href)').extract_first()
            }
