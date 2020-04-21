import json
import requests
import sqlite3

DB_NAME = 'world.sqlite'

def load_countries():
    base_url = 'https://restcountries.eu/rest/v2/all'
    countries = requests.get(base_url).json()
    # print(json.dumps(countries, indent=2))  languages = c['languages']

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    insert_sql = '''
        INSERT INTO "Countries"
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    for c in countries:
        eng_name = c['name']
        alpha2 = c['alpha2Code']
        capital = c['capital']
        currencies = c['currencies'][0]['code']
        languages = c['languages'][0]['name']
        subregion = c['subregion']
        population = c['population']
       
        
        cur.execute(insert_sql,
            [ 
                None, alpha2, capital, eng_name, currencies, languages,
                 subregion, population
            ]
        )
    conn.commit()
    conn.close()


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()


    drop_countries_sql = 'DROP TABLE IF EXISTS "Countries"'
    
    
    create_countries_sql = '''
        CREATE TABLE IF NOT EXISTS 'Countries'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT NOT NULL,
            'Capital' TEXT NOT NULL,
            'Name' TEXT NOT NULL,
            'Currencies' TEXT,
            'Languages' TEXT, 
            'Subregion' TEXT NOT NULL,
            'Population' INTEGER NOT NULL
        )
    '''
    
    cur.execute(drop_countries_sql)
    cur.execute(create_countries_sql)
    conn.commit()
    conn.close()

create_db()
load_countries()

