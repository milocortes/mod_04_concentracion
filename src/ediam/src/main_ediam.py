from ediam import ediam, ode_ediam
from optimization_algo import genetico_binario, DE, PSO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# Para hacer el muestreo por Latin Hypecube
from scipy.stats.qmc import LatinHypercube,scale

### Set initial conditions
## Y renewable energy, advanced economies
Yre_N_0 = 25.1
## Y carbon energy, advanced economies
Yce_N_0 = 144.9
## Y renewable energy, emerging economies
Yre_S_0 = 9.0
## Y carbon energy, emerging economies
Yce_S_0 = 105.3
### Environment quality
S_0 = 915.970085

#Initial Productivity conditions are determined by the initial levels of production of energy
ε = 3.5
α = 0.33
size_factor = 1
#In the Northern Region
Ace_N_0 = ((Yce_N_0**((ε-1)/ε)+Yre_N_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yce_N_0/Yre_N_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))
Are_N_0 = ((Yce_N_0**((ε-1)/ε)+Yre_N_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yre_N_0/Yce_N_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))

#In the Southern Region
Ace_S_0 = (1/size_factor)*((Yce_S_0**((ε-1)/ε)+Yre_S_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yce_S_0/Yre_S_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))
Are_S_0 = (1/size_factor)*((Yce_S_0**((ε-1)/ε)+Yre_S_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yre_S_0/Yce_S_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))

U_init = [Ace_N_0, Are_N_0, Ace_S_0, Are_S_0]


## Load observed fossil fuel consumption

fossil_fuel_consumption = pd.read_csv("../datos/fossil_total_ocde_no_ocde.csv")
obs_N_fossil_energy = fossil_fuel_consumption["fossil_total_ocde"][3:].to_numpy()
obs_S_fossil_energy = fossil_fuel_consumption["fossil_total_no_ocde"][3:].to_numpy()


# Loss function 
def loss_f_ediam(X):

    params = X

    dt = 1    # 1 Year
    D = 30 # Simulate for 30 years
    N_t = int(D/dt) # Corresponding no of time steps
    T = dt*N_t    # End time
    U_0 = [Are_N_0, Ace_N_0, Are_S_0,Ace_S_0,S_0]


    N_fossil_energy = []
    S_fossil_energy = []
    N_renewable_energy = []
    S_renewable_energy = []
    Delta_Temp_list = []

    u, t = ode_ediam(ediam, U_init, params, U_0, dt, T, N_fossil_energy, S_fossil_energy, Delta_Temp_list, N_renewable_energy, S_renewable_energy)

    N_fossil_energy = np.array(N_fossil_energy)
    S_fossil_energy = np.array(S_fossil_energy)

    return (np.square(N_fossil_energy - obs_N_fossil_energy)).mean() + (np.square(S_fossil_energy - obs_S_fossil_energy)).mean() 


"""
############
###   PSO
############
"""
# Ejecutamos el algoritmo PSO
# Tamaño de la población
n = 100
# Número de variables
n_var = 10
l_bounds = np.array([0.001]*n_var)
u_bounds = np.array([0.12]*n_var)
maxiter = 100
# Social scaling parameter
α = 0.5
# Cognitive scaling parameter
β = 0.8
# velocity inertia
w = 0.5

fitness_pso, x_best_pso = PSO(loss_f_ediam, n, maxiter, n_var, l_bounds, u_bounds, α, β, w)


"""
############
###   Genético
############
"""
# Ejecutamos el algoritmo genético binario

m = 100
n_variables = 10
i_inf_vec = [0.001]*n_var
i_sup_vec = [0.12]*n_var
precision = 10
maxiter = 100
prob_c = 0.9

fitness_genetico, x_best_genetico = genetico_binario(loss_f_ediam,m,n_variables,i_sup_vec,i_inf_vec,precision,maxiter,prob_c)


"""
############
###   DE
############
"""
# Ejecutamos el algoritmo DE
pop_size = 100   
n_dim = 10               
lb = np.array([0.001]*n_var)
ub = np.array([0.12]*n_var)

maxiter = 100  

pc = 0.9 


fitness_de, x_best_de = DE(loss_f_ediam,pop_size,maxiter,pc,lb,ub,step_size = 0.8)


# Comparamos el fitness de los algoritmos

plt.plot(range(maxiter), fitness_de, label ="DE")
plt.plot(range(maxiter), fitness_pso, label ="PSO")
plt.plot(range(maxiter), fitness_genetico, label ="Genético")

plt.legend()
plt.title("Comparación de algoritmos de optimización")
plt.show()

# Seleccionamos el mejor vector
min_value = 100000
x_best = None
algo_best = None

for algo,x in zip(["Genético","DE","PSO"],[x_best_genetico,x_best_de,x_best_pso]):
    if loss_f_ediam(x) < min_value:
        min_value = loss_f_ediam(x)
        x_best = x
        algo_best = algo
