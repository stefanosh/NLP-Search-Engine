# NLP-Search-Engine

Make sure scrapy and dependencies are installed like it is mentioned on <a href="https://doc.scrapy.org/en/latest/intro/install.html">docs</a>

Also install BeautifulSoup dependency used to clear the html content with: **NOTE** maybe it will be removed if we choose refactored method of lxml
```
pip install BeautifulSoup4
```

<strong> Option A: </strong>
cd to project folder (NLP-Search-Engine) and run:<br/>
```
scrapy crawl texts
```
Check terminal for output to see if everything is set up correctly <br/>


<strong> Option B: </strong>
cd to <em> spiders </em> folder and run: <br/>
```
scrapy runspider texts_spider.py -o texts.json
```
JSON file will be created in the same folder
