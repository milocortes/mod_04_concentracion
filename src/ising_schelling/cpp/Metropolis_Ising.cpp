#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>
#include <random>

using namespace std;

#define L 100

int RandomChoice(vector<double> Freqs, mt19937 &gen){
  discrete_distribution<> d(Freqs.begin(),Freqs.end());
  return d(gen);
}

double Magnetization_spin(int State[L][L]){
    int m_spin = 0; 
    for(int y=0;y<L;y++){
       for(int x=0; x<L;x++){
	  m_spin+=State[x][y];
        }
    }

    return 1.0*m_spin/(1.0*L*L);
}

double Energy_spin(int State[L][L], vector<vector<vector<int>>> Neighbors){
    int energy = 0;
    int count = 0;
     
    for(int y=0;y<L;y++){
       for(int x=0; x<L;x++){
	  for(int j=0; j<Neighbors[count].size(); j++){
             energy += -State[x][y] * State[Neighbors[count][j][0]][Neighbors[count][j][1]];
	  }
          count += 1;  
          }
        }
	    return 1.0*energy/(2.0*L*L);
}

void Flips(double T, int delta_t, int State[L][L], vector<vector<int>> Coordinates, vector<vector<vector<int>>> Neighbors,
           uniform_int_distribution<> &s_choice,  mt19937 &gen){

  for(int t=0; t<delta_t ;  t++){
  int k = s_choice(gen);
  int DeltaE = 0;
  int xk = Coordinates[k][0];
  int yk = Coordinates[k][1];

  for(int i = 0; i < Neighbors[k].size(); i++){
	DeltaE += 2*State[xk][yk] * State[Neighbors[k][i][0]][Neighbors[k][i][1]];
  }

 // cout << DeltaE << endl;
  if(DeltaE>0){
    double expval = exp(-DeltaE/T);
    State[xk][yk] = (2*RandomChoice({expval, 1-expval}, gen)-1)*State[xk][yk];
  }
  else{
   State[xk][yk] = -State[xk][yk];
  }
  }
}


int main(){
  random_device rd;
  mt19937 gen(rd());
  
  int Nv = L*L;
 
  int T = 2;
  uniform_int_distribution<> s_choice(0, Nv-1);

  vector<vector<int>> Coordinates(Nv);
  vector<vector<vector<int>>> Neighbors(Nv);

  vector<double> Mspin;

  int State[L][L];

  // En qué entrada de las coordenadas estoy
  int count = 0;

  for(int y=0; y<L;y++){
      for(int x=0; x<L;x++){
        Coordinates[count] = {x,y};
        Neighbors[count] = {{(x+1)%L,y},
		            {(x-1+L)%L,y},
                            {x,(y+1)%L},
                            {x,(y-1+L)%L}};
        State[x][y] = 2*RandomChoice({0.5, 0.5},gen)-1;
        count ++;
      }
  }


  // Algoritmo de Metropolis

  int n_flips = 10000;
  ofstream Mag_Spin ("Magnetization.dat");

  for(int t = 0; t<n_flips ; t++){
 	 Flips(T, Nv, State, Coordinates, Neighbors, s_choice, gen);
         Mag_Spin<< 1.0*t << "  " <<Magnetization_spin(State) << "   " << Energy_spin(State,Neighbors) <<endl;
  }
  
  Mag_Spin.close();

  ofstream MatrixState ("State.dat");
  for(int y=0; y<L;y++){
      for(int x=0; x<L;x++){
	  MatrixState << State[x][y]<< "   ";
       }
       MatrixState << endl;
  }
  MatrixState.close();

  return 0;

}
