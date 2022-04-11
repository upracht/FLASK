import sys
root = "/home/pi/FLASK"
sys.path.append(f"{root}/backend")

from cooler import Cooler
import datetime as dt
import board, digitalio, adafruit_max31865
from pymodbus.client.sync import ModbusSerialClient
import time, os, csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def log(spi):
    file = f"{root}/static/cal.txt"
    if not os.path.isfile(file):
        with open(file, 'w+') as f:
            f.write("Time\tT YBCO (C)\tT CF (C)\tDiode (V)\n")
    temps = c.PT100(spi)
    V = c.read(1)
    
    with open(file, 'a+') as f:
        line = f"{dt.datetime.now()}\t{round(c.PT100(spi)[0],3)}\t{round(c.PT100(spi)[1],3)}\t{c.read(1)}\n"
        f.write(line)
        print(line)

def poly(x,a,b,c,d,e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e 


def TtoV(V,T):
    init = [1e-11, -6e-07, 0.0096, -64, 161700]
    popt, pcov = curve_fit(poly,V,T,init)
    return popt




c = Cooler()
spi = busio.SPI(board.SCK,MOSI=board.MOSI, MISO=board.MISO)




targets = [-170, -180, -190, -200, -210, -215]
frame = 0.1
diff = 0.5
cal_T, cal_V = [],[]

print("This routine sweeps an entire ambient to low-T run to generate the diode calibration")
ans = input("Run calibration (y/n)? ")

if ans in ['yes', 'y', 'Y', 'Yes']:

    c.write(5,1)
    time.sleep(1)
    c.write(8,14000)
    c.write(6,3900)

    for target in targets:
        print(f'Cooling to {target}')
        while not target - frame < c.PT100(spi)[1] < target + frame:
            log(spi)
            time.sleep(60)
        
        diode_set = c.read(1)
        c.write(8,1)
        init_ybco = c.PT100(spi)[0]
        time.sleep(60)
        
        while init_ybco - c.PT100(spi)[1] > diff:
            log(spi)
            init_ybco = c.PT100(spi)[1]
            V = c.read(1)
            time.sleep(60)
        
        with open('{root}/static/discrete_data.txt', 'a+') as f:
            f.write(f"{init_ybco}\t{V}")

        c.write(8,14000)

    print("\n\n\nT sweep completed, starting analysis...")
    c.write(6001)

    T_ybco, V = [],[]
    file = f"{root}/static/discrete_data.txt"
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            T_ybco.append(float(row[0]))
            V.append(float(row[1]))

    popt = VtoT(V,T_ybco)

    with open(file, 'a') as f:
        line = f"\n-180C <-> {poly(-180,*popt)}\n-210C <-> {poly(-210,*popt)}"
        print(line)
        f.write(line)

    
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.scatter(T_ybco,V)
T_fit = np.linspace(-170,-215,100)
ax.plot(T_fit, [poly(i,*popt) for i in T_fit], label=f"fO(4) poylnom\n{popt}")
ax.set_ylabel('Diode Voltage (10e-4 V)')
ax.set_xlabel('YBCO Temperature (C)')
ax.legend()
plt.savefig(f'{root}/static/cal.png') 
plt.close()          

