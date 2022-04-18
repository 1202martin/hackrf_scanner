from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS
from hackrf_scan_live_ssh import Scanner    #Change to hackrf_scan_live if ssh tunneling isn't preferred for any reason
import os,time, json

app = Flask(__name__)  
CORS(app)
api = Api(
    app,
    version = 0.1,
    title = "HackRF Control server",
    description = "IDfense API Server",
    terms_url='/',
    contact="jungh.park@cs.stonybrook.edu",
    license="MIT"
)  

f = open('hackrf.json')
configs = json.load(f)

SSH_CONFIG = configs["SSH_CONFIG"]
DB_CONFIG = configs["HACKRF_DB_CONFIG"]

print("ssh config = ", SSH_CONFIG)

Scanner.init_table(Scanner, SSH_CONFIG, DB_CONFIG)


# 433, 915, 2400, 5000
@api.route('/433')  
class use433(Resource):
    def get(self): 
        #function call
        print("433")
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG, DB_CONFIG, 413, 453, 1, 0)

@api.route('/915')  
class use915(Resource):
    def get(self): 
        #function call
        print("915")
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, 895, 935, 1, 0)

@api.route('/2400')  
class use2400(Resource):
    def get(self): 
        #function call
        print("2400")
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, 2380, 2420, 1, 0)

@api.route('/5000')  
class use5000(Resource):
    def get(self): 
        #function call
        print("5000")
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, 4980, 5020, 1, 0)

@api.route('/all')
class useAll(Resource):
    def get(self):
        #function call
        print('all')
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG,413, 5020, 1, 0)

if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0', port=5000)
      