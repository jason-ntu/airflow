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
  - add this into config: `{"stocks":["META"]}`

- run mysql on docker:
  - `docker run --name local_mysql -e MYSQL_ROOT_PASSWORD=airflow -p 3306:3306 -d mysql:5.7`

- [How can I add new "Conn Types" to Airflow 2.0?](https://stackoverflow.com/questions/65890511/how-can-i-add-new-conn-types-to-airflow-2-0)