print(f"El valor mínimo de la función es {min_value}\nEl mejor vector fue el del algoritmo {algo_best}\nx_best: {x_best}")

###########
### Test best vector

params = x_best

dt = 1    # 1 Quarterly
D = 30 # Simulate for 30 years
N_t = int(D/dt) # Corresponding no of time steps
T = dt*N_t    # End time
U_0 = [Are_N_0, Ace_N_0, Are_S_0,Ace_S_0,S_0]


N_fossil_energy = []
S_fossil_energy = []
N_renewable_energy = []
S_renewable_energy = []
Delta_Temp_list = []

u, t = ode_ediam(ediam, U_init, params, U_0, dt, T, N_fossil_energy, S_fossil_energy, Delta_Temp_list, N_renewable_energy, S_renewable_energy)


fig = plt.figure()
tiempo_line = [1983 +x for x in t[:-1]]
l1, l2 = plt.plot(tiempo_line, N_fossil_energy, tiempo_line, S_fossil_energy)
l1_obs, l2_obs = plt.plot(tiempo_line, obs_N_fossil_energy,tiempo_line, obs_S_fossil_energy)
fig.legend((l1, l2, l1_obs, l2_obs), ("Advanced Region, Simulation", "Emerging Region, Simulation","OECD, Historic Record", "Non-OECD, Historic Record" ), "center")
plt.title("Fossil Energy Consumption Across Regions Simulated Output vs Historic Record\nSOURCE: U.S. Energy Information Administration (EIA, 2015)")
plt.xlabel("Años")
plt.show()



### Possible futures


### Set initial conditions
## Y renewable energy, advanced economies
Yre_N_0 = N_renewable_energy[-1]
## Y carbon energy, advanced economies
Yce_N_0 = N_fossil_energy[-1]
## Y renewable energy, emerging economies
Yre_S_0 = S_renewable_energy[-1]
## Y carbon energy, emerging economies
Yce_S_0 = S_fossil_energy[-1]
### Environment quality
S_0 = u.T[-1][-1] 

#Initial Productivity conditions are determined by the initial levels of production of energy
ε = 3.5
α = 0.33
size_factor = 1
#In the Northern Region
Ace_N_0 = ((Yce_N_0**((ε-1)/ε)+Yre_N_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yce_N_0/Yre_N_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))
Are_N_0 = ((Yce_N_0**((ε-1)/ε)+Yre_N_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yre_N_0/Yce_N_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))

#In the Southern Region
Ace_S_0 = (1/size_factor)*((Yce_S_0**((ε-1)/ε)+Yre_S_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yce_S_0/Yre_S_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))
Are_S_0 = (1/size_factor)*((Yce_S_0**((ε-1)/ε)+Yre_S_0**((ε-1)/ε))**(ε/(ε-1)))*(1+(Yre_S_0/Yce_S_0)**((1-ε)/ε))**(1/((1-α)*(1-ε)))

U_init = [Ace_N_0, Are_N_0, Ace_S_0, Are_S_0]

# Save calibrated values
N_fossil_energy_calibrated = N_fossil_energy 
S_fossil_energy_calibrated = S_fossil_energy 

# LatinHypercube sampling
n_var = 10
n_sample = 100

engine = LatinHypercube(d = n_var)
sample = engine.random(n = n_sample)

lb = np.array([0.001]*n_var)
ub = np.array([0.12]*n_var)

l_bounds = np.array(lb)
u_bounds = np.array(ub)

sample_scaled = scale(sample,l_bounds, u_bounds)
sample_scaled = scale(sample,l_bounds, u_bounds)


# Run model for each sample

save_runs = {}
for id, sample in enumerate(sample_scaled):
    params = sample

    dt = 1    # 1 Year
    D = 10 # Simulate for 10 years
    N_t = int(D/dt) # Corresponding no of time steps
    T = dt*N_t    # End time
    U_0 = [Are_N_0, Ace_N_0, Are_S_0,Ace_S_0,S_0]


    N_fossil_energy = N_fossil_energy_calibrated.copy()
    S_fossil_energy = S_fossil_energy_calibrated.copy()
    N_renewable_energy = []
    S_renewable_energy = []
    Delta_Temp_list = []

    u, t = ode_ediam(ediam, U_init, params, U_0, dt, T, N_fossil_energy, S_fossil_energy, Delta_Temp_list, N_renewable_energy, S_renewable_energy)

    save_runs[id] = S_fossil_energy


for k, v in save_runs.items():
    plt.plot(range(1983,2023), v)

plt.plot(range(1983,2013), obs_S_fossil_energy, label = "Non-OECD, Historic Record", color = "red")
plt.legend()
plt.title("Possible future scenarios Fossil Energy Consumption in Non-OECD economies")
plt.show()