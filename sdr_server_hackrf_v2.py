from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS
from hackrf_scan_live_ssh_v2 import Scanner    #Change to hackrf_scan_live if ssh tunneling isn't preferred for any reason
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

# Scanner.init_table(Scanner, SSH_CONFIG, DB_CONFIG)

@api.route("/")
class home(Resource):
    def get(self):
        print('home')
        Scanner.scan_flag = False
        time.sleep(1)

# 433, 915, 2400, 5000
# User input can be taken from calling on url by adding "?min_freq=xx&max_freq=xx&cen_freq=xx&bin_size=xx" to the normal url.
@api.route('/433')
class use433(Resource):
    def get(self): 
        print("433")
        freq_range = 433
        parameter_dict = request.args.to_dict()
        if len(parameter_dict) == 0:
            min_freq = 413
            max_freq = 453
            bin_size = (max_freq-min_freq)/5000
        else:
            print(parameter_dict)
            min_freq = int(parameter_dict['min_freq'])
            max_freq = int(parameter_dict['max_freq'])
            if parameter_dict['bin_size'] == '':
                bin_size = (max_freq-min_freq)/5000
            else:
                bin_size = float(parameter_dict['bin_size'])
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG, DB_CONFIG, min_freq, max_freq, bin_size, freq_range, 0)

@api.route('/915')  
class use915(Resource):
    def get(self):
        print("915")
        freq_range = 915
        parameter_dict = request.args.to_dict()
        if len(parameter_dict) == 0:
            min_freq = 895
            max_freq = 935
            bin_size = (max_freq-min_freq)/5000
            print(bin_size)
        else:
            min_freq = int(parameter_dict['min_freq'])
            max_freq = int(parameter_dict['max_freq'])
            if parameter_dict['bin_size'] == '':
                bin_size = (max_freq-min_freq)/5000
            else:
                bin_size = float(parameter_dict['bin_size'])

        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, min_freq, max_freq, bin_size, freq_range, 0)

@api.route('/2400')  
class use2400(Resource):
    def get(self): 
        print("2400")
        freq_range = 2400
        parameter_dict = request.args.to_dict()
        if len(parameter_dict) == 0:
            min_freq = 2380
            max_freq = 2420
            bin_size = (max_freq-min_freq)/5000
        else:
            min_freq = int(parameter_dict['min_freq'])
            max_freq = int(parameter_dict['max_freq'])
            if parameter_dict['bin_size'] == '':
                bin_size = (max_freq-min_freq)/5000
            else:
                bin_size = float(parameter_dict['bin_size'])

        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, min_freq, max_freq, bin_size, freq_range, 0)

@api.route('/5000')  
class use5000(Resource):
    def get(self): 
        print("5000")
        freq_range = 5000
        parameter_dict = request.args.to_dict()
        if len(parameter_dict) == 0:
            min_freq = 4980
            max_freq = 5020
            bin_size = (max_freq-min_freq)/5000
        else:
            min_freq = int(parameter_dict['min_freq'])
            max_freq = int(parameter_dict['max_freq'])
            if parameter_dict['bin_size'] == '':
                bin_size = (max_freq-min_freq)/5000
            else:
                bin_size = float(parameter_dict['bin_size'])

        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG, min_freq, max_freq, bin_size, freq_range, 0)

@api.route('/all')
class useAll(Resource):
    def get(self):
        print('all')
        freq_range = 0
        parameter_dict = request.args.to_dict()
        if len(parameter_dict) == 0:
            min_freq = 413
            max_freq = 5020
            bin_size = 1
        else:
            min_freq = int(parameter_dict['min_freq'])
            max_freq = int(parameter_dict['max_freq'])
            if parameter_dict['bin_size'] == '':
                bin_size = 1
            else:
                bin_size = float(parameter_dict['bin_size'])
            
        Scanner.scan_flag = False
        time.sleep(1)
        Scanner.freq_scan_start_end(Scanner, SSH_CONFIG,DB_CONFIG,min_freq, max_freq, bin_size, freq_range, 0)

if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0', port=5000)
      