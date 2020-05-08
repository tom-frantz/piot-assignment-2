# Backend

- `pipenv` is used for virtual environment.
  To install: `pip3 install pipenv`

- Environment variable settings for development:

  ```
  export FLASK_APP=master_pi.py
  export FLASK_ENV=development
  export My_SQL={your local MySQL password}
  ```

- Run on local server:
  Make sure your MySQL server process `mysqld` is running.

  ```
  pipenv install
  pipenv shell
  flask run
  ```
  
- Default port: `5000`
