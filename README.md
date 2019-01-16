# NLP-Search-Engine

Make sure scrapy and dependencies are installed like it is mentioned on <a href="https://doc.scrapy.org/en/latest/intro/install.html">docs</a>

<strong> Option A: </strong>
cd to project folder (NLP-Search-Engine) and run:<br/>
```
scrapy crawl hackernews OR scrapy crawl technews
```
Check terminal for output to see if everything is set up correctly <br/>


<strong> Option B: </strong>
cd to <em> spiders </em> folder and run: <br/>
```
scrapy runspider hackernews_spider.py -o hackernews.json  OR  scrapy runspider technews_spider.py -o technews.json
```
JSON file will be created in the same folder
