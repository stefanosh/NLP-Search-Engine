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

Then, run:<br/>
```
scrapy crawl hackernews
scrapy crawl technews
```
Check terminal for output to see if everything is set up correctly <br/>

After Postagger step is done and file is correctly generated with words and postags, run :<br/>
```
python vector_space__model.py
```
and check console for the output.
*NOTE* For testing purposes, i have uploaded file withpos.json which is the file that vector_space__model.py loads and makes the calculations.