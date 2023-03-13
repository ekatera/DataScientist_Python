from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from db import DB
from fastapi.staticfiles import StaticFiles
import random
class Vocab(BaseModel):
    id:int = 0
    source: str = ''
    translation:str = ''
    score: int = 0
    times: int = 0

db = DB("vocab.db")
app = FastAPI()
templates = Jinja2Templates(directory="templates")
quiz_vocab = Vocab()
list_of_vocabs:list = []

app.mount("/static", StaticFiles(directory="static"), name="static")

# translate word
@app.get("/show/{word}", response_class=HTMLResponse)
async def read_item(request: Request, word: str):
    res = db.get_translation(word)
    if not res:
       res = f"Failed to find translation for {word}"
    return templates.TemplateResponse("index.html", {"request": request, "word_requested":word, "word": res})

# show dictionary
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    res = db.fetch_table()
    return templates.TemplateResponse("index.html", {"request": request, "vocab": res})

#form for inserting a new word
@app.get('/insert', response_class=HTMLResponse)
def insert_word(request: Request):
    return templates.TemplateResponse('insert.html', {'request': request})

# create new item
@app.post('/insert', response_class=HTMLResponse)
def save_result(request: Request, new_word: str = Form(''), new_transl: str = Form('')):
    print("RESULT", new_word, new_transl)
    res = db.insert(word_pair={"source": new_word, "translation":new_transl})
    if res:
        return templates.TemplateResponse('insert.html', {'request': request, 'added_word': new_word, 'added_translation': new_transl})
    else:
        return templates.TemplateResponse('insert.html', {'request': request, 'word_exit': True})
    
# vocabular trainer
@app.get('/random', response_class=HTMLResponse)
def get_random_item(request: Request):
    vocabs = db.fetch_table()
    random_value = random.randint(0, len(vocabs)-1)
    
    quiz_vocab.id = vocabs[random_value][0]
    quiz_vocab.source = vocabs[random_value][1]
    quiz_vocab.translation = vocabs[random_value][2]
    quiz_vocab.score = vocabs[random_value][3]

    list_of_vocabs.append(quiz_vocab)
    return templates.TemplateResponse('trainer.html', {'request': request, "random_word":quiz_vocab.source})

@app.post('/random', response_class=HTMLResponse)
def save_result(request: Request, quiz_item: str = Form('')):
    for item in list_of_vocabs:
        if item.source == quiz_vocab.source:
            quiz_answers= quiz_vocab.translation.split(",")
    
    quiz_answers = [item.strip().lower() for item in quiz_answers]
    print(quiz_answers)
    if quiz_item.strip().lower() in quiz_answers:
        is_right = "Correct"
    else:
        is_right = "Wrong"
    
    db.update(word_pair={"source": quiz_vocab.source, "translation":quiz_vocab.translation, "score": quiz_vocab.score})
    return templates.TemplateResponse('trainer.html', {'request': request, 'is_right': is_right})

#update word
@app.put("/update")
def update_word(voc:Vocab):
    db.update(word_pair={"source": voc.source, "translation":voc.translation, "score": voc.score})

#delete word
@app.delete("/delete/{word}")
def update_vocabulary_item(word):
    db.delete(word)
