import uvicorn
from fastapi import FastAPI, Request
import os
import sys
from threading import Thread



app = FastAPI()

@app.get('/')
async def index():
    return {"answer": 'ХУЙ'}

def start():
    uvicorn.run("my_site:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=False)

def keep_alive():
    t = Thread(target=start)
    t.start()
