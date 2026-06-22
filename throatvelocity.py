#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt

Pt = 105000  
Tt = 300     
R = 287     
gamma = 1.4  
At = 0.0012  
Pu_range = np.linspace(105000, 300000, 1000)
critical_ratio = (2 / (gamma + 1))**(gamma / (gamma - 1))
P_critical_upstream = Pt / critical_ratio

Vt = []
m_dot = [] 

for Pu in Pu_range:
    pressure_ratio = Pt / Pu  
    
    if pressure_ratio <= critical_ratio:
        T_star = Tt * (2 / (gamma + 1))
        V = np.sqrt(gamma * R * T_star)
        mdot = At * Pu * np.sqrt(gamma / (R * Tt)) * (2 / (gamma + 1))**((gamma + 1) / (2 * (gamma - 1)))
    else:
        V = np.sqrt(2 * (gamma / (gamma - 1)) * R * Tt * (1 - (pressure_ratio)**((gamma - 1) / gamma)))
        term1 = At * Pu / np.sqrt(R * Tt)
        term2 = (pressure_ratio)**(1 / gamma)
        term3 = np.sqrt((2 * gamma / (gamma - 1)) * (1 - (pressure_ratio)**((gamma - 1) / gamma)))
        mdot = term1 * term2 * term3
        
    Vt.append(V)
    m_dot.append(mdot)
plt.figure(figsize=(8, 5))  
plt.plot(np.array(Pu_range)/1000, np.array(Vt), color='darkorange', linewidth=2.5, label='Throat Velocity ($V_t$)')
plt.axvline(x=P_critical_upstream/1000, color='red', linestyle='--', linewidth=1.5, label='Choking Limit')
plt.title('Throat Velocity vs. Upstream Pressure', fontsize=14, fontweight='bold')
plt.xlabel('Upstream Pressure $P_u$ (kPa)', fontsize=12)
plt.ylabel('Velocity $V_t$ (m/s)', fontsize=12)
plt.text(120, 200, 'Subsonic', fontsize=10, color='blue', fontweight='bold')
plt.text(220, 200, 'Sonic (Choked)', fontsize=10, color='red', fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

