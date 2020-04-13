import numpy as np
import matplotlib.pylab as pl
from scipy.optimize import curve_fit
from datetime import datetime
import requests


def func(x, a0, a1, a2):
    return (a0 * (np.tanh((x + a1) * a2) + 1))


def fit(func, x, y, popt=None):
    popt = [50000, -30, 0.1]
    try:
        param_bounds = ([0, -60, 0], [1e6, -10, 1.])
        popt1, pcov = curve_fit(func, x, y, p0=popt, bounds=param_bounds)
    except:
        print('Fit failed!')
        return [[0, 0, 0], None]

    return [popt1, pcov]


url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/key-countries-pivoted.csv"
myfile = requests.get(url)
open('download.csv', 'wb').write(myfile.content)
path = './download.csv'

f = open(path)
lines = f.readlines()
f.close()

names = lines[0].split(',')

for i in range(len(names)):
    names[i] = names[i].replace('\n', '')

data = np.genfromtxt(path, delimiter=',', skip_header=1, names=names)
count = 0

date = datetime.today().strftime('%m %d, %Y')

for name in names[1:]:

    # extract y values after 100
    y = data[name]
    ind = np.where(y < 100)
    y = np.delete(y, ind)

    len_data = len(y)
    x = np.arange(len_data)

    popt1, pcov = fit(func, x, y)

    delta_hd = np.round(len(y) - 1 + popt1[1], 1)
    print(name, 'delta hump day: ', delta_hd)
    x_off = popt1[1]

    x_fit = np.linspace(0, 120, 100)

    pl.subplot(2, 4, count + 1)

    pl.plot([0, 0], [0, 1000000], 'r--', alpha=0.5)
    pl.plot([-30, 30], [2 * popt1[0], 2 * popt1[0]], 'r--', alpha=0.5)

    pl.plot(x_fit + x_off, func(x_fit, *popt1), label='Fit')
    pl.plot(x + x_off, y, 'x', color='r', label='Data')

    conv = 'high'
    if delta_hd < 2:
        conv = 'low'
    if 2 <= delta_hd <= 10:
        conv = 'medium'

    textstr = '\n'.join((name, r'Delta hump day: ' + str(delta_hd), 'Confidence: ' + conv, str(date)))

    props = dict(boxstyle='round', facecolor='w', alpha=0.8)

    pl.text(-25, 162000, textstr, fontsize=10, bbox=props)

    if not (count == 0 or count == 4):
        pl.yticks([])
    else:
        pl.ylabel('Number of confirmed cases')

    pl.xlim([-27, 30])
    pl.ylim([0, 200000])

    pl.xlabel('Delta hump day (d)')

    pl.legend(loc=1)
    count += 1

pl.show()
