from flask import Flask, render_template, redirect, make_response, jsonify, request
import pymysql
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
   entries = request.args.get('entries', 500)
   return render_template('CalDayVis.html', entries=entries)
   #return render_template('Debug.html')

@app.route('/data')
def get_data():
   """
   The URL at this query takes an optional query strings: entries.

   Entries is a number referring to the n most recent desired entries

   this would be in the format: https://www.ocf.berkeley.edu/~ankurmahesh/weatherwebsite/data?entries=4
   """
   entries = request.args.get('entries', None)
   
   sql_hostname = 'mysql'
   sql_username='ankurmahesh'

   sql_password = 'b1C4ZcoJR8lTXMm3EocB46ek'
   #sql_password = os.environ["SQL_PASSWORD"]

   #with open("sql_password", "r") as f:
   #    sql_password = f.read().replace("\n", "")
   #with open("ssh_password", "r") as f:
   #    ssh_password = f.read().replace("\n", "")

   sql_main_database='ankurmahesh'
   sql_port = 3306

   conn = pymysql.connect(host='mysql', user=sql_username,
                passwd=sql_password, db=sql_main_database,
                port=sql_port, autocommit=True)
   query = "SELECT * from weatherdata;"
   data = pd.read_sql_query(query, conn)
   
   #Select the N most recent entries from the table using the "tail" method
   #N is the "entries" variable 
   if entries is not None:
       data = data.tail(int(entries))
   data["date"] = data["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
   conn.close()
   return data.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
