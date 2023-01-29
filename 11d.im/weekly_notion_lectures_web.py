# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
from datetime import datetime, timedelta

import requests, json
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('NOTION')

databaseId = 'a3c9bdc092ff497494ab493d82970985'

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}


# %%
def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


# %%
readDatabase(databaseId, headers)

# %%
highlights = (
    pd.DataFrame(
        list(
            [
                item['properties']['Title']['title'][0]['plain_text'],
                item['properties']['URL']['url'],
                item['properties']['Last Highlighted']['date']['start']
            ]
            for item
            in
                json.load(open('db.json'))
                ['results']
            if
                item['properties']['Category']['select']['name'] == 'Articles'
        ),
        columns=['title', 'url', 'date']
    )
    .assign(
        date = lambda df: pd.to_datetime(df.date, utc=True)
    )
)

# %%
day = datetime.now()
friday = day - timedelta(days=day.weekday()) + timedelta(days=4)
friday_prev = friday + timedelta(weeks=-1)

[friday, friday_prev]

# %%
last = highlights[ highlights.date >= '2023-01-20' ]

# %%
print("\n".join([ f"- [{l[0]}]({l[1]})" for l in last.values.tolist()  ]))

# %%
podcasts = (
    pd.DataFrame(
        list(
            [
                item['properties']['Title']['title'][0]['plain_text'],
                item['properties']['URL']['url'],
                item['properties']['Last Highlighted']['date']['start']
            ]
            for item
            in
                json.load(open('db.json'))
                ['results']
            if
                item['properties']['Category']['select']['name'] == 'Podcasts'
        ),
        columns=['title', 'url', 'date']
    )
    .assign(
        date = lambda df: pd.to_datetime(df.date, utc=True)
    )
)

# %%
podcasts

# %%
print("\n".join([ f"- [{l[0]}]({l[1]})" for l in podcasts[ podcasts.date >= '2023-01-20' ].values.tolist()  ]))

# %%
