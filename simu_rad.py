import pybamm
import os
os.chdir(pybamm.__path__[0]+'/..')
import math
import random
import matplotlib.pyplot as plt
from csv import writer
parameter_values = pybamm.ParameterValues('Chen2020')
parameter_values["Lower voltage cut-off [V]"] = 3
parameter_values['Separator thickness [m]'] = 5e-05
parameter_values['Typical current [A]'] = 0.68

pop_size = 30 
max_gen = 100
N_t_min = 0.00005
N_t_max = 0.00015
P_t_min = 0.00005
P_t_max = 0.00015
N_p_min = 0.1
N_p_max = 0.4
P_p_min = 0.1
P_p_max = 0.4
N_r_max = 20.0e-06
N_r_min = 1.0e-06
P_r_min = 1.0e-06
P_r_max = 20.0e-06
rad = []
P = []
W = []
V_1 = []
C = []
P_1 = []
W_1 = []
V_2 = []
C_1 = []
for i in range(0,pop_size):
    try:
        solution = []
        solution__N_t = N_t_min+(N_t_max-N_t_min)*random.random()
        solution.append(round(solution__N_t,6))
        solution__P_t = P_t_min+(P_t_max-P_t_min)*random.random()
        solution.append(round(solution__P_t,6))
        solution__N_p = N_p_min+(N_p_max-N_p_min)*random.random()
        solution.append(round(solution__N_p,2))
        solution__P_p = P_p_min+(P_p_max-P_p_min)*random.random()
        solution.append(round(solution__P_p,2))
        solution__N_r = N_r_min+(N_r_max-N_r_min)*random.random()
        solution.append(round(solution__N_r,6))
        solution__P_r = P_r_min+(P_r_max-P_r_min)*random.random()
        solution.append(round(solution__P_r,6))
        parameter_values['Positive particle radius [m]'] = solution[5]
        with open('/Users/soumyadeep/ddp/p_r.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            
            writer_object.writerow(solution)  
            
            f_object.close()
        rad.append(solution[0])
        model = pybamm.lithium_ion.DFN()
        safe_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="safe")
        fast_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="fast")
        safe_sim = pybamm.Simulation(model, parameter_values=parameter_values, solver=safe_solver)
        #fast_sim = pybamm.Simulation(model, parameter_values=param, solver=fast_solver)
        safe_sim.solve([0, 3600])
        print("Safe mode solve time: {}".format(safe_sim.solution.solve_time))
        #fast_sim.solve([0, 3600])
        #print("Fast mode solve time: {}".format(fast_sim.solution.solve_time))
        solution = safe_sim.solution
        t = solution["Time [s]"]
        with open('/Users/soumyadeep/ddp/t.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            
            writer_object.writerow(t.entries)  
            
            f_object.close()
        V = solution["Terminal voltage [V]"]
        with open('/Users/soumyadeep/ddp/v.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            
            writer_object.writerow(V.entries)  
            
            f_object.close()
        x1= solution["Discharge capacity [A.h]"]
        with open('/Users/soumyadeep/ddp/c.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            
            writer_object.writerow(x1.entries)  
            
            f_object.close()
        
        
    except:
        continue
