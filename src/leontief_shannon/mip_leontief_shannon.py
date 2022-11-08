import pandas as pd
import numpy as np
import math
import scipy
from scipy.sparse.linalg import eigs
import requests
import matplotlib.pyplot as plt


import os

# Cambiamos al directorio de descargas
os.chdir("descargas")
# Descargamos las MIP a precios constantes de 2013
url = "https://www.inegi.org.mx/contenidos/investigacion/mcsm/tabulados/"
mi_inegi = ["mip_pcn_ixi_t_{}.xlsx".format(x) for x in range(2003,2019)]

for mip in mi_inegi:
    print("Descargando {}".format(mip))
    r=requests.get(url+mip, allow_redirects=True)
    open(mip,'wb').write(r.content)

# Definimos función que calcula la entropía
def compute_entropy(archivo):
    ## Cargamos la matriz que se encuentra en formato .xlsx
    mip = pd.read_excel(archivo, index_col=None, na_values=['-'],header =0, skiprows=4, nrows=258,usecols = "B:IY")
    ## Convertimos el data frame en la matriz Z
    Z = mip.to_numpy()
    ### Nos quedamos con los sectores "básicos".
    ## Se excluyen a los sectores con filas iguales a cero
    delete_sectors = []

    for i in range(Z.shape[0]):
        suma = sum(Z[i,])
        if suma==0:
            delete_sectors.append(i)

    for i in range(len(delete_sectors)):
        if i ==0:
            Z=np.delete(Z, delete_sectors[i], axis=0)
            Z=np.delete(Z,  delete_sectors[i], axis=1)
        else:
            Z=np.delete(Z, delete_sectors[i]-i, axis=0)
            Z=np.delete(Z,  delete_sectors[i]-i, axis=1)
    ## Construimos la matriz de probabilidades o de transiciones
    P = np.zeros((Z.shape[0],Z.shape[0]))
    suma = 0
    for i in range(Z.shape[0]):
        P[i,] = Z[i,]/sum(Z[i,])

    ##  Calculamos el vector de estacionaridad-probabilidad
    values, vectors = scipy.sparse.linalg.eigs(P, k=1, sigma=1)
    pi_vector = vectors/sum(vectors)
    ## Se calcula la entropía en bits
    H = 0
    for i in range(P.shape[0]):
        for j in range(P.shape[0]):
            if P[i][j]>0:
                H-= pi_vector[i]*P[i][j]*math.log2(P[i][j])
    print("Porcentaje del nivel máximo de entropía {}".format(H[0].real/math.log2(P.shape[0])))
    return H[0].real

### Calculamos la entropía para las MIP de 2003 a 2020
print("%--------------------------------------------------%")
print("               Calculando entropía")
print("%--------------------------------------------------%")

H_mip=[]

for mip in mi_inegi:
    print(mip)
    H_mip.append(compute_entropy(mip))

### Obtenemos el dato del índice de complejidad económica

print("%--------------------------------------------------%")
print("Obtenemos el dato del índice de complejidad económica")
print("%--------------------------------------------------%")

complex_index = pd.read_csv("Country Complexity Rankings 1995 - 2018.csv")
mexico= complex_index[complex_index['Country']=='Mexico']
mexico_eci = np.around(mexico[['ECI {}'.format(anio) for anio in range(2003,2019)] ].to_numpy(),2)[0].tolist()
### Graficamos las series
os.chdir("..")

tiempo_line = [x for x in range(2003,2019)]

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Año')
ax1.set_ylabel('Entropía', color=color)
ax1.plot(tiempo_line, H_mip, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel("Economic Complexity Index (ECI)", color=color)
ax2.plot(tiempo_line, mexico_eci, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()
plt.savefig('entropia_vs_eci.jpg')
plt.show()
