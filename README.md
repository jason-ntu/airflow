# airflow

- [Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
  1. `airflow standalone` or
  2.
  ```
  airflow db init

  airflow users create \
      --username admin \
      --firstname Peter \
      --lastname Parker \
      --role Admin \
      --email spiderman@superhero.org
  
  # set password to 'airflow'

  airflow webserver --port 8080

  airflow scheduler
  ```

- practice for **download_stock_price**:
  - add this into config: `{"stocks":["Meta"]}`

- run mysql on docker:
  - `docker run --name local_mysql -e MYSQL_ROOT_PASSWORD=airflow -p 3306:3306 -d mysql:5.7`

- [ImportError: No module named 'MySQL'](https://stackoverflow.com/questions/32877671/importerror-no-module-named-mysql)