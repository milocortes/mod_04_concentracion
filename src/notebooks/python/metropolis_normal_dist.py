import numpy as np 
import matplotlib.pyplot as plt
from decimal import Decimal


niter = 100000

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
plt.show() 

import glob

image_files = glob.glob("metropolis_normal_k/*") 
image_files = [( i,int(i.split("_")[-1].split(".png")[0])) for i in image_files] 

image_files = [i[0] for i in sorted(image_files,key = lambda tup: tup[1], reverse=False)]

from PIL import Image


frames = [Image.open(image) for image in image_files[:-50]]
frame_one = frames[0]
frame_one.save("metropolis_normal_dist.gif", format="GIF", append_images=frames,
            save_all=True, duration=30, loop=0)