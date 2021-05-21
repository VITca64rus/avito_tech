# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D0%BA%D0%BE%D1%82&locationId=653241
# https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query=%D1%81%D1%82%D1%83%D0%BB&categoryId=20&locationId=653241

import requests
from fastapi import FastAPI

app = FastAPI()


def get_region_id(region):
    url = 'https://m.avito.ru/api/1/slocations?' \
          'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' \
          '&locationId=621540&limit=10&q={}'.format(region)
    response = requests.get(url)
    id_region = response.json()['result']['locations'][1]['id']
    return id_region

@app.get("/add")
async def root(search, region): #FIX_ME
    get_region_id(region)
    return {search: region}


@app.get ("/stat")
async def root(pair_id, time_start, time_end): #FIX_ME
    pass
