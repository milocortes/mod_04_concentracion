import random
import numpy as np

# Para hacer el muestreo por Latin Hypecube
from scipy.stats.qmc import LatinHypercube,scale
import math

# Genera población aleatoria binaria de m bit-string y cromosomas de tamaño n
def rand_population_binary(m,n):
    return [[random.randint(0, 1) for j in range(n)]for i in range(m)]

# Función que codifica las variables
def length_variable(i_sup,i_inf,precision):
    return int(math.ceil(math.log2((i_sup-i_inf)*10**(precision))))

# Función que obtiene las potencias en base dos de un vector de bits
def to_decimal(dimension,v):
    v.reverse()
    return sum(np.array([2**(i) for i in range(dimension)])*np.array(v))

# Función que codifica el vector de bits a un valor real
def binary2real(i_sup,i_inf,dimension,pob):
     return [i_inf + (to_decimal(dimension,v)*(i_sup-i_inf)/(2**(dimension)-1)) for v in pob]

# Función que genera la estructura de datos Fenotipo
def DECODE(n_variables,m,i_sup_vec,i_inf_vec,dimension_vec,pob_vec):

    feno = [[] for i in range(m)]

    for i in range(n_variables):
        i_sup = i_sup_vec[i]
        i_inf = i_inf_vec[i]
        pob = pob_vec[i]
        dim = dimension_vec[i]
        b2r = binary2real(i_sup,i_inf,dim,pob)
        for k in range(m):
            feno[k].append(b2r[k])

    return feno

# Funcion que genera la estructura de datos de la función objetivo
def OBJFUN(f,feno):
    return [f(i) for i in feno]


# Función que genera la aptitud de los individuos
def APTITUD(objv,operacion):

    val_max = max(objv)
    val_min = min(objv)

    if operacion == "min":
        objv_norm = [(((i-val_min)/(val_max-val_min))+0.01)**-1 for i in objv]
        suma = sum(objv_norm)
        key_objv = [(k,i/suma) for (k,i) in enumerate(objv_norm)]
        objv_sort = sorted(key_objv,key=lambda tup: tup[1],reverse=True)

    elif operacion == "max":
        objv_norm = [(((i-val_min)/(val_max-val_min))+0.1) for i in objv]
        suma = sum(objv_norm)
        key_objv = [(k,i/suma) for (k,i) in enumerate(objv_norm)]
        objv_sort = sorted(key_objv,key=lambda tup: tup[1],reverse=True)

    return objv_sort

# Función que selecciona a los mejores individuos
def SELECCION(aptitud,tipo,n_variables,población):
    if tipo == "ruleta":
        n = int(len(aptitud)/2)
        suma_acumulada = np.cumsum([v for (k,v) in aptitud])

        individuos_dict = {i:{} for i in range(n)}

        for pareja in range(n):
            for individuo in range(2):
                aleatorio = random.random()
                index_ind = np.where(suma_acumulada >= aleatorio)[0][0]
                cromosoma = []
                for gen in range(n_variables):
                    cromosoma.append(población[gen][aptitud[index_ind][0]])

                cromosoma = sum(cromosoma,[])
                individuos_dict[pareja][individuo] = cromosoma

    return individuos_dict

def CRUZA(seleccion,tipo,length_total_cromosoma,prob_c):
    if tipo == "unpunto":
        n = len(seleccion)

        nueva_poblacion = []

        for pareja in range(n):
            
            aleatorio_pc = random.random()
            
            if aleatorio_pc < prob_c:
                punto_cruza = random.randint(0, length_total_cromosoma)

                primer_nuevo_individuo = seleccion[pareja][0][0:punto_cruza] + seleccion[pareja][1][punto_cruza:length_total_cromosoma]
                segundo_nuevo_individuo = seleccion[pareja][1][0:punto_cruza] + seleccion[pareja][0][punto_cruza:length_total_cromosoma]

                nueva_poblacion.append(primer_nuevo_individuo)
                nueva_poblacion.append(segundo_nuevo_individuo)
            else:
                nueva_poblacion.append(seleccion[pareja][0])
                nueva_poblacion.append(seleccion[pareja][1])

    return nueva_poblacion

def MUTACION(nueva_poblacion,length_total_cromosoma,n_variables,dimension_vec):

    mutacion_param = 2/length_total_cromosoma
    n = len(nueva_poblacion)

    for individuo in range(n):
         muta_random = np.array([random.random() for i in range(length_total_cromosoma)])
         muta_index = np.where(muta_random < mutacion_param)[0]

         for i in muta_index:
             nueva_poblacion[individuo][i] = int(not nueva_poblacion[individuo][i])

    inicio = 0
    fin = 0
    nueva_poblacion_format = []

    for gen in range(n_variables):
        nueva_poblacion_gen = []
        fin += dimension_vec[gen]
        for individuo in nueva_poblacion:
            nueva_poblacion_gen.append(individuo[inicio:fin])

        nueva_poblacion_format.append(nueva_poblacion_gen)
        inicio +=dimension_vec[gen]

    return nueva_poblacion_format


