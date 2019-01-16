# NLP-Search-Engine

Make sure scrapy and dependencies are installed like it is mentioned on <a href="https://doc.scrapy.org/en/latest/intro/install.html">docs</a>

Dependencies install:

```
pip install BeautifulSoup4
```

Create DB and 'ARTICLES' table
```
cd NLP_Search_Engine
cd database
python create_DB.py
```

Then, run:<br/>
```
scrapy crawl hackernews
scrapy crawl technews
```
Check terminal for output to see if everything is set up correctly <br/>

