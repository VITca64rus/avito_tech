import requests
from fastapi import FastAPI
import asyncio
import time
import sqlite3
from typing import List, Tuple, Dict

app = FastAPI()
conn = sqlite3.connect('orders.db')
key = 0


def get_region_id(region: str) -> int:
    url = 'https://m.avito.ru/api/1/slocations?' \
          'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' \
          '&locationId=621540&limit=10&q={}'.format(region)
    response = requests.get(url)
    id_region = response.json()['result']['locations'][1]['id']
    return id_region


async def get_count(key_: int, search: str, id_reg: int) -> None:
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
async def root(search: str, region: str) -> Dict[str, int]:
    #global key  # FIXME
    cur = conn.cursor()
    cur.execute("SELECT MAX(key) FROM keys;")
    key = cur.fetchone()[0] + 1
    print(key)
    id_reg: int
    id_reg = get_region_id(region)
    asyncio.create_task(get_count(key, search, id_reg))
    #key += 1
    return {'id связки (поисковая фраза + регион)': key}


@app.get("/stat")
async def root(pair_id: int, t1: int, t2: int) -> Dict[str, List[Tuple[int, int]]]:
    cur = conn.cursor()
    sql_select_query = """select count, timestamp from keys where key = ? and timestamp > ? and timestamp < ?"""
    cur.execute(sql_select_query, (pair_id, t1, t2))
    records = cur.fetchall()
    print('STAT', records)
    return {'счётчики и соответствующие им временные метки': records}
