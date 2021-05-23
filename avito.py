# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D0%BA%D0%BE%D1%82&locationId=653241
# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D1%81%D1%82%D1%83%D0%BB&categoryId=20&locationId=653241

import requests
from fastapi import FastAPI
import asyncio
import time
import sqlite3

app = FastAPI()
conn = sqlite3.connect('orders.db')
key = 0


def get_region_id(region):
    url = 'https://m.avito.ru/api/1/slocations?' \
          'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' \
          '&locationId=621540&limit=10&q={}'.format(region)
    response = requests.get(url)
    id_region = response.json()['result']['locations'][1]['id']
    return id_region


async def get_count(key_, search, id_reg):
    while True:
        url = 'https://m.avito.ru/api/10/items?' \
              'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&' \
              'query={}&locationId={}'.format(search, id_reg)
        response = requests.get(url)
        count = response.json()['result']['count']
        print(search, "+", id_reg, '=', count)
        timestamp = int(time.time())
        info = (key_, count, timestamp, search, id_reg)
        cur = conn.cursor()
        cur.execute("INSERT INTO keys(key, count, timestamp, search_fraze, region) VALUES(?, ?, ?, ?, ?);", info)
        conn.commit()
        cur.execute("SELECT * FROM keys;")
        one_result = cur.fetchall()
        print(one_result)
        await asyncio.sleep(60)  # FIXME


@app.get("/add")
async def root(search, region):
    global key
    id_reg = get_region_id(region)
    asyncio.create_task(get_count(key, search, id_reg))
    key += 1
    return {'id связки (поисковая фраза + регион)': key-1}


@app.get("/stat")
async def root(pair_id, t1, t2):  # FIXME
    cur = conn.cursor()
    sql_select_query = """select count, timestamp from keys where key = ? and timestamp > ? and timestamp < ?"""
    cur.execute(sql_select_query, (pair_id, t1, t2))
    records = cur.fetchall()
    print('STAT', records)
    return {'счётчики и соответствующие им временные метки': records}
