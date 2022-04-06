
import matplotlib.pyplot as plt
import matplotlib.gridspec as gsp
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import csv, os, random
import datetime as dt
import numpy as np
from datetime import timedelta as delta

root = os.getcwd()


''' Functions for live plot'''

def filter(X,Y,ymin, ymax):
	tmpX, tmpY = [],[]
	for cnt, i in enumerate(Y):
		if ymin < i < ymax:
			tmpX.append(X[cnt])
			tmpY.append(i)
		else:
			pass

	return tmpX, tmpY

def check(file):
	'''handler for _csv.Error: lines contains NULL byte'''
	ex, i = 0,0
	while ex == 0:
		try:
			with open(file, 'r') as f:
				reader = csv.reader(f, delimiter='\t')
				for cnt, line in enumerate(reader):
					pass
			ex = 1

		except csv.Error as e:
			print('NULL byte detected')
			tmp = r'\000'
			cmd = f"tr < {file} -d {tmp} > {file}"
			print(cmd)
			os.system(cmd)
			i += 1
			

def plot(cut=0):
	plots = [i for i in os.listdir(f"{root}/static/") if 'plot' in i]
	for i in plots:
		os.remove(f"{root}/static/{i}")

	files = [i for i in os.listdir(f'{root}/log') if 'log_' in i]
	id = max([int(entry.split('_')[1][:-4]) for entry in files])
	file = f"{root}/log/log_{id}.txt"
	tt, PT100A, PT100B, PT100C, speed, speed_set, diode, diode_set, bus,Power, error =[], [], [],[],[],[],[],[],[],[],[]

	check(file)

	with open(file) as f:
		skip = True
		reader = csv.reader(f,  delimiter='\t')
		for row in reader:
			if skip == True:
				skip = False
			else:
				tt. append(row[0])
				speed.append(int(row[4]))
				speed_set.append(int(row[5]))
				diode.append(float(row[6]))
				diode_set.append(float(row[7]))
				PT100A.append(float(row[1]))
				PT100B.append(float(row[2]))
				PT100C.append(float(row[3]))
				Power.append(float(row[-2]))

	if int(cut) != 0:
		cut = int(cut)
		tt = tt[-cut:]
		speed = speed[-cut:]
		speed_set=speed_set[-cut:]
		diode = diode[-cut:]
		diode_set = diode_set[-cut:]
		PT100A = PT100A[-cut:]
		PT100B = PT100B[-cut:]
		PT100C = PT100C[-cut:]
		Power = Power[-cut:]

	f.close()

	t = [dt.datetime.strptime(item, "%Y-%m-%d %H:%M:%S.%f") for item in tt]
	print(tt[-1])
