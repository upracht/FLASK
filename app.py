#!/usr/bin/python3
import time, os, busio, board
import datetime as dt

from flask import Flask, render_template, request, send_from_directory, send_file
from flask_restful import Api

from fullAPI import VacuumHandler, PreHandler, PinnHandler,BaseHandler,OffHandler, DownloadHandler
from cooler import Cooler
from plotter import plot


# let some time pass to allow WiFi access point so build up when loaded on boot
time.sleep(40) 


# Initialize webframework and required APIs
#ip = '10.0.0.1'

os.system("hostname -I > tmp")
ip = os.popen("head tmp").read().split(' ')[0]
root = os.getcwd()
app = Flask(__name__, template_folder=f"{root}/templates/")
api = Api(app)
api.add_resource(PreHandler, '/api/Pre')
api.add_resource(PinnHandler, '/api/Pinn')
api.add_resource(BaseHandler, '/api/Base')
api.add_resource(OffHandler, '/api/Off')
api.add_resource(DownloadHandler, '/api/stateDownload')
api.add_resource(VacuumHandler, '/api/vacuum')

# Initialize cooler and max31865 temperature sensor
global sri, spi
sri = Cooler()
spi = busio.SPI(board.SCK,MOSI=board.MOSI, MISO=board.MISO)





def dir_last_updated(folder):
	''' Auxiliary function to escape caching in the web browser. Returns the age of the last modified file in folder for the 
	last_updated parameter in render_template. 
	Note: seems depreciated in newer versions of Flask 
	'''
	s = str(max(os.path.getmtime(os.path.join(root_path,f)) for root_path,dirs,files in os.walk(folder) for f in files))
	return s

def VtoT(V):
	''' Turns the measured diode voltage into temperature'''
	para = [1.604782468904384e-11, -6.438297661009054e-07, 0.009675297504190352, -64.60449287705708, 161700.15813458277]
	T = para[0]*V**4 + para[1]*V**3 + para[2]*V**2 + para[3]*V + para[4]
	return round(T,2)

def rpm(x):
	'''Auxiliary function to filter out unrealistically large RPM '''
	if x > 4000:
		return 0
	else:
		return x

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(f'{root}/js', path)

# GUI screen
@app.route('/user')
def expert():
    return render_template( f'UI_m.html', last_updated=dir_last_updated(f'{root}'),rpm = rpm(sri.read(0)), T = VtoT(int(sri.read(1))))

# Runs the data sampling and logging routine upon calling
@app.route('/sample')
def sample():
	sri.log(spi)
	return 'logged'

# Live data screen
@app.route('/live_<RANGE>')
def live(RANGE):
	file,tt,key = plot(cut=RANGE)
	return render_template(f"log.html", last_updated_2=dir_last_updated(f'{root}static'), d = file)

# Link to data archive 
@app.route('/down')
def download():
	now = dt.datetime.now().date()
	name = f"{root}/static/archive_{now}.zip"
	return send_file(name, as_attachment=True, cache_timeout=1)

# Link to vacuum performance test
@app.route("/vacuum_performance_test")
def vac_test():
	ans = c.vacuum_test(spi)
	return ans

if __name__ == '__main__':
    app.run(debug=True, host=ip, port=13378)