def genetico_binario(f, m, n_variables, i_sup_vec, i_inf_vec, precision, maxiter, prob_cruza):
    '''
    ------------------------------------------
                        
            Genetic Binary Algorithm 
    -------------------------------------------
    # Inputs:
        * f             - function to be minimized
        * m             - number of individuals in the population
        * n_variables
        * maxiter        - maximum number of optimization iterations
        * prob_cruza     - crossover probability
        * i_inf_vec
        * i_sup_vec
        * precision
        
    # Output
        * fitness_values - history of best fitness values 
        * best_vector    - best solution found
    '''
    dimension_vec = []
    genotipo = []
    length_total_cromosoma = 0

    ## Generamos población inicial
    for i in range(n_variables):
        length_cromosoma = length_variable(i_sup_vec[i],i_inf_vec[i],precision)
        length_total_cromosoma += length_cromosoma
        dimension_vec.append(length_cromosoma)
        genotipo.append(rand_population_binary(m, length_cromosoma))

    ## Iniciamos el algoritmo genético
    feno = DECODE(n_variables,m,i_sup_vec,i_inf_vec,dimension_vec,genotipo)
    print("Evaluando poblacion inicial")
    objv = OBJFUN(f,feno)

    resultados = []
    mejor_individuo = 0
    mejor_valor = min(objv)

    fitness_values = []

    for it in range(maxiter):
        print("-----------------------------")
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("        Iteración {}".format(it))
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("-----------------------------")

        aptitud = APTITUD(objv,"min")
        seleccion = SELECCION(aptitud, "ruleta", n_variables, genotipo)
        genotipo = CRUZA(seleccion, "unpunto", length_total_cromosoma, prob_cruza)
        genotipo = MUTACION(genotipo, length_total_cromosoma, n_variables, dimension_vec)
        feno = DECODE(n_variables, m, i_sup_vec, i_inf_vec, dimension_vec, genotipo)
        objv = OBJFUN(f,feno)
        resultados.append(min(objv))
        mejor_individuo = objv.index(min(objv))
        #print("Mejor valor fun.obj ---> {}. Variables de decision ---> {}".format(objv[mejor_individuo],feno[mejor_individuo]))
        #print("Mejor valor fun.obj ---> {}".format(objv[mejor_individuo]))
        if objv[mejor_individuo] < mejor_valor:
            mejor_valor = objv[mejor_individuo]
            mejor_vector = feno[mejor_individuo]
        fitness_values.append(mejor_valor)
    best_vector = mejor_vector

    return fitness_values, best_vector





def DE(f_cost,pop_size,max_iters,pc,lb,ub,step_size = 0.4, theta_0 = None):
    '''
    ------------------------------------------
                        DE
    Classic Differential Evolution
    -------------------------------------------
    ## Implemented as a minimization algorithm
    # Inputs:
        * f_cost        - function to be minimized
        * pop_size      - number of individuals in the population
        * max_iters     - maximum number of optimization iterations
        * pc            - crossover probability
        * lb
        * ub
        * step_size
        * theta_0
    # Output
        * best_theta    - best solution found
        * best_score    - history of best score
    '''
    # problem dimension
    n_dim = np.shape(lb)[0]
    # randomly initialize the population
    pop_chrom = (ub - lb) * np.random.random_sample(size = (pop_size,n_dim)) + lb

    if theta_0 is not None:
        pop_chrom[0] = theta_0
    # obtain the cost of each solution
    pop_cost = np.zeros(pop_size)

    for id_p in range(pop_size):
        pop_cost[id_p] = f_cost(pop_chrom[id_p])

    # optimization
    for id_iter in range(max_iters):
        print("-----------------------------")
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("        Iteración {}".format(id_iter))
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("-----------------------------")

        for id_pop in range(pop_size):
            # pick candidate solution
            xi = pop_chrom[id_pop]
            # ids_cs vector containing the indexes of
            # the all other candidate solution but xi
            ids_cs = np.linspace(0, pop_size - 1, pop_size, dtype = int)
            # remove id_pop from ids_cs
            ids_cs = np.where(ids_cs != id_pop)
            # convert tuple to ndarray
            ids_cs = np.asarray(ids_cs)[0]
            # randomly pick 3 candidate solution using indexes ids_cs
            xa , xb , xc = pop_chrom[np.random.choice(ids_cs, 3, replace = False)]
            V1 = xa
            V2 = xb
            Vb = xc
            # create the difference vector
            Vd = V1 - V2
            # create the mutant vector
            Vm = Vb + step_size*Vd
            # make sure the mutant vector is in [lb,ub]
            Vm = np.clip(Vm,lb,ub)
            # create a trial vector by recombination
            Vt = np.zeros(n_dim)
            jr = np.random.rand()   # index of the dimension
                                    # that will under crossover
                                    # regardless of pc
            for id_dim in range(n_dim):
                rc = np.random.rand()
                if rc < pc or id_dim == jr:
                    # perform recombination
                    Vt[id_dim] = Vm[id_dim]
                else:
                    # copy from Vb
                    Vt[id_dim] = xi[id_dim]
            # obtain the cost of the trial vector
            vt_cost = f_cost(Vt)
            # select the id_pop individual for the next generation
            if vt_cost < pop_cost[id_pop]:
                pop_chrom[id_pop] = Vt
                pop_cost[id_pop] = vt_cost
        # store minimum cost and best solution
        ind_best = np.argmin(pop_cost)
        if id_iter == 0:
            minCost = [pop_cost[ind_best]]
            bestSol = [pop_chrom[ind_best]]
        else:
            minCost = np.vstack((minCost,pop_cost[ind_best]))
            bestSol = np.vstack((bestSol,pop_chrom[ind_best]))

    # return values
    ind_best_cost = np.argmin(minCost)
    best_theta = bestSol[ind_best_cost]
    best_score = minCost

    return best_score.flatten() ,best_theta.flatten()


