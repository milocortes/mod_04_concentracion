import numpy as np
import matplotlib.pyplot as plt

L = 100
Nv = L * L

Coordinates = [[x,y] for y in range(L) for x in range(L)]

Neighbors = [[((x+1)%L,y),
              ((x-1)%L,y),
              (x,(y+1)%L),
              (x,(y-1)%L)]
             for x,y in Coordinates]

State = np.zeros([L,L])

for y in range(L):
    for x in range(L):
        State[x][y] = np.random.choice([1,-1], p = [0.5,0.5])

plt.imshow(State,cmap())
plt.axis("off")
plt.show()

import time

start = time.time()

State = np.zeros([L,L])
for y in range(L):
    for x in range(L):
        State[x][y] = np.random.choice([1,-1], p = [0.5,0.5])

T = 2
n_flips = Nv*10
Mlist = []
Time = []

for t in range(n_flips):

      expval = np.exp(-deltaE/T)
        State[xk][yk] = State[xk][yk]*np.random.choice([-1,1], p = [expval, 1-expval])
    else:
        State[xk][yk] = -State[xk][yk]

    Mlist.append(np.sum(State.flatten())/Nv)
    #if (t/Nv) in [0, 1, 2, 4, 6, 10, 20, 40, 100]:
    if (t%Nv)==0:
        print(t)

        plt.title(r'$t=' +str(t/Nv)+'$ laticce units')
        plt.imshow(State)
        plt.axis("off")
        plt.show()        

end = time.time()
print(end - start)k = np.random.choice(list(range(Nv)))
    xk, yk =  Coordinates[k]

    deltaE = 0

    for j in range(len(Neighbors[k])):
        x,y = Neighbors[k][j]
        deltaE += 2*State[xk][yk]*State[x][y]

    if deltaE > 0:
        expval = np.exp(-deltaE/T)
        State[xk][yk] = State[xk][yk]*np.random.choice([-1,1], p = [expval, 1-expval])
    else:
        State[xk][yk] = -State[xk][yk]

    Mlist.append(np.sum(State.flatten())/Nv)
    #if (t/Nv) in [0, 1, 2, 4, 6, 10, 20, 40, 100]:
    if (t%Nv)==0:
        print(t)

        plt.title(r'$t=' +str(t/Nv)+'$ laticce units')
        plt.imshow(State)
        plt.axis("off")
        plt.show()        

end = time.time()
print(end - start)

# Graficamos la magnetización
plt.plot(Mlist)
plt.xlabel(r"t")
plt.ylabel(r"m(t)")


## Python es muy lento ... usemos C++
State_cpp = np.loadtxt("../datos/State.dat")
plt.imshow(State_cpp)

magne = np.loadtxt("../datos/Magnetization.dat")
plt.plot(magne.T[0],abs(magne.T[1]))
plt.xlabel(r"t (lattice units)")
plt.ylabel(r"m(t)")

Data = np.loadtxt("../datos/Results_Ensemble.dat")
Temperature = np.unique(Data.T[0])
Average_m_spin = []

for t in Temperature:
    Average_m_spin.append(np.mean(abs(Data.T[1][Data.T[0]==t])))
    
plt.plot(Temperature, Average_m_spin, "*")
plt.xlabel(r"$T$", size=20)
plt.ylabel(r"$<m>$", size = 20)