from ssl import VERIFY_ALLOW_PROXY_CERTS
import sys
root = "/home/pi/FLASK"
sys.path.append(f"{root}/backend")


from cooler import Cooler
from flask_restful import Resource, reqparse
import time
from csv import reader 

with open(f"{root}/static/discrete_data.txt") as f:
	R  = reader
	for row in R:
		if "-180 <" in row:
			V_pre = int(row.split(' <=> ')[1])
		elif "-210 <" in row:
			V_pinn = int(row.split(' <=> ')[1])
		else:
			pass

c = Cooler()
class PreHandler(Resource,V_pre):

	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('Pre', type=str)

	def get(self):
		return {'Pre': ''}, 200
		print('hello')

	def post(self):
		args = self.parser.parse_args()
		if args['Pre'] != '':
			state = int(c.read(5))
			time.sleep(0.1)
			try:
				if state != 0:
					c.write(8,V_pre)
				else:
					c.write(5,1)
					time.sleep(1)
					c.write(8,V_pre)
				msg = f"Set to precool mode"
				print(msg)
				c.cmd_log(msg) 
				
			except Exception as e:
				msg = f"Encountered error while attempting to set to precool mode: {e}"
				print(msg)
				c.cmd_log(msg) 
			
			return  {'Pre':'done'},200



class PinnHandler(Resource, V_pinn):
	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('Pinn', type=str)

	def get(self):
		return {'Pinn': ''}, 200

	def post(self):
		args = self.parser.parse_args()
		if args['Pinn'] != '':
			state = int(c.read(5))
			time.sleep(0.1)
			try:
				if state != 0:
					c.write(8,V_pinn)
				else:
					c.write(5,1)
					time.sleep(1)
					c.write(8,V_pinn)

				msg = f"Set to Pinning Mode"
				print(msg)
				c.cmd_log(msg) 
	
			except Exception as e:
				msg = f"Encountered error while attemptingto set pinning mode: {e}"
				print(msg)
				c.cmd_log(msg) 
			
			return  {'Pinn':'done'}, 200


class BaseHandler(Resource):
	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('Base', type=str)

	def get(self):
		return {'Base': ''}, 200

	def post(self):
		args = self.parser.parse_args()
		if args['Base'] != '':
			state = int(c.read(5))
			time.sleep(0.1)

			try:
				if state != 0:
					c.write(8,14000)
					c.write(6,3900)
				else:
					c.write(5,1)
					time.sleep(1)
					c.write(8,14000)
					c.write(6,3900)
			
				msg = f"Set to base-cooling mode"
				print(msg)
				c.cmd_log(msg) 
	
			except Exception as e:
				msg = f"Encountered error while attempting to set to base-cooling mode: {e}"
				print(msg)
				c.cmd_log(msg) 

			return {'Base':'done'}, 200

class OffHandler(Resource):
	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('Off', type=str)

	def get(self):
		return {'Off': ''}, 200

	def post(self):
		args = self.parser.parse_args()
		if args['Off'] != '':
			try:
				c.write(8,6001)
				msg = f"Stopped cooler"
				print(msg)
				c.cmd_log(msg) 
	
			except Exception as e:
				msg = f"Encountered error while attempting to stop cooler: {e}"
				print(msg)
				c.cmd_log(msg) 

			return  {'Off':'done'},200

class DownloadHandler(Resource):
	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('stateDownload', type=str)

	def get(self):
		return {'stateDownload': ''}, 200

	def post(self):
		args = self.parser.parse_args()
		if args['stateDownload'] != '':

			try:
				c.bundle_logs()
				msg = f"Prepared zip file for download"
				print(msg)
				c.cmd_log(msg) 
	
			except Exception as e:
				msg = f"Encountered error while attempting to create zip archive: {e}"
				print(msg)
				c.cmd_log(msg) 

			return  200

class VacuumHandler(Resource):
	def __init__(self, **kwargs):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('vacuum', type=str)

	def get(self):
		return {'vacuum': ''}, 200

	def post(self):
		args = self.parser.parse_args()
		if args['vacuum'] != '':
			return  200
