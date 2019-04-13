#!venv/bin/python
from flup.server.fcgi import WSGIServer
from weatherapplication import app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    #load_dotenv(".env")
    with open("sql_password.pass", "r") as fin:
        sql_password = fin.read()
    os.environ["SQL_PASSWORD"] = sql_password.replace("\n", "")
    WSGIServer(app).run()
