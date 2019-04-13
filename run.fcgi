#!venv/bin/python
from flup.server.fcgi import WSGIServer
from weatherapplication import app
from dotenv import load_dotenv
if __name__ == '__main__':
    load_dotenv(".env")
    WSGIServer(app).run()
