# NLP-Search-Engine

Make sure scrapy and dependencies are installed like it is mentioned on <a href="https://doc.scrapy.org/en/latest/intro/install.html">docs</a>

Additional Dependencies Install:

```
pip install BeautifulSoup4
pip install pathlib
pip install nltk 
pip install numpy
pip install xmljson
```

Create DB and 'ARTICLES' table
```
cd NLP_search_engine
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

After Postagger step is done, in order to add lemmatisation, calculations of tf_idf etc, and write to inverted_index.xml file, run :<br/>
```
python vector_space_model.py
```

Do everything in one command:
```
cd NLP_search_engine/ && python ./database/create_DB.py && scrapy crawl hackernews && scrapy crawl technews && python morphoSyntactic_analysis.py && python vector_space_model.py
```

Start a query! You can add as many words you wish, and limit the results by limit argument(when there is no limit, all articles containing the word are returned)
```
python query_index.py day compete value --limit 10
```