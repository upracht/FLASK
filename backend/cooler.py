import sys
root = "/home/pi/FLASK"
sys.path.append(f"{root}/backend")

import board, digitalio, adafruit_max31865
from pymodbus.client.sync import ModbusSerialClient
import time, os
import datetime as dt
import numpy as np
from zipfile import ZipFile
from csv import reader

with open(f"{root}/static/discrete_data.txt") as f:
	R  = reader(f)
	for cnt,row in enumerate(R):
		if cnt == 7:
			V_pre = int(round(float(row[0].split(' <-> ')[1]),1))
		elif cnt == 8:
			V_pinn = int(round(float(row[0].split(' <-> ')[1]),1))
		else:
			pass
print(V_pre)
print(V_pinn)

class Cooler():
	def __init__(self, error='tbd'):
 		# MODBUS INIT
		i, con = 0, False
		while con == False:
			try:
				self.port = f"/dev/ttyUSB{i}"
				self.client = ModbusSerialClient(method='rtu', port = self.port, baudrate=38400)
			except Exception as e:
				error = e
				pass
			if self.client.connect() == True:
				con = True
			else:
				i += 1

			if i == 100:
				con = True
				msg = f"Encountered error while attempting to set to connect to cooler: {error}"
				print(msg)
				self.cmd_log(msg) 

		self.connected = "CONNECTED"



	def read(self,address):
		res = 0
		try:
			res = self.client.readwrite_registers(read_address=address, read_count=1,  write_address=24, write_registers=51, unit=51).registers[0]
		except (AttributeError,UnboundLocalError) as e:
			print(f'error while reading - {e}')
		return res

	def write(self,address,value):
		try:
			self.client.readwrite_registers(read_address=address, read_count=1,  write_address=address, write_registers=value, unit=51).registers[0]
		except (AttributeError,UnboundLocalError) as e:
			print(f'error while writing - {e}')



	def PT100(self,spi):
		#spi = busio.SPI(board.SCK,MOSI=board.MOSI, MISO=board.MISO)
		cs = digitalio.DigitalInOut(board.D13)
		sensor = adafruit_max31865.MAX31865(spi,cs,rtd_nominal=100.00, ref_resistor=430.0, wires=2)
		T_ybco = round(sensor.temperature,2)
		cs = digitalio.DigitalInOut(board.D19)
		sensor = adafruit_max31865.MAX31865(spi,cs,rtd_nominal=100.00, ref_resistor=430.0, wires=2)
		T_kf = round(sensor.temperature,2)
		cs = digitalio.DigitalInOut(board.D26)
		sensor = adafruit_max31865.MAX31865(spi,cs,rtd_nominal=100.00, ref_resistor=430.0, wires=2)
		T_motor = round(sensor.temperature,2)
		#print(f"{T_motor}\t{T_ybco}\t{T_kf}")
		return [T_ybco,T_kf,T_motor]

	def Power(self, Vdc=24):
		I = 1
		return Vdc * I

	def cmd_log(self, message):
		src = f"{root}/log/cmd_log.txt"
		with open(src, 'a+') as f:
			f.write(f"{dt.datetime.now()}\t{message}\n")


	def log(self, spi):
		log_files = [i for i in os.listdir(f"{root}/log") if 'log_' in i]
		if log_files == []:
			tmp_log = f'{root}/log/log_0.txt'
			init = True
		else:
			id = max([int(entry.split('_')[1][:-4]) for entry in log_files])
			tmp_log = f'{root}/log/log_{id}.txt'

			if os.path.getsize(f'{root}/log/log_{id}.txt') > 50000:
				tmp_log = f'{root}/log/log_{id+1}.txt'
				init = True
			else:
				init = False
		t = dt.datetime.now()
		rpm = self.read(0)
		if rpm > 4000:
			rpm = 0
		data = f"{t}\t{self.PT100(spi)[1]}\t{self.PT100(spi)[0]}\t{self.PT100(spi)[2]}\t{rpm}\t{self.read(6)}\t{round(self.read(1)*0.0001,4)}\t{round(self.read(8)*0.0001,4)}\t{round(self.read(2)/10.,1)}\t{round(self.read(2)/10.*self.Power(),2)}\t{self.read(4)}\n"
		with open(tmp_log, 'a+') as f:
			if init == True:
				f.write("Time\tT Coldfinger (C)\tT Supra (C)\tT Motor (C)\tSpeed (rpm)\tSpeed set (rpm)\tDiode (V)\tDiode set (V)\tBus (V)\tPower(W)\tError code\n")
			f.write(data)



	def bundle_logs(self):
		dest = f"{root}/static"
		src = f"{root}/log"

		old = [i for i in os.listdir(dest) if '.zip' in i]
		if old != []:
			os.remove(f"{dest}/{old[0]}")
			while os.path.isfile(f"{dest}/{old[0]}") == True:
				print('...')

			print(f"remove {dest}/{old[0]}")


		now = str(dt.datetime.now().date())
		bundle_name = f'{dest}/archive_{now}.zip'
		bundle = ZipFile(bundle_name, 'w')
		for i in os.listdir(src):
			file = f"{src}/{i}"
			bundle.write(file, os.path.basename(file))
		bundle.close()

		return bundle_name

	def vacuum_test(spi, base=-212, max_hours_down=3, heat_break_rpm=0):
		self.cmd.log('Start performance test')
		if self.read(8) == V_pinn:    # pinning mode 
			self.write(8,14000)
		
			init_time = dt.datetime.now()
			reach = True
			while self.PT100(spi)[0] > base and reach:
				time.sleep(1)
				if dt.datetime.now() > init_time + dt.timedelta(hours=max_hours_down):
					reach = False
					self.cmd_log('ABORT performance test: did no reach base T')

			if heat_break_rpm == 0:
				self.write(8,10000)
				init_time_up = dt.datetime.now()
				while self.PT100(spi)[0] < -210:
					pass
				self.write(8,V_pinn)

				if reach:
					time_up = (dt.datetime.now() - init_time_up).total_seconds()
					if not os.path.isfile(f'{root}/log/performance_log.txt'):			
						with open(f'{root}/log/performance_log.txt', 'w+') as f:
							line = "date\twarming time (s)\t motor load (RPM)\n"
							f.write(line)
					with open(f'{root}/log/performance_log.txt', 'a+') as f:
						line = f"{dt.datetime.now().date()}\t{time_up}\t{heat_break_rpm}\n"
						f.write(line)

					self.cmd_log('Finished performance test')

			else:
				self.write(6,heat_break_rpm)
				init_time_up = dt.datetime.now()
				while self.PT100(spi)[0] < -210:
					pass

				self.write(5,1)
				time.sleep(1)
				self.write(8,V_pinn)

				if reach:
					time_up = (dt.datetime.now() - init_time_up).total_seconds()
					if not os.path.isfile(f'{root}/log/performance_log.txt'):			
						with open('{root}/log/performance_log.txt', 'w+') as f:
							line = "date\twarming time (s)\tmotor load (RPM)\n"
							f.write(line)
					with open(f'{root}/log/performance_log.txt', 'a+') as f:
						line = f"{dt.datetime.now().date()}\t{time_up}\t{heat_break_rpm}\n"
						f.write(line)

					self.cmd_log('Finished performance test')

		else:
			self.cmd_log('Could not start peformance test routine because cryostat is not in pinning state')



