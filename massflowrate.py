#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

Pt = 105000  
Tt = 300    
R = 287      
gamma = 1.4  
At = 0.0015   

Pu_range = np.linspace(105000, 300000, 500)
critical_ratio = (2 / (gamma + 1))**(gamma / (gamma - 1))

Vt = []
m_dot = []

for Pu in Pu_range:
    pressure_ratio = Pt / Pu 
    
    if pressure_ratio <= critical_ratio:
        T_star = Tt * (2 / (gamma + 1))
        V = np.sqrt(gamma * R * T_star)
    
        term1 = At * Pu / np.sqrt(Tt)
        term2 = np.sqrt(gamma / R)
        term3 = (2 / (gamma + 1))**((gamma + 1) / (2 * (gamma - 1)))
        mdot = term1 * term2 * term3
        
    else:
        V = np.sqrt(2 * (gamma / (gamma - 1)) * R * Tt * (1 - (pressure_ratio)**((gamma - 1) / gamma)))
        
        term1 = At * Pu / np.sqrt(R * Tt)
        term2 = (pressure_ratio)**(1 / gamma)
        term3 = np.sqrt((2 * gamma / (gamma - 1)) * (1 - (pressure_ratio)**((gamma - 1) / gamma)))
        mdot = term1 * term2 * term3
        
    Vt.append(V)
    m_dot.append(mdot)
m_dot_gs = np.array(m_dot) * 1000
P_critical_val = Pt / critical_ratio


plt.figure(figsize=(10, 6))
plt.plot(Pu_range/1000, m_dot_gs, color='darkgreen', linewidth=2, label='Mass Flow Rate')


plt.axvline(x=P_critical_val/1000, color='red', linestyle='--', label='Sonic Limit (Choking Point)')

plt.text(140, 100, 'Subsonic Region', fontsize=12, fontweight='bold', color='blue')
plt.text(220, 100, 'Choked (Sonic) Region', fontsize=12, fontweight='bold', color='red')

plt.title('Mass Flow Rate vs Upstream Pressure (Seamless Transition)', fontsize=14)
plt.xlabel('Upstream Pressure (kPa)', fontsize=12)
plt.ylabel('Mass Flow Rate (g/s)', fontsize=12)
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)

plt.show()

