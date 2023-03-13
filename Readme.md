# Final assignmnent

## Vocabulary

The app exports vocabulary into db, let the user look through the whole vocabulary, find translation for a word and use it as a training tool.

##### Project structure #####
**file_handler.py**
**db.py**
**api_handler.py**
**setup.sql**
**templates map** with 3 html files

1. The app is reading a .txt file with words and its translations from .txt file that shall have a following structure
in order to be read successfully:
**word**
**translation**
**score**

2. The file content is exported into the database.

3. We can execute following operations with db:
   1.**show** the list of all words as html with help of **Ninja2 and FastApi**
   __@app.get("/", response_class=HTMLResponse)__
   2. get word translation in html 
   __@app.get("/show/{word}", response_class=HTMLResponse)__
   3. **insert** a new word with translation with the help of **input Form**
   __@app.get('/insert', response_class=HTMLResponse)__
   Both __get__ and __post__ are used here.
   4. use a vocabulary db as training tool via html interface
   __@app.get('/random', response_class=HTMLResponse)__
	Both __get__ and __post__ are used here.
   5.  update the word translation
   __@app.put("/update")__
   6. Remove the word from the db
   __@app.delete("/delete/{word}")__
   7. Save the modified db back into the file