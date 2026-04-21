import numpy as np
from data_management import *
from var import *

R0 = var(50, 2.5)
v_phi = var(2e8, 1e7)

M = """100	9.88	0.01
200	19.76	0.01
300	29.9	0.1"""

M = text2dataframe(M)
M = M.to_numpy()

l = var(M[:,0], 0.01)
C = var(M[:,1], M[:,2])

# Z_G > 2 G\Omega para l = 300 m
# Z_G * l > 

M = """0.5	5.6	4.64	528	1	1.658760921	1.658760921
1	5.28	4.48	528	1	3.317521842	3.317521842
1.5	5.44	4.32	524	1	4.938583651	4.938583651
2	5.28	4.16	20	0.8	0.2513274123	6.534512719
2.5	5.44	4	120	1	1.884955592	8.168140899
3	5.28	3.92	183	1	3.449468734	9.732654041
3.5	5.36	3.84	228	1	5.013981875	11.29716718
4	5.28	3.68	14.4	0.8	0.3619114737	12.92828209
4.5	5.36	3.68	70	0.8	1.979203372	14.54557399
5	5.28	3.52	112	1	3.518583772	16.08495439
5.5	5.36	3.52	152	1	5.252742917	17.81911353
6	5.28	3.44	12	0.8	0.4523893421	19.30194526
6.5	5.28	3.36	50	0.8	2.042035225	20.89159115
7	5.2	3.36	82.4	0.8	3.624141285	22.47369721
7.5	5.28	3.28	110	1	5.183627878	24.0331838
8	5.36	3.2	10	0.8	0.5026548246	25.63539605
8.5	5.36	3.12	38.4	0.8	2.050831684	27.18357291
9	5.28	3.12	64.8	0.8	3.664353671	28.7970949
9.5	5.28	3.04	88.8	0.8	5.300495125	30.43323635
10	5.2	3.04	7.6	0.8	0.4775220833	31.89344862"""

M = text2dataframe(M)
M = M.to_numpy()

f = var(M[:,0], 0.01, "f") # MHz
dt = var(M[:,3], M[:,4]) # ns

f.show()

f.redefine(lambda x: x[0]*(10**6)) # Hz
f.show()
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
