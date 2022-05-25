from flask import Flask
from flask_cors import CORS

import os, sys

sys.dont_write_bytecode = True

from database.Database import Database
from routes import createRoutes

# API config 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


Database.createTables()

createRoutes(app)


print('🔥 the server started!')

def main():
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
   main()