# Definimos la clase Particle
class Particle:
    def __init__(self,x,v):
        self.x = x
        self.v = v
        self.x_best = x
        
def PSO(f, pop_size, maxiter, n_var, lb, ub, α, β, w):
    '''
    ------------------------------------------
                        PSO
    Particle Swarm Optimization
    -------------------------------------------
    ## Implemented as a minimization algorithm
    # Inputs:
        * f             - function to be minimized
        * pop_size      - number of individuals in the population
        * max_iter     - maximum number of optimization iterations
        * n_var
        * lb
        * ub
        * α             - Social scaling parameter
        * β             - Cognitive scaling parameter
        * w             - velocity inertia
        
    # Output
        * x_best        - best solution found
        * fitness_values - history of best score
    '''   
    # LatinHypercube sampling
    engine = LatinHypercube(d=n_var)
    sample = engine.random(n=pop_size)

    l_bounds = np.array(lb)
    u_bounds = np.array(ub)

    sample_scaled = scale(sample,l_bounds, u_bounds)
    sample_scaled = scale(sample,l_bounds, u_bounds)

    # define particle population
    pob = [Particle(x,np.array([0]*n_var)) for x in sample_scaled]


    
    x_best = pob[0].x_best
    y_best = f(x_best)

    
    # minimum value for the velocity inertia
    w_min = 0.4
    # maximum value for the velocity inertia
    w_max = 0.9

    # Velocidad máxima
    vMax = np.multiply(u_bounds-l_bounds,0.2)
    # Velocidad mínima
    vMin = -vMax

    
    for P in pob:
        y = f(P.x)
        if y < y_best:
            x_best = P.x_best
            y_best = y

    fitness_values = []

    for k in range(maxiter):
        
        print("-----------------------------")
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("        Iteración {}".format(k))
        print("-%%%%%%%%%%%%%%%%%%%%%%%%%%%-")
        print("-----------------------------")
        
        for P in pob:
            # Actualiza velocidad de la partícula
            ϵ1,ϵ2 = np.random.uniform(), np.random.uniform()
            P.v = w*P.v + α*ϵ1*(P.x_best - P.x) + β*ϵ2*(x_best - P.x)

            # Ajusta velocidad de la partícula
            index_vMax = np.where(P.v > vMax)
            index_vMin = np.where(P.v < vMin)

            if np.array(index_vMax).size > 0:
                P.v[index_vMax] = vMax[index_vMax]
            if np.array(index_vMin).size > 0:
                P.v[index_vMin] = vMin[index_vMin]

            # Actualiza posición de la partícula
            P.x += P.v

            # Ajusta posición de la particula
            index_pMax = np.where(P.x > u_bounds)
            index_pMin = np.where(P.x < l_bounds)

            if np.array(index_pMax).size > 0:
                P.x[index_pMax] = u_bounds[index_pMax]
            if np.array(index_pMin).size > 0:
                P.x[index_pMin] = l_bounds[index_pMin]

            # Evaluamos la función
            y = f(P.x)

            if y < y_best:
                x_best = np.copy(P.x_best)
                y_best = y
            if y < f(P.x_best):
                P.x_best = np.copy(P.x)
            

            # Actualizamos w

            w = w_max - k * ((w_max-w_min)/maxiter)

        fitness_values.append(y_best)

    return fitness_values ,x_best