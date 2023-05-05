import numpy as np 
import matplotlib.pyplot as plt
from decimal import Decimal
from tqdm import tqdm 

for niter in tqdm(range(1000, 1000000+1, 1000)):
    x = 0
    naccept = 0

    guarda_x = []

    for it in range(niter):
        backup = x
        action_init = (1/2)*x**2

        dx = np.random.random()
        dx = (dx-0.5)*2.0

        x = x + dx

        action_final =  (1/2)*x**2

        ### Metropolis tes
        r = np.random.random()

        if np.exp(action_init - action_final) > r:
            ## Aceptamos el candidato
            naccept += 1
        else:
            ## Rechazamos el candidato
            x = backup

        
        guarda_x.append(x)

    plt.hist(guarda_x, bins = 400)
    plt.xlim([-4, 4])
    plt.suptitle(r"Histograma para $x^{(1)}, x^{(2)}, \dots , x^{(k)}$" )
    plt.title(r"$K$ = " + '%.2E' % Decimal(str(niter)))
    #plt.show()
    plt.savefig(f"metropolis_normal_k/metropolis_normal_{niter}.png") 
    plt.clf()