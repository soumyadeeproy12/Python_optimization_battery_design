import pybamm
import os
os.chdir(pybamm.__path__[0]+'/..')
import math
import random
import matplotlib.pyplot as plt
from csv import writer
import time
def parameter_init(b):
    model = pybamm.lithium_ion.DFN()
    parameter_values =  model.default_parameter_values
    if len(b)==0:
      parameter_values["Lower voltage cut-off [V]"] = 3
      parameter_values['Negative electrode thickness [m]']=10e-05
      parameter_values['Positive electrode thickness [m]']=11.8e-05
      parameter_values['Separator thickness [m]'] = 5e-05
      parameter_values['Typical current [A]'] = 0.68
    else:
      parameter_values["Lower voltage cut-off [V]"] = 3
      parameter_values['Negative electrode thickness [m]']=b[0]
      parameter_values['Positive electrode thickness [m]']=b[1]
      parameter_values['Separator thickness [m]'] = 5e-05
      parameter_values['Typical current [A]'] = 0.68
      parameter_values['Negative electrode porosity'] = b[2]
      parameter_values['Positive electrode porosity'] = b[3]
      parameter_values['Negative particle radius [m]'] = b[4]
      parameter_values['Positive particle radius [m]'] = b[5]
    return parameter_values

def solve_model(b):
    safe_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="safe")
    parameter_values = parameter_init(b)
    model = pybamm.lithium_ion.DFN()
    safe_sim = pybamm.Simulation(model, parameter_values=parameter_values, solver=safe_solver)
    #fast_sim = pybamm.Simulation(model, parameter_values=param, solver=fast_solver)
    safe_sim.solve([0, 3600])
    print("Safe mode solve time: {}".format(safe_sim.solution.solve_time))
    #fast_sim.solve([0, 3600])
    #print("Fast mode solve time: {}".format(fast_sim.solution.solve_time))
    solution = safe_sim.solution
    t = solution["Time [s]"]
    V = solution["Terminal voltage [V]"]
    x1= solution["Discharge capacity [A.h]"]
    xx = x1.entries*V.entries/0.0562
    y1= solution["Power [W]"]
  
    return xx[-2], y1.entries[-2]

#First function to optimize
def function1(a,b):
    m,n = solve_model(b)
    return m
  
  #Second function to optimize
def function2(a,b):
    m,n = solve_model(b)
    return n/0.0562
