import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

db = sqlite3.connect("birthday.db")

db.execute(
    '''
    CREATE TABLE IF NOT EXISTS gift_records(
    name        TEXT,
    gift        TEXT,
    greeting    TEXT,
    PRIMARY KEY (name, gift)
    )
    '''
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GiftRecord(BaseModel):
    name: str
    gift: str
    greeting: str

@app.get("/")
async def get_gifts():
    c = db.cursor()
    c.execute(
        '''
        SELECT    name, gift, greeting
        FROM      gift_records
        '''
    )
    return [{"name": name, "gift": gift, "message": greeting} for name, gift, greeting in c]

@app.post("/")
async def post_gift(gift_record: GiftRecord):
    c = db.cursor()
    try:
        c.execute(
            '''
            INSERT
            INTO gift_records(name, gift, greeting)
            VALUES(?, ?, ?)
            ''',
            [gift_record.name, gift_record.gift, gift_record.greeting]
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        print("Duplicate entry!")