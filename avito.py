# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D0%BA%D0%BE%D1%82&locationId=653241
# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D1%81%D1%82%D1%83%D0%BB&categoryId=20&locationId=653241

import requests
from fastapi import FastAPI
import asyncio

app = FastAPI()

import sqlite3
conn = sqlite3.connect('orders.db')

def get_region_id(region):
    url = 'https://m.avito.ru/api/1/slocations?' \
          'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' \
          '&locationId=621540&limit=10&q={}'.format(region)
    response = requests.get(url)
    id_region = response.json()['result']['locations'][1]['id']
    return id_region


async def get_count(key, search, id_reg):
    while True:
        url = 'https://m.avito.ru/api/10/items?' \
              'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&' \
              'query={}&locationId={}'.format(search, id_reg)
        response = requests.get(url)
        count = response.json()['result']['count']
        print(search, "+", id_reg, '=', count)
        info = (key, count, search, id_reg)
        cur = conn.cursor()
        cur.execute("INSERT INTO keys(key, count, search_fraze, region) VALUES(?, ?, ?, ?);", info)
        conn.commit()

        cur.execute("SELECT * FROM keys;")
        one_result = cur.fetchall()
        print(one_result)
        await asyncio.sleep(60)  # FIXME

key = 0
@app.get("/add")
async def root(search, region):  # FIXME
    global key
    id_reg = get_region_id(region)
    asyncio.create_task(get_count(key, search, id_reg))
    key += 1
    # await mytask
    return {'id связки (поисковая фраза + регион)': key-1}


@app.get("/stat")
async def root(pair_id, time_start, time_end):  # FIXME
    pass
