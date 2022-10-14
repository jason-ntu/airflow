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

# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from textwrap import dedent
import yfinance as yf

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    'owner': 'jason',
    'depends_on_past': False,
    'email': ['df41022@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# [END default_args]

os.environ["no_proxy"]="*"

def download_price():
    ticker = "MSFT"
    msft = yf.Ticker(ticker)
    hist = msft.history(period="max")
    print(type(hist))
    print(hist.shape)
    print(hist)
   
# [START instantiate_dag]
with DAG(
    dag_id='Download_Stock_Price',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['jasondata'],
) as dag:
    # [END instantiate_dag]

    dag.doc_md = """
    This DAG download stock price.
    """  # otherwise, type it like this
    
    download_task = PythonOperator(
        task_id = "download_prices",
        python_callable = download_price
    )

# [END tutorial]