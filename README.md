# NLP-Search-Engine

Make sure scrapy and dependencies are installed like it is mentioned on <a href="https://doc.scrapy.org/en/latest/intro/install.html">docs</a>

Additional Dependencies Install:

```
pip install BeautifulSoup4
pip install pathlib
pip install nltk 
pip install numpy 
```

Create DB and 'ARTICLES' table
```
cd NLP_Search_Engine
cd database
python create_DB.py
```

Then, run to crawl the websites and store the articles in database:<br/>
```
scrapy crawl hackernews
scrapy crawl technews
```

Then, add postags to each word in article :<br/>
```
python morphoSyntactic_analysis.py
```

After Postagger step is done and file is correctly generated with words and postags, run :<br/>
```
python vector_space_model.py
```

To created inverted file in xml format run: :<br/>

```
python indexing.py
```

and check console for the output.
