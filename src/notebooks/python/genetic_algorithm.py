from math import log2, ceil
import random
import numpy as np
import pandas as pd

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
        
        proba_mutacion = 0.1 * (1/self.L_genotipo)
        if aleatorio < proba_mutacion:
            id_swap_gen = np.random.choice([i for i in range(self.L_genotipo)])
            self.genotipo[id_swap_gen] = int(not self.genotipo[id_swap_gen])





## Definimos los parámetros del algoritmo genético
N = 100
n_variables = 2
l_sup_vec = [5, 5]
l_inf_vec = [-5, -5]
precision = 10
generaciones = 100

mejor_individuo = 0
mejor_valor = 100000000000000
fitness_values = []

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

##### APTITUD
#### Obtenemos la aptitud de cada individuo
min_val, max_val = min(objv), max(objv)

scaled_objv = []

for individuo in poblacion:
    individuo.calcula_aptitud(max_val, min_val, 1, 100)
    scaled_objv.append(individuo.aptitud)

##### SELECCIÓN
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

##### CRUZA
nueva_poblacion = []

for pareja in parejas_cruza:
    
    id_ind_uno, id_ind_dos = pareja
    
    genotipo_cruza = poblacion[id_ind_uno].cruza(poblacion[id_ind_dos])

    nueva_poblacion.append(
        Individuo(f_himmelblau, l_sup_vec, l_inf_vec, n_variables, precision, genotipo = genotipo_cruza)
    )

##### MUTACIÓN

for individuo in nueva_poblacion:
    individuo.mutacion(0.05)



#### Evaluamos la nueva población
objv_nueva = [] 
for individuo in nueva_poblacion:
    # Decodificamos el genotipo del individuo al dominio del problema (i.e, obtenemos el fenotipo)
    individuo.decode()
    # Evaluamos el fenotipo 
    individuo.evalua_funcion()
    # Guardamos el valor de la función
    objv_nueva.append(individuo.objv)

#### ESTO ES SÓLO PARA UNA GENERACIÓN ... 
#### Necesitamos iterar para más generaciones
#### Para ello, modifiquemos nuestro programa creando la función:
####    * SELECCION

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


"""

REINICIAMOS LA EJECUCIÓN DEL ALGORITMO

"""
from math import e,pi

def ackley(X):
    return -20*e**(-0.2*(0.5*(X[0]**2+X[1]**2))**(1/2) ) -e**(0.5*(np.cos(2*pi*X[0])+np.cos(2*pi*X[1])))+e+20

def eggholder(X):
    x,y = X
    return -(y+47) * np.sin(np.sqrt(abs( (x/2) + (y+47) ))) - x*np.sin( np.sqrt( abs(x - (y+47))))

## Definimos los parámetros del algoritmo genético
N = 1000
n_variables = 2
l_sup_vec = [5, 5]
l_inf_vec = [-5, -5]
precision = 10
generaciones = 200

mejor_individuo = 0
mejor_valor = 100000000000000
fitness_values = []

#### Inicializamos la población
poblacion = [ Individuo(ackley, l_sup_vec, l_inf_vec, n_variables, precision) for i in range(N)]

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
            Individuo(ackley, l_sup_vec, l_inf_vec, n_variables, precision, genotipo = genotipo_cruza)
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

import matplotlib.pyplot as plt
plt.plot(fitness_values)
plt.title("Fitness")
plt.ylabel("$f(X)$")
plt.legend()
plt.show()
print(f"Mejor valor {mejor_valor}")
print(f"Mejor vector {mejor_vector}")