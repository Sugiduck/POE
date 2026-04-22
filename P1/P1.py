import numpy as np
import matplotlib.pyplot as plt
from data_management import *
from var import *

R0 = var(50, 2.5)
v_phi = var(2e8, 1e7)

M = """100	9.88	0.01	5.5
200	19.76	0.01	10.5
300	29.9	0.1	16.9"""

M = text2dataframe(M)
M = M.to_numpy()

z = var(M[:,0], 0.02, "z", "m") # m
C = var(M[:,1], M[:,2], "C", "nF") # nF
R = var(M[:,3], 0.1, "R") # \Omega

# C.redefine(lambda x: x[0]*1e-9) # F

# [C, C_0] = C.vs(l) # C -> F/m
# plt.savefig("./P1/images/C_vs_z")
# plt.close()

C_esp = f_var(lambda x: x[0]/x[1], [C, z])
C_esp = var(*C_esp.media_ponderada(), r"$C_{Característica}$", "nF/m")
C_esp.show()

R_esp = f_var(lambda x: x[0]/x[1], [R, z])
R_esp = var(*R_esp.media_ponderada(), r"$R_{Característica}$", r"\Omega/m")
R_esp.show()

# Z_G > 2 G\Omega para l = 300 m
# G < 0.5 nano Siemen para l = 300 m
# G < 0.5 / 300    nano Siemen / m

L_esp = f_var(lambda x: 1e15/(x[0]*x[1]**2), [C_esp, v_phi], r"$L_{Caracteristica}$", r"$\mu$H/m") # uH/m
L_esp.show()

M = """0.5	5.6	4.64	528	1
1	5.28	4.48	528	1
1.5	5.44	4.32	524	1
2	5.28	4.16	20	0.8
2.5	5.44	4	120	1
3	5.28	3.92	183	1
3.5	5.36	3.84	228	1
4	5.28	3.68	14.4	0.8
4.5	5.36	3.68	70	0.8
5	5.28	3.52	112	1
5.5	5.36	3.52	152	1
6	5.28	3.44	12	0.8
6.5	5.28	3.36	50	0.8
7	5.2	3.36	82.4	0.8
7.5	5.28	3.28	110	1
8	5.36	3.2	10	0.8
8.5	5.36	3.12	38.4	0.8
9	5.28	3.12	64.8	0.8
9.5	5.28	3.04	88.8	0.8
10	5.2	3.04	7.6	0.8"""

M = text2dataframe(M)
M = M.to_numpy()

f = var(M[:,0], 0.01, "f") # MHz
dt = var(M[:,3], M[:,4]) # ns
Ve = var(M[:,1], 0.1) # V
Vs = var(M[:,2], 0.1) # V

f.redefine(lambda x: x[0]*(10**6)) # Hz
dt.redefine(lambda x: x[0]*1e-9) # s

w = f_var(lambda x: 2*np.pi*x[0], [f], r"$\omega$") # rad/s

# Procesado del intervalo en angulo:
dphi = f_var(lambda x: 2*np.pi*x[0]*x[1], [dt, f], r"$\Delta \phi$")

dphi_value = dphi.value
dphi_err = dphi.err

n = 0
for i in range(len(dphi_value) - 1):
    if dphi_value[i+1] < dphi_value[i]:
        n += 1
    dphi_value[i+1] += 2*np.pi*n
dphi = var(dphi_value, dphi_err)

beta = f_var(lambda x: x[0]/100, [dphi], r"$\beta$", "rad/m")
w.redefine(lambda x: x[0]/1e6, r" $\cdot 10^6$ rad/s")

w.vs(beta)
plt.savefig("./P1/images/w_vs_beta")
plt.close()

# Cálculo de alpha:
import sympy as sp
alpha = f_var(lambda x: (-sp.ln(x[1] / x[0])/100), [Ve, Vs], r"$\alpha$", r"$m^{-1}$")
w.vs(alpha)
plt.savefig("./P1/images/w_vs_alpha")
plt.close()