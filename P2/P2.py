from var import *
from data_management import *
import numpy as np

M = """9829	38	120.5	4
9664	44.9	108.2	3
9308	39.1	107.6	3
9004	54.3	127	3
8731	44	123	3
8425	65	121.7	2
8202	52.5	112.7	2
7984	70.8	105.2	1
7763	59.2	96	1
7586	42.1	123.6	2"""

M = text2dataframe(M)
M = M.to_numpy()

w = var(M[:,0], 1) # MHz
z_max = var(M[:,1], 0.2) # mm
z_min = var(M[:,2], 0.2) # mm

N = var(M[:,3], 0)

lambda_2 = f_var(lambda x: (x[1] - x[0])/x[2], [z_max, z_min, N], r"\lambda/2")
k = f_var(lambda x: 2*np.pi/x[0], [lambda_2])

# k.vs(w)

import matplotlib.pyplot as plt

plot_args = {"marker": "o",
                "capsize": 4,
                "markerfacecolor": "None",
                "linestyle": "",
                }

plt.errorbar(k.value, w.value, w.err, k.err, **plot_args) # x, y, \Delta y, \Delta x

ax = plt.gca()
ax.set_box_aspect(1.0)
plt.xlabel(r"$\beta$ (rad/mm)")
plt.ylabel(r"$\omega$ (rad/s)")
plt.grid(visible = True)
plt.minorticks_on()

plt.show()

# Cálculo frecuencia de corte teórica

a = var(2.25, 0.05) # cm
a.redefine(lambda x: x[0]/100) # m
k_c = f_var(lambda x: np.pi/x[0], [a], r"$k_c$") # rad/m

c = var(299792456, 1) # m/s

w_c = f_var(lambda x: x[0]*x[1], [k_c, c])
f_c = f_var(lambda x: x[0]/2/np.pi, [w_c], "Frecuencia de corte teorica", "Hz")
f_c.redefine(lambda x: x[0]/1e6, "MHz")

f_c.show()

# Frecuencia de corte experimental:

beta2 = f_var(lambda x: x[0]**2, [k], r"$\beta^2$", r"mm$^{-2}$")
w2 = f_var(lambda x: x[0]**2, [w], r"$\omega^2$", r"rad$^2$/s$^2$")

plt.close()
[m, n] = beta2.vs(w2)

f = lambda t: m.value*t + n.value
t = np.linspace(-0.05*1e8, 1*1e8, 20)

ax = plt.gca()
ax.plot(t, f(t), color = "C0")

plt.show()

import sympy as sp
wc_exp = f_var(lambda x: sp.sqrt(-x[1]/x[0]), [m,n])
fc_exp = f_var(lambda x: x[0]/2/np.pi, [wc_exp], "Frecuencia de corte experimental", "MHz")
fc_exp.show()


# Cálculo de las impedancias

SWR = var([20, 20, 1.45], [2, 1, 0.05])
Gamma = f_var(lambda x: (1+x[0])/(1-x[0]), [SWR])