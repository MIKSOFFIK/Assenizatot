from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import sqlite3
import time
import traceback
import os

app = FastAPI()

with open("index.html", 'r', encoding='utf-8') as f:
    content=f.read()

def data_bese(phone:str, name:str, message:str, time:int):
    connection = sqlite3.connect('Users_base.db', timeout=10000)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            phone TEXT NOT NULL,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            time INTEGER NOT NULL
        )
        ''')
    cursor.execute('INSERT INTO Users (phone, name, message, time) VALUES (?, ?, ?, ?)', (phone, name, message, time))
    
    connection.commit()
    cursor.close()
    connection.close()    

app.mount("/lib", StaticFiles(directory="lib"), name="lib")

@app.get('/', response_class=HTMLResponse)
def main():
    return content

@app.get('/creat_zaiavka')
def creat_zaiavka(phone:str, name:str, message:str):
    data_bese(phone, name, message, time.monotonic())
    return 200





# Запуск сервера
if __name__ == '__main__':
    import uvicorn 
    while True:
        try:
            uvicorn.run(app, host='0.0.0.0', port=8080)
        except Exception as e:
            print(f"{e}\n{traceback.format_exc()}")