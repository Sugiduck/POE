
def text2mat (M:str):
    M = M.replace("\t", " ")
    M = M.replace("−", "-")

    lines = M.split("\n")
    values = [line.split(" ") for line in lines]

    for i in range(len(values)):
        for j in range(len(values[i])):
            if values[i][j] == "":
                values[i][j] = "nan"
            try:
                values[i][j] = float(values[i][j])
            except:
                print(f"No se pudo convertir a float: {values[i][j]}")
                values[i][j] = values[i][j]

    return values

def text2dataframe (M:str):
    import pandas as pd
    return pd.DataFrame(text2mat(M))

# Otras maneras que probablemente sean mejores son:
# data = pd.read_csv(filepath, delimiter = r"\s+")
# data = np.loadtxt("data/massnubasestbldata.dat")

def round_err (x,e):
    import numpy as np
    n = -np.floor(np.log10(e)) + 1

    x = x*10**(n)
    e = e*10**(n)
    x = round(x)
    x = x*10**(-n)
    e = np.ceil(e)
    e = e*10**(-n)

    return x,e