#	key = int(1000000*sum([float(i) for i in tt[-1].split(' ')[1].split(':')]))
	key = random.randint(0,10000)
	kwargs_frame={'fc':'black'}
	kwargs_ax={'size':12, 'color':'white'}
	kwargs_scatter={'color':'darkslategrey', 'edgecolor':'#007eec', 's':70}
	kwargs_scatter_2={'color':'lightgreen', 'edgecolor':'#007eec', 's':70}

	fig = plt.figure(figsize=(15,10))
	fig.patch.set_alpha(0)
	fig.autofmt_xdate()
	gs = gsp.GridSpec(2,4)
	xfmt = mdates.DateFormatter('%H:%M')
	xfmt2 = mdates.DateFormatter('%H')



	ax0 = fig.add_subplot(gs[:,0:2], **kwargs_frame, ylabel='Temperature (C)', xlabel='Time')
	ax0.scatter(filter(t,PT100A,-240., 100.)[0],filter(t,PT100A,-240.,100.)[1], **kwargs_scatter_2,label=f'Sensor A, {PT100A[-1]}C')
	ax0.scatter(filter(t,PT100B,-240.,100.)[0], filter(t,PT100B,-240,200)[1], **kwargs_scatter, label=f'Sensor B, {PT100B[-1]}C')
	ax0.grid(True)
	ax0.tick_params(colors='white')
	ax0.yaxis.label.set_color('white')
	ax0.xaxis.set_major_formatter(xfmt)
	ax0.spines['bottom'].set_color('white')
	ax0.spines['left'].set_color('white')
	ax0.spines['right'].set_color('white')
	ax0.spines['top'].set_color('white')
	ax0.set_xlabel('Time', color='white')

	ax0.legend()


	tmp_t,tmp_diode_set = [],[]
	for cnt, el in enumerate(diode_set):
		if el != 1.4:
			tmp_diode_set.append(el)
			tmp_t.append(t[cnt])
		else:
			pass
	print(tmp_diode_set[0:10])
	ax1 = fig.add_subplot(gs[0,2], **kwargs_frame, ylabel='Diode (V)')
	ax1.scatter(filter(t,diode,0.5,1.5)[0],filter(t,diode,0.5,1.5)[1], **kwargs_scatter)
	ax1.plot(tmp_t,tmp_diode_set, color='lightgreen')
	ax1.grid(True)
	ax1.tick_params(colors='white')
	ax1.yaxis.label.set_color('white')
	ax1.xaxis.set_major_formatter(xfmt)
	ax1.xaxis.set_major_locator(ticker.LinearLocator(4))
	ax1.spines['bottom'].set_color('white')
	ax1.spines['left'].set_color('white')
	ax1.spines['right'].set_color('white')
	ax1.spines['top'].set_color('white')

	ax2 = fig.add_subplot(gs[1,2], **kwargs_frame, ylabel='Motor Temperature (C)', xlabel='Time')
	ax2.scatter(filter(t,PT100C, 10., 200.)[0], filter(t,PT100C,10.,200.)[1], **kwargs_scatter)
	ax2.tick_params(colors='white')
	ax2.yaxis.label.set_color('white')
	ax2.xaxis.label.set_color('white')
	ax2.xaxis.set_major_formatter(xfmt)
	ax2.xaxis.set_major_locator(ticker.LinearLocator(4))
	ax2.set_xlabel('Time', color='white')
	ax2.spines['bottom'].set_color('white')
	ax2.spines['left'].set_color('white')
	ax2.spines['right'].set_color('white')
	ax2.spines['top'].set_color('white')
	ax2.grid(True)


	ax3 = fig.add_subplot(gs[0,3], **kwargs_frame,  ylabel='Motor Speed (RPM)')
	ax3.scatter(filter(t,speed,-1,4000)[0],filter(t,speed,-1,4000)[1], **kwargs_scatter)
	ax3.tick_params(colors='white')
	ax3.yaxis.label.set_color('white')
	ax3.xaxis.set_major_formatter(xfmt)
	ax3.xaxis.set_major_locator(ticker.LinearLocator(4))
	ax3.spines['bottom'].set_color('white')
	ax3.spines['left'].set_color('white')
	ax3.spines['right'].set_color('white')
	ax3.spines['top'].set_color('white')
	ax3.grid(True)

	ax4 = fig.add_subplot(gs[1,3], **kwargs_frame,xlabel='Time',  ylabel='Power (W)')
	ax4.scatter(filter(t,Power,-10,60)[0],filter(t,Power,-10,60)[1], **kwargs_scatter)
	ax4.tick_params(colors='white')
	ax4.yaxis.label.set_color('white')
	ax4.xaxis.set_major_formatter(xfmt)
	ax4.xaxis.set_major_locator(ticker.LinearLocator(4))
	ax4.spines['bottom'].set_color('white')
	ax4.spines['left'].set_color('white')
	ax4.spines['right'].set_color('white')
	ax4.spines['top'].set_color('white')
	ax4.set_xlabel('Time', color='white')
	ax4.grid(True)

	new = f"{root}/static/plot_{key}.png"
	plt.tight_layout()
	plt.savefig(new)
	plt.close()

	return f"plot_{key}.png",tt[-1],key
