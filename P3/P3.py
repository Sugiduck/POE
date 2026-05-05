import numpy as np
import matplotlib.pyplot as plt
from var import *
from data_management import *

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

"""
M = text2dataframe(M)
M = M.to_numpy()

w = var(M[:,0], 1, "$\omega$", "MHz", str_format = "{:.1f}") # MHz
w.redefine(lambda x: 2*np.pi*x[0])
# w = f_var(lambda x: 2*np.pi*x[0], [f]) # 1e6 rad/s
z_max = var(M[:,1], 0.2) # mm
z_min = var(M[:,2], 0.2) # mm

N = var(M[:,3], 0, str_format = "{:.0f}")

# print(var2ipython_latex([w, z_min, z_max, N]).replace("\\", "\\\\"))
print(var2ipython_latex([w, z_min, z_max, N]))
"""

M = """9	16.1	-19.09	0.01
8.75	15.8	-19.03	0.01
8.5	15.5	-19.01	0.01
8.25	15.1	-18.99	0.01
8	14.5	-18.95	0.01
7.75	13.8	-18.94	0.01
7.5	12.9	-18.98	0.01
7.25	11.6	-19.33	0.01
7	10.1	-20.03	0.01
6.75	8.2	-21.45	0.03
6.5	6.1	-23.52	0.03
6.25	4	-26.06	0.03
6	2.4	-29.23	0.03
5.75	1.2	-32.63	0.03
5.5	0.6	-37	1
5.25	0.3	-37	2
5	0.1	-38	4
4.75	0	-43	5"""

M = text2dataframe(M)
M = M.to_numpy()

x = var(M[:,0], 0.01, "Posición atenuador", "u.a.")
V = var(M[:,1], 0.1, "Voltaje", "mV")
V.redefine(lambda x: -x[0])
P_dB = var(M[:,2], M[:,3], "Potencia", "dbm")
P = f_var(lambda x: 10**((x[0]/10)-3), [P_dB], "Potencia", "W")

print(var2ipython_latex([x, V, P_dB]))

options = {"fitlm": False, "errors": True}
plot_args = {"markerfacecolor": None}

P.vs(V, options = options, plot_args = plot_args)
plt.savefig("~P3/images/P_vs_V")
# plt.show()

plt.close()
P_dB.vs(V, options = options, plot_args = plot_args)
plt.savefig("~P3/images/PdBm_vs_V")
# plt.show()

# Parte 2

M = """9	42	42.1	0	0	0.6	0.5
8.75	40.1	40.8	0	0	0.6	0.5
8.5	37.8	38.6	0	0	0.6	0.5
8.25	34.7	36.2	0	0	0.6	0.4
8	31	32.8	0	0	0.5	0.4
7.75	27	29.1	0	0	0.4	0.4
7.5	22.6	25	0	0	0.4	0.3
7.25	18.1	20.5	0	0	0.3	0.3
7	13.7	16	0	0	0.3	0.2
6.75	9.8	11.8	0	0	0.2	0.1
6.5	6.4	8.1	0	0	0.1	0.1
6.25	4	5.1	0	0	0	0
6	2.2	2.9	0	0	0	0
5.75	1.1	1.6	0	0	0	0
5.5	0.6	0.8	0	0	0	0
5.25	0.2	0.4	0	0	0	0
5	0.1	0.2	0	0	0	0
4.75	0	0.1	0	0	0	0"""

D32 = var(M[:,1], 0.1)
D23 = var(M[:,2], 0.1)