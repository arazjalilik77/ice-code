#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

P1 = 100.0       
T1 = 300.0        
r = 14.55        
re = 17.0        
qin = 1453.46     
R = 0.287         
Cv = 0.718        
Cp = 1.005       
k = 1.4

V1 = R * T1 / P1  
V2 = V1 / r
T2 = T1 * r**(k - 1)
P2 = P1 * r**k

V3 = V2
T3 = T2 + qin / Cv
P3 = P2 * (T3 / T2)

V4 = V3 * re
T4 = T3 * (V3 / V4)**(k - 1)
P4 = P3 * (V3 / V4)**k

V5 = V4
P5 = P1
T5 = P5 * V5 / R

qout_45 = Cv * (T4 - T5)   
qout_51 = Cp * (T5 - T1)   

qout = qout_45 + qout_51

Wnet = qin - qout
eta = Wnet / qin

print("Atkinson Cycle Results")
print("------------------------")
print(f"T1 = {T1:.2f} K, P1 = {P1:.2f} kPa, V1 = {V1:.4f} m^3/kg")
print(f"T2 = {T2:.2f} K, P2 = {P2:.2f} kPa, V2 = {V2:.4f} m^3/kg")
print(f"T3 = {T3:.2f} K, P3 = {P3:.2f} kPa, V3 = {V3:.4f} m^3/kg")
print(f"T4 = {T4:.2f} K, P4 = {P4:.2f} kPa, V4 = {V4:.4f} m^3/kg")
print(f"T5 = {T5:.2f} K, P5 = {P5:.2f} kPa, V5 = {V5:.4f} m^3/kg")

print()
print(f"Heat input, q_in = {qin:.2f} kJ/kg")
print(f"Heat rejected, q_out = {qout:.2f} kJ/kg")
print(f"Net work output, W_net = {Wnet:.2f} kJ/kg")
print(f"Thermal efficiency = {eta * 100:.2f} %")

V_12 = np.linspace(V1, V2, 200)
P_12 = P1 * (V1 / V_12)**k

V_23 = np.array([V2, V3])
P_23 = np.array([P2, P3])

V_34 = np.linspace(V3, V4, 200)
P_34 = P3 * (V3 / V_34)**k

V_45 = np.array([V4, V5])
P_45 = np.array([P4, P5])

V_51 = np.linspace(V5, V1, 200)
P_51 = np.ones_like(V_51) * P1

plt.figure(figsize=(8, 6))

plt.plot(V_12, P_12, 'b', linewidth=2, label='1-2 Isentropic Compression')
plt.plot(V_23, P_23, 'r', linewidth=2, label='2-3 Constant-Volume Heat Addition')
plt.plot(V_34, P_34, 'g', linewidth=2, label='3-4 Isentropic Expansion')
plt.plot(V_45, P_45, 'm', linewidth=2, label='4-5 Constant-Volume Heat Rejection')
plt.plot(V_51, P_51, 'k', linewidth=2, label='5-1 Constant-Pressure Return')

states_V = [V1, V2, V3, V4, V5]
states_P = [P1, P2, P3, P4, P5]
labels = ['1', '2', '3', '4', '5']

plt.scatter(states_V, states_P, color='black', zorder=5)

for i, label in enumerate(labels):
    plt.text(states_V[i] * 1.02, states_P[i] * 1.02, label, fontsize=12)

plt.xlabel('Specific Volume, V (m³/kg)')
plt.ylabel('Pressure, P (kPa)')
plt.title('P-V Diagram of Atkinson Cycle')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

