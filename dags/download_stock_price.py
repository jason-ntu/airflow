#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
from __future__ import annotations
import os
import yfinance as yf
import mysql.connector

# [START tutorial]
# [START import_module]
# from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from textwrap import dedent
from airflow.models import Variable

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# [END import_module]

os.environ["no_proxy"] = "*"

def get_tickers(context):
    stock_list = Variable.get("stock_list_json", deserialize_json=True)

    stocks = context["dag_run"].conf.get("stocks", None) if (
        "dag_run" in context and context["dag_run"] is not None) else None

    if stocks:
        stock_list = stocks
    return stock_list


def download_price(*args, **context):
    stock_list = get_tickers(context)

    for ticker in stock_list:
        dat = yf.Ticker(ticker)
        hist = dat.history(period="1mo")
        print(hist.shape[0])
        with open(get_file_path(ticker), 'w') as writer:
            hist.to_csv(writer, index=True)
        print(f"Downloaded {ticker}")


def get_file_path(ticker):
    # NOT SAVE in distributed system.
    return f'/Users/jason/airflow/logs/{ticker}.csv'


def load_price_data(ticker):
    with open(get_file_path(ticker), 'r') as reader:
        lines = reader.readlines()
        return [[ticker]+line.split(',')[:5] for line in lines if line[:4] != 'Date']


def save_to_mysql_stage(*args, **context):
    tickers = get_tickers(context)

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql',
        database='demodb',
        port=3306
    )

    mycursor = mydb.cursor()
    for ticker in tickers:
        val = load_price_data(ticker)
        print("val: ", val)
        print(f"{ticker} length={len(val)}   {val[1]}")

        sql = """INSERT INTO stock_prices_stage
            (ticker, as_of_date, open_price, high_price, low_price, close_price) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
        mycursor.executemany(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")


default_args = {
    'owner': 'jason'
}

# [START instantiate_dag]
with DAG(
    dag_id='Download_Stock_Price',
    default_args=default_args,
    description=f'This DAG downloads stock prices and save them into text files.',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['jasondata'],
) as dag:
    # [END instantiate_dag]

    dag.doc_md = """
    This DAG download stock price.
    """  # otherwise, type it like this

    download_task = PythonOperator(
        task_id="download_prices",
        python_callable=download_price,
        provide_context=True
    )

    save_to_mysql_task = PythonOperator(
        task_id='save_to_database',
        python_callable=save_to_mysql_stage,
    )

# [END tutorial]
