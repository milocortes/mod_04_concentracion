import matplotlib.pyplot as plt
import random
import math 

max_val, min_val = 1, -1
range_size = (max_val - min_val)  

secuencia_puntos = [(random.random() * range_size + min_val, random.random() * range_size + min_val) for i in range(200)]

for i in range(len(secuencia_puntos)):
    print(i)
    figure, axes = plt.subplots()
    Drawing_colored_circle = plt.Circle(( 0 , 0 ), 1 ,fill=False)
    
    axes.set_aspect( 1 )
    axes.add_artist( Drawing_colored_circle )
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])

    for punto in secuencia_puntos[:1+i]:

        axes.scatter(*punto, color = "red")

    plt.title( f'Muestras : {i+1}' )
    #plt.show()
    plt.savefig(f"pi_mc/pi_mc_{i}.png")
    plt.clf()