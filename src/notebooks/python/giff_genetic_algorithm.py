from math import log2, ceil
import random
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import ticker, cm


def length_variable(l_sup: int, l_inf: int , precision: int):
    return ceil(log2((l_sup - l_inf)*10**precision))

# Función que obtiene las potencias base 2 de un vector de bits (un individuo)
def to_decimal(dimension,individuo):
    return sum([2**(i) for i in range(dimension-1,-1,-1) ]* np.array(individuo))

# Función que decodifica el vector a un valor real
def binary2real(i_sup, i_inf, dimension, individuo):
    return i_inf+ (to_decimal(dimension, individuo)* ((i_sup-i_inf)/(2**len(individuo)-1)))


# Función a minimizar
def f_himmelblau(X):
  x,y = X
  return (x**2 + y -11)**2 + (x + y**2 -7)**2

class Individuo:
    def __init__(self, f, upper_bound, lower_bound, n_vars, precision, genotipo = []):
        self.f = f
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.n_vars = n_vars
        self.precision = precision
        self.genotipo = genotipo
        self.fenotipo = []
        self.objv = None
        self.aptitud = None
        self.L_genotipo = None

    def construye_genotipo(self):
        acumula_gen = []
        
        for i in range(self.n_vars):
            L_var = length_variable(self.upper_bound[i], self.lower_bound[i], self.precision)
            acumula_gen += [random.randint(0,1)  for j in range(L_var)]

        self.genotipo = acumula_gen

    def decode(self):
        L_total_vars = 0
        for i in range(self.n_vars):
            L_var = length_variable(self.upper_bound[i], self.lower_bound[i], self.precision)

            self.fenotipo.append(
                binary2real(self.upper_bound[i], self.lower_bound[i], L_var, self.genotipo[L_total_vars: L_total_vars + L_var])
            )
            
            L_total_vars += L_var            

        self.L_genotipo = L_total_vars

    def evalua_funcion(self):
        self.objv = self.f(self.fenotipo)

    def calcula_aptitud(self, max_val, min_val, new_max, new_min):
        # scaled_fitness
        y = np.array([new_min, new_max])
        X = np.matrix([[min_val, 1],[max_val, 1]])

        try:
            a,b = np.ravel(X.I @ y)
        except:
            a,b = np.ravel(np.linalg.pinv(X) @ y)
        self.aptitud = a*self.objv + b 
    
    def cruza(self, individuo_cruza):
        
        # Implementación de cruza en un punto
        # Escogemos de forma aleatoria el punto de cruza
        punto_cruza = np.random.choice([i for i in range(self.L_genotipo)])

        return self.genotipo[:punto_cruza] + individuo_cruza.genotipo[punto_cruza:]
    
    def mutacion(self, proba_mutacion):
        
        self.L_genotipo = len(self.genotipo)

        aleatorio = random.random()
        
        if aleatorio < proba_mutacion:
            id_swap_gen = np.random.choice([i for i in range(self.L_genotipo)])
            self.genotipo[id_swap_gen] = int(not self.genotipo[id_swap_gen])



def SELECCION(scaled_objv, N):
    ### Calculamos la probabilidad de selección con el valor de aptitud
    suma = sum(scaled_objv)
    proba_seleccion = [i/suma  for i in scaled_objv]

    ### Obtenemos N parejas para generar la nueva población
    ordena_proba_seleccion = sorted(enumerate(proba_seleccion),key = lambda tup: tup[1], reverse=True)

    suma_acumulada = np.cumsum([v for (k,v) in ordena_proba_seleccion])

    parejas_cruza = []

    for i in range(N):
        pareja = []

        for p in range(2):
            aleatorio = random.random()
            pareja_id = np.argwhere(suma_acumulada >= aleatorio).ravel()[0]
            pareja.append(ordena_proba_seleccion[pareja_id][0])
        
        parejas_cruza.append(pareja)
    
    return parejas_cruza


# Generamos valores para Y y X.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = (X**2 + Y -11)**2 + (X + Y**2 -7)**2

"""
fig,ax=plt.subplots(1,1)
cp = ax.contourf(X, Y, Z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
fig.colorbar(cp)
ax.set_title('Filled Contours Plot')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

"""

"""

REINICIAMOS LA EJECUCIÓN DEL ALGORITMO

"""
## Definimos los parámetros del algoritmo genético
N = 1000
n_variables = 2
l_sup_vec = [5, 5]
l_inf_vec = [-5, -5]
precision = 20
generaciones = 200

mejor_individuo = 0
mejor_valor = 100000000000000
fitness_values = []

#### Inicializamos la población
poblacion = [ Individuo(f_himmelblau, l_sup_vec, l_inf_vec, n_variables, precision) for i in range(N)]

#### Iniciamos el ciclo evolutivo
print("Evaluación de la población inicial")

objv = []

#### Generamos la población inicial
for individuo in poblacion:
    # Contruimos el genotipo del individuo
    individuo.construye_genotipo()
    # Decodificamos el genotipo del individuo al dominio del problema (i.e, obtenemos el fenotipo)
    individuo.decode()
    # Evaluamos el fenotipo 
    individuo.evalua_funcion()
    # Guardamos el valor de la función
    objv.append(individuo.objv)

fenotipo_poblacion = np.array([individuo.fenotipo for individuo in poblacion])

### Generamos un giff de las figuras de la matriz en las distintas iteraciones
fig,ax=plt.subplots(1,1)
cp = ax.contourf(X, Y, Z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
fig.colorbar(cp)
ax.set_title('Filled Contours Plot')
ax.set_xlabel('x')
ax.set_ylabel('y')

ims = []

im = ax.scatter(fenotipo_poblacion.T[0], fenotipo_poblacion.T[1],color='red',s = 10)

ims.append([im])



for it in range(generaciones):
    print("-----------------------------")
    print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
    print("        Generación {}".format(it))
    print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
    print("-----------------------------")

    ### APTITUD de la población
    #### Obtenemos la aptitud de cada individuo
    min_val, max_val = min(objv), max(objv)

    scaled_objv = []

    for individuo in poblacion:
        individuo.calcula_aptitud(max_val, min_val, 0, 100)
        scaled_objv.append(individuo.aptitud) 
    
    ### SELECCIÓN de los individuos que contribuirán a crea la nueva generación
    parejas_cruza = SELECCION(scaled_objv, N)

    ### Construimos la nueva población con la operación genética de CRUZA
    ##### CRUZA
    nueva_poblacion = []

    for pareja in parejas_cruza:
        
        id_ind_uno, id_ind_dos = pareja
        
        genotipo_cruza = poblacion[id_ind_uno].cruza(poblacion[id_ind_dos])

        nueva_poblacion.append(
            Individuo(f_himmelblau, l_sup_vec, l_inf_vec, n_variables, precision, genotipo = genotipo_cruza)
        )

    ##### MUTACIÓN de la población
    for individuo in nueva_poblacion:
        individuo.mutacion(0.00005)
    
    ##### Actualizamos la nueva población
    poblacion = nueva_poblacion

    #### Evaluamos la nueva población
    objv = [] 
    for individuo in poblacion:
        # Decodificamos el genotipo del individuo al dominio del problema (i.e, obtenemos el fenotipo)
        individuo.decode()
        # Evaluamos el fenotipo 
        individuo.evalua_funcion()
        # Guardamos el valor de la función
        objv.append(individuo.objv)

    #### Identificamos al mejor individuo de la población
    mejor_individuo = objv.index(min(objv))

    #### Actualizamos el mejor valor encontrado
    if objv[mejor_individuo] < mejor_valor:
        mejor_valor = objv[mejor_individuo] 
        mejor_vector = poblacion[mejor_individuo].fenotipo
    
    fitness_values.append(mejor_valor)

    fenotipo_poblacion = np.array([individuo.fenotipo for individuo in poblacion])
    im = ax.scatter(fenotipo_poblacion.T[0], fenotipo_poblacion.T[1],color='red',s = 10)
    
    ims.append([im])

import matplotlib.animation as animation

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
writer = animation.PillowWriter(fps=6)

ani.save("demo_himmelblau.gif", writer=writer)


print(f"Mejor valor {mejor_valor}")
print(f"Mejor vector {mejor_vector}")
