import requests
import random
import pandas as pd
import time
import math
from copy import deepcopy
from statistics import mean

def request() -> list:
    res = requests.get('http://localhost:3000/api/ep1')
    return res.json()

def data_treatment(json:list):
    for i in range(len(json)):
        for key in json[i]:
            if ('prod' in key):
                if (type(json[i][key])!=dict):
                    qnt = json[i][key]
                    if (type(qnt)==str):
                        qnt = float(qnt)
                    if (qnt<0):
                        qnt = 0
                    if (key in [product for product in json[i] if ('prod' in product and (int(product[5]) < 9 and len(product) < 7))]):
                        json[i][key] = {'qnt':[round(qnt)], 'price':None}
                    else:
                        json[i][key] = {'qnt':[qnt], 'price':None}
        try:
            json[i]['date'] = time.ctime(json[i]['date'])
        except:
            continue
    return json


def generate_random_price(n_min=1.0, n_max=100.0) -> float:
    return round(random.uniform(n_min, n_max), 2)


def logistic_function(v: float) -> float:
    return 0.5 + (1 / (1 + math.e ** -v))


def calc_qnt_variation(last_week: list, current_week: list) -> float:
    return mean(current_week) - mean(last_week) / mean(last_week) if (mean(last_week) != 0) else 0


def calc_new_price(product_db: dict, sales_week: dict) -> dict:
    for product in product_db:
        if (product_db[product]['qnt'] != None):
            if (product not in sales_week.keys()):
                sales_week[product] = [0]
            product_db[product]['next_week_price'] = logistic_function(calc_qnt_variation(product_db[product]['qnt'], sales_week[product])) * product_db[product]['price']
        product_db[product]['qnt'] = sales_week[product]
    return product_db


def product_pricing(json: list, product_db: dict) -> tuple:
    sales_week = {}

    for transaction in json:
        for key in transaction:
            if ('prod' in key):
                if (key not in product_db.keys()):
                    transaction[key]['price'] = generate_random_price()
                    sales_week[key] = deepcopy(transaction[key]['qnt'])
                    product_db[key] = deepcopy(transaction[key])
                    product_db[key]['qnt'] = None
                    product_db[key]['next_week_price'] = product_db[key]['price']
                else:
                    transaction[key]['price'] = deepcopy(product_db[key]['next_week_price'])
                    product_db[key]['price'] = product_db[key]['next_week_price']
                    if (key not in sales_week.keys()):
                        sales_week[key] = deepcopy(transaction[key]['qnt'])
                    else:
                        sales_week[key] += deepcopy(transaction[key]['qnt'])

    product_db = calc_new_price(product_db, sales_week)

    return json, product_db


def df_to_all_df(json, all_df, week):
    for transacao in json:
        json_to_df = deepcopy(transacao)
        date = json_to_df['date']
        id = json_to_df['id']
        del json_to_df['date']
        del json_to_df['id']
        df = pd.DataFrame(json_to_df).T
        df['id'] = id
        df['date'] = date
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        df['week'] = week
        df = pd.concat([all_df, df])
        # df=df.set_index(['date','id'])

    return df


def format_all_df(all_df:pd.DataFrame):
    all_df=all_df.reset_index().rename(columns={'index':'product'}).set_index('id').reset_index()
    all_df['qnt'] = [float(item[0]) for item in all_df['qnt']]
    return all_df


def all_sales_csv(alldf):
    df_aux = alldf.copy()
    df_all_sales = pd.pivot_table(df_aux,index=['id', 'date'], columns=['product'], values = 'qnt', ).reset_index()
    all_sales_aux = pd.pivot_table(df_aux,index=['id', 'month'], columns=['product'], values = 'qnt', ).reset_index()
    df_all_sales = df_all_sales.fillna(0)
    df_all_sales['date'] = all_sales_aux['month']
    df_all_sales.to_csv('all_sales.csv', index = False)
    return df_all_sales


product_database = {}
weeks = 8
all_df = pd.DataFrame([])

for week in range(weeks):
    json = data_treatment(request())
    json, product_database = product_pricing(json, product_database)

    all_df = df_to_all_df(json=json, all_df=all_df, week=week)

all_df = format_all_df(all_df=all_df)


all_sales_csv(all_df)


