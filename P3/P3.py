import numpy as np
import matplotlib.pyplot as plt
from var import *
from data_management import *

path = "P3/"

M = """9	18.7	-19.09	0.01
8.75	18.6	-19.03	0.01
8.5	18.5	-19.01	0.01
8.25	18.3	-18.99	0.01
8	15.7	-18.95	0.01
7.75	14.8	-18.94	0.01
7.5	13.9	-18.98	0.01
7.25	12.5	-19.33	0.01
7	10.8	-20.03	0.01
6.75	8.7	-21.45	0.03
6.5	6.4	-23.52	0.03
6.25	4.2	-26.06	0.03
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
V.show()
P_dB = var(M[:,2], M[:,3], "Potencia", "dBm")
# P = f_var(lambda x: 10**((x[0]/10)-3), [P_dB], "Potencia", "W")

delta_P = var(P_dB.err, 0, r"\Delta P", "dBm")
print(var2ipython_latex([x, V, P_dB]))

options = {"fitlm": False, "errors": True}
plot_args = {"markerfacecolor": "None", "capsize": 4}

# P.vs(V, options = options, plot_args = plot_args)
# plt.savefig(path + "images/P_vs_V")
# plt.show()

plt.close()
P_dB.vs(V, options = options, plot_args = plot_args)
plt.savefig(path + "images/PdBm_vs_V")
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

M = text2dataframe(M)
M = M.to_numpy()

V_D32 = var(M[:,1], 0.1, "V", "mV")
V_D23 = var(M[:,2], 0.1, "V", "mV")
V_D31 = var(M[:,3], 0.1, "V", "mV")
V_D13 = var(M[:,4], 0.1, "V", "mV")
V_D21 = var(M[:,5], 0.1, "V", "mV")
V_D12 = var(M[:,6], 0.1, "V", "mV")

plt.close()
V_D32.vs(x, options = options, plot_args = plot_args)
V_D23.vs(x, options = options, plot_args = plot_args)
# plt.savefig(path + "images/V_vs_atenuador")
# plt.show()


def interpol (x):
    x_cal = V.value
    y_cal = P_dB.value

    if x < min(x_cal) or x > max(x_cal):
        return min(x_cal)

    for i in range(len(x_cal)):
        if x > x_cal[i]:
            x0 = x_cal[i-1]
            y0 = y_cal[i-1]
            x1 = x_cal[i]
            y1 = y_cal[i]
            break

    return y0 + ((y1 - y0)/(x1-x0))*x

P_dB.name = "Potencia de entrada"
P_D32 = var([interpol(-xi) for xi in M[:,1]], 0, "Potencia de salida", "dBm")
P_D23 = var([interpol(-xi) for xi in M[:,2]], 0, "Potencia de salida", "dBm")
P_D31 = var([interpol(-xi) for xi in M[:,3]], 0, "Potencia de salida", "dBm")
P_D13 = var([interpol(-xi) for xi in M[:,4]], 0, "Potencia de salida", "dBm")
P_D21 = var([interpol(-xi) for xi in M[:,5]], 0, "Potencia de salida", "dBm")
P_D12 = var([interpol(-xi) for xi in M[:,6]], 0, "Potencia de salida", "dBm")

plt.close()
P_D32.vs(x, options = options, plot_args = plot_args)
P_D23.vs(x, options = options, plot_args = plot_args)
# P_D31.vs()
plt.savefig(path + "images/P_vs_atenuador")
# plt.show()

plt.close()
ax = plt.gca()
ax.set_title("Entrada en puerta 2")
P_D21.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 1"})
P_D23.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 3"})
plt.legend()
plt.savefig(path + "images/P_salida_vs_entrada_2")
# plt.show()

plt.close()
ax = plt.gca()
ax.set_title("Entrada en puerta 1")
P_D12.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 2"})
P_D13.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 3"})
plt.legend()
plt.savefig(path + "images/P_salida_vs_entrada_1")

plt.close()
ax = plt.gca()
ax.set_title("Entrada en puerta 3")
P_D31.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 1"})
P_D32.vs(P_dB, options = options, plot_args = plot_args | {"label": "Salida por puerto 2"})
plt.legend()
plt.savefig(path + "images/P_salida_vs_entrada_3")


# Segundo cacharro ("El cilindrico")

M = """9.00	18.2	3.5
8.75	17.6	3.3
8.50	17.2	3.2
8.25	16.8	3.0
8.00	16.1	2.6
7.75	15.3	2.2
7.50	14.0	1.9
7.25	12.2	1.5
7.00	9.9	1.1
6.75	7.2	0.7
6.50	4.8	0.4
6.25	2.8	0.2
6.00	1.4	0.1
5.75	0.7	0.0
5.50	0.3	0.0
5.25	0.1	0.0
5.00	0.0	0.0
4.75	0.0	0.0"""

M = text2dataframe(M)
M = M.to_numpy()

P_D12 = var([interpol(-xi) for xi in M[:,1]], 0, "Potencia de salida", "dBm")
P_D21 = var([interpol(-xi) for xi in M[:,2]], 0, "Potencia de salida", "dBm")

plt.close()
ax = plt.gca()
ax.set_title("Elemento de dos puertas")
P_D12.vs(P_dB, options = options, plot_args = plot_args | {"label": "Entrada por puerta 1"})
P_D21.vs(P_dB, options = options, plot_args = plot_args | {"label": "Entrada por puerta 2"})
plt.legend()
plt.savefig(path + "images/P_cilindro")



explicacion = "En la curva de calibración del cristal detector, observamos que para los valores usados de potencia más altos, el voltaje varía bastante y no está unívocamente determinado (la curva tiene más de un valor de potencia para un mismo voltaje), por lo que no será útil para medir potencias. Para valores de voltaje entre -1 mV y -12.5 mV se encuentra una zona lineal, que es ideal para calcular la potencia en función del voltaje emitido por el cristal detector. Para potencias cercanas a 0, lógicamente, el voltaje también se va a 0."