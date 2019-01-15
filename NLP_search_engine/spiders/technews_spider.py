import scrapy
import lxml.etree
import lxml.html

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
    # to-do: do not include content about author
    #        Specifically, ignore <p id="story-authorbio">

   
    def parse_text_data(self, response):
        for text in response.css('#story'):          
            content = text.css('#story-body').extract_first()
            root = lxml.html.fromstring(content)

            # remove tags that are not usually rendered in browsers
            # javascript, HTML/HEAD, comments, add the tag names you dont want at the end
            lxml.etree.strip_elements(
                root, lxml.etree.Comment, "script", "head")
            
            #convert html to string
            just_text = lxml.html.tostring(
                root, method="text", encoding="unicode")

            #remove newline chars
            just_text = just_text.replace("\n", " ").replace('\"', " ").replace("\t", " ")
                     
            yield {
                'text-title': text.css('h1.title::text').extract_first(),
                'text-url': response.request.url,
                'text-content': just_text
            }
