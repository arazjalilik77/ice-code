#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

R = 0.287
Cp = 1.005 
Cv = 0.718 
k = 1.4
P1 = 100 
T1 = 300 
alpha = 1.7 
cutoff_percent = 0.05 
T_max_limit = 2500
r_range = np.linspace(12, 18, 100)

def analyze_dual_cycle(r):
    V1 = R * T1 / P1
    V2 = V1 / r
    P2 = P1 * (r**k)
    T2 = T1 * (r**(k-1))
    V3 = V2
    P3 = alpha * P2
    T3 = alpha * T2
    beta = 1 + 0.05 * (r - 1)
    V4 = beta * V3
    P4 = P3
    T4 = T3 * beta
    
    Qin = Cv * (T3 - T2) + Cp * (T4 - T3)
    return T4, Qin, beta

optimal_r = 12
max_qin = 0
for r in r_range:
    T4, Qin, beta = analyze_dual_cycle(r)
    if T4 <= T_max_limit:
        optimal_r = r
        max_qin = Qin
    else:
        break

print(f"Optimal Compression Ratio: {optimal_r:.2f}")
print(f"Max Temperature at Optimal r: {analyze_dual_cycle(optimal_r)[0]:.2f} K")
print(f"Heat Input at Optimal r: {max_qin:.2f} kJ/kg")

def get_pv_points(r, cycle_type, Qin_fixed):
    V1 = R * T1 / P1
    V2 = V1 / r
    
    if cycle_type == 'Dual':
        T4, Qin, beta = analyze_dual_cycle(r)
        v12 = np.linspace(V1, V2, 50)
        p12 = P1 * (V1 / v12)**k
        v23 = [V2, V2]
        p23 = [P1*r**k, alpha*P1*r**k]
        v34 = [V2, beta*V2]
        p34 = [alpha*P1*r**k, alpha*P1*r**k]
        V4 = beta * V2
        P4 = alpha * P1 * r**k
        V5 = V1
        v45 = np.linspace(V4, V5, 50)
        p45 = P4 * (V4 / v45)**k
        v51 = [V1, V1]
        p51 = [p45[-1], P1]
        return np.concatenate([v12, v23, v34, v45, v51]), np.concatenate([p12, p23, p34, p45, p51])

    elif cycle_type == 'Otto':
        T2 = T1 * r**(k-1)
        T3 = Qin_fixed / Cv + T2
        P2 = P1 * r**k
        P3 = P2 * (T3/T2)
        v12 = np.linspace(V1, V2, 50)
        p12 = P1 * (V1 / v12)**k
        v23 = [V2, V2]
        p23 = [P2, P3]
        v34 = np.linspace(V2, V1, 50)
        p34 = P3 * (V2 / v34)**k
        v41 = [V1, V1]
        p41 = [p34[-1], P1]
        return np.concatenate([v12, v23, v34, v41]), np.concatenate([p12, p23, p34, p41])

    elif cycle_type == 'Diesel':
        T2 = T1 * r**(k-1)
        T3 = Qin_fixed / Cp + T2
        beta_d = T3 / T2
        V3_d = beta_d * V2
        P2 = P1 * r**k
        v12 = np.linspace(V1, V2, 50)
        p12 = P1 * (V1 / v12)**k
        v23 = [V2, V3_d]
        p23 = [P2, P2]
        v34 = np.linspace(V3_d, V1, 50)
        p34 = P2 * (V3_d / v34)**k
        v41 = [V1, V1]
        p41 = [p34[-1], P1]
        return np.concatenate([v12, v23, v34, v41]), np.concatenate([p12, p23, p34, p41])

v_dual, p_dual = get_pv_points(optimal_r, 'Dual', max_qin)
v_otto, p_otto = get_pv_points(optimal_r, 'Otto', max_qin)
v_diesel, p_diesel = get_pv_points(optimal_r, 'Diesel', max_qin)

plt.figure(figsize=(10, 6))
plt.plot(v_dual, p_dual, 'r-', label='Dual Cycle', linewidth=2)
plt.plot(v_otto, p_otto, 'b--', label='Otto Cycle', linewidth=2)
plt.plot(v_diesel, p_diesel, 'g-.', label='Diesel Cycle', linewidth=2)
plt.xlabel('Volume (m³/kg)')
plt.ylabel('Pressure (kPa)')
plt.title(f'P-V Diagram Comparison (r = {optimal_r:.2f})')
plt.legend()
plt.grid(True)
plt.savefig('/mnt/data/PV_Comparison.png')
plt.show()


# In[1]:





# In[1]:


import numpy as np
import matplotlib.pyplot as plt

P1 = 100          
T1 = 300         
R = 0.287         
cp = 1.005        
cv = 0.718       
k = 1.4

r = 14.55         
alpha = 1.7       
qin = 1453.46    

V1 = R * T1 / P1
V2 = V1 / r

T2_dual = T1 * r**(k - 1)
P2_dual = P1 * r**k

T3_dual = alpha * T2_dual
P3_dual = alpha * P2_dual
V3_dual = V2

beta = 1 + 0.05 * (r - 1)
V4_dual = beta * V3_dual
P4_dual = P3_dual
T4_dual = beta * T3_dual

V5_dual = V1
P5_dual = P4_dual * (V4_dual / V5_dual)**k
T5_dual = T4_dual * (V4_dual / V5_dual)**(k - 1)

V12_dual = np.linspace(V1, V2, 100)
P12_dual = P1 * (V1 / V12_dual)**k

V23_dual = np.array([V2, V3_dual])
P23_dual = np.array([P2_dual, P3_dual])

V34_dual = np.array([V3_dual, V4_dual])
P34_dual = np.array([P3_dual, P4_dual])

V45_dual = np.linspace(V4_dual, V5_dual, 100)
P45_dual = P4_dual * (V4_dual / V45_dual)**k

V51_dual = np.array([V5_dual, V1])
P51_dual = np.array([P5_dual, P1])

T2_otto = T1 * r**(k - 1)
P2_otto = P1 * r**k

T3_otto = T2_otto + qin / cv
P3_otto = P2_otto * (T3_otto / T2_otto)
V3_otto = V2

V4_otto = V1
P4_otto = P3_otto * (V3_otto / V4_otto)**k
T4_otto = T3_otto * (V3_otto / V4_otto)**(k - 1)

V12_otto = np.linspace(V1, V2, 100)
P12_otto = P1 * (V1 / V12_otto)**k

V23_otto = np.array([V2, V3_otto])
P23_otto = np.array([P2_otto, P3_otto])

V34_otto = np.linspace(V3_otto, V4_otto, 100)
P34_otto = P3_otto * (V3_otto / V34_otto)**k

V41_otto = np.array([V4_otto, V1])
P41_otto = np.array([P4_otto, P1])

T2_diesel = T1 * r**(k - 1)
P2_diesel = P1 * r**k

T3_diesel = T2_diesel + qin / cp
rho = T3_diesel / T2_diesel
V3_diesel = rho * V2
P3_diesel = P2_diesel

V4_diesel = V1
P4_diesel = P3_diesel * (V3_diesel / V4_diesel)**k
T4_diesel = T3_diesel * (V3_diesel / V4_diesel)**(k - 1)

V12_diesel = np.linspace(V1, V2, 100)
P12_diesel = P1 * (V1 / V12_diesel)**k

V23_diesel = np.array([V2, V3_diesel])
P23_diesel = np.array([P2_diesel, P3_diesel])

V34_diesel = np.linspace(V3_diesel, V4_diesel, 100)
P34_diesel = P3_diesel * (V3_diesel / V34_diesel)**k

V41_diesel = np.array([V4_diesel, V1])
P41_diesel = np.array([P4_diesel, P1])

plt.figure(figsize=(10, 7))

plt.plot(V12_dual, P12_dual, 'r-', linewidth=2, label='Dual Cycle')
plt.plot(V23_dual, P23_dual, 'r-', linewidth=2)
plt.plot(V34_dual, P34_dual, 'r-', linewidth=2)
plt.plot(V45_dual, P45_dual, 'r-', linewidth=2)
plt.plot(V51_dual, P51_dual, 'r-', linewidth=2)

plt.plot(V12_otto, P12_otto, 'b--', linewidth=2, label='Otto Cycle')
plt.plot(V23_otto, P23_otto, 'b--', linewidth=2)
plt.plot(V34_otto, P34_otto, 'b--', linewidth=2)
plt.plot(V41_otto, P41_otto, 'b--', linewidth=2)
plt.plot(V12_diesel, P12_diesel, 'g-.', linewidth=2, label='Diesel Cycle')
plt.plot(V23_diesel, P23_diesel, 'g-.', linewidth=2)
plt.plot(V34_diesel, P34_diesel, 'g-.', linewidth=2)
plt.plot(V41_diesel, P41_diesel, 'g-.', linewidth=2)

plt.scatter(
    [V1, V2, V3_dual, V4_dual, V5_dual],
    [P1, P2_dual, P3_dual, P4_dual, P5_dual],
    color='red',
    s=35
)

plt.scatter(
    [V1, V2, V3_otto, V4_otto],
    [P1, P2_otto, P3_otto, P4_otto],
    color='blue',
    s=35
)

plt.scatter(
    [V1, V2, V3_diesel, V4_diesel],
    [P1, P2_diesel, P3_diesel, P4_diesel],
    color='green',
    s=35
)

plt.xlabel('Specific Volume, v (m³/kg)', fontsize=12)
plt.ylabel('Pressure, P (kPa)', fontsize=12)
plt.title('P-V Diagram Comparison of Dual, Otto, and Diesel Cycles', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig('PV_Diagram_Dual_Otto_Diesel.png', dpi=300)

plt.show()

print('===== Dual Cycle =====')
print(f'T2 = {T2_dual:.2f} K')
print(f'T3 = {T3_dual:.2f} K')
print(f'T4 = {T4_dual:.2f} K')
print(f'P2 = {P2_dual:.2f} kPa')
print(f'P3 = {P3_dual:.2f} kPa')
print(f'P4 = {P4_dual:.2f} kPa')
print(f'Cut-off ratio beta = {beta:.4f}')

print('\n===== Otto Cycle =====')
print(f'T2 = {T2_otto:.2f} K')
print(f'T3 = {T3_otto:.2f} K')
print(f'T4 = {T4_otto:.2f} K')
print(f'P2 = {P2_otto:.2f} kPa')
print(f'P3 = {P3_otto:.2f} kPa')
print(f'P4 = {P4_otto:.2f} kPa')

print('\n===== Diesel Cycle =====')
print(f'T2 = {T2_diesel:.2f} K')
print(f'T3 = {T3_diesel:.2f} K')
print(f'T4 = {T4_diesel:.2f} K')
print(f'P2 = {P2_diesel:.2f} kPa')
print(f'P3 = {P3_diesel:.2f} kPa')
print(f'P4 = {P4_diesel:.2f} kPa')
print(f'Cut-off ratio rho = {rho:.4f}')


# In[1]:


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


# In[1]:


import numpy as np
import matplotlib.pyplot as plt
crank_angles = np.linspace(-180, 540, 1000)
  
IVO, IVC = -10, 220 
EVO, EVC = 320, 550  

intake_lift = np.zeros_like(crank_angles)
exhaust_lift = np.zeros_like(crank_angles)

for i, ca in enumerate(crank_angles):
    if IVO <= ca <= IVC:
        intake_lift[i] = 9.5 * np.sin(np.pi * (ca - IVO) / (IVC - IVO)) 
    if EVO <= ca <= EVC:
        exhaust_lift[i] = 8.5 * np.sin(np.pi * (ca - EVO) / (EVC - EVO)) 

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
    
m_dot_gs = np.array(m_dot) * 1000
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

axes[0].plot(crank_angles, intake_lift, label='Intake Valve (ورودی)', color='blue', linewidth=2.5)
axes[0].plot(crank_angles, exhaust_lift, label='Exhaust Valve (تخلیه)', color='red', linewidth=2.5)
axes[0].set_title('1. Valve Lift Profile (EF7 Engine)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Crank Angle (Degrees)', fontsize=10)
axes[0].set_ylabel('Valve Lift (mm)', fontsize=10)
axes[0].axhline(0, color='black', linewidth=0.8, linestyle='--')
axes[0].set_xlim(-180, 540)
axes[0].set_xticks([-180, -90, 0, 90, 180, 270, 360, 450, 540])
axes[0].grid(True, linestyle=':', alpha=0.6)
axes[0].legend(loc='upper right')

axes[1].plot(Pu_range/1000, Vt, color='darkorange', linewidth=2.5, label='Throat Velocity ($V_t$)')
axes[1].axvline(x=P_critical_upstream/1000, color='red', linestyle='--', linewidth=1.5, label='Choking Limit')
axes[1].set_title('2. Throat Velocity vs. Upstream Pressure', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Upstream Pressure $P_u$ (kPa)', fontsize=10)
axes[1].set_ylabel('Velocity $V_t$ (m/s)', fontsize=10)

axes[1].text(120, 200, 'Subsonic', fontsize=10, color='blue', fontweight='bold')
axes[1].text(220, 200, 'Sonic (Choked)', fontsize=10, color='red', fontweight='bold')
axes[1].grid(True, linestyle=':', alpha=0.6)
axes[1].legend(loc='lower right')

axes[2].plot(Pu_range/1000, m_dot_gs, color='green', linewidth=2.5, label='Mass Flow Rate ($\dot{m}$)')
axes[2].axvline(x=P_critical_upstream/1000, color='red', linestyle='--', linewidth=1.5, label='Choking Limit')
axes[2].set_title('3. Mass Flow Rate vs. Upstream Pressure', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Upstream Pressure $P_u$ (kPa)', fontsize=10)
axes[2].set_ylabel('Mass Flow Rate $\dot{m}$ (g/s)', fontsize=10)

axes[2].text(120, m_dot_gs[-1]*0.4, 'Subsonic Region', fontsize=10, color='blue', fontweight='bold')
axes[2].text(220, m_dot_gs[-1]*0.4, 'Choked Region', fontsize=10, color='red', fontweight='bold')
axes[2].grid(True, linestyle=':', alpha=0.6)
axes[2].legend(loc='lower right')


plt.tight_layout()
plt.show()


# In[1]:


import numpy as np
import matplotlib.pyplot as plt

crank_angles = np.linspace(-180, 560, 2000) 

IVO, IVC = -10, 220
EVO, EVC = 320, 550

intake_lift = np.zeros_like(crank_angles)
exhaust_lift = np.zeros_like(crank_angles)
 
intake_lift[(crank_angles >= IVO) & (crank_angles <= IVC)] = 9.5 * np.sin(
    np.pi * (crank_angles[(crank_angles >= IVO) & (crank_angles <= IVC)] - IVO) / (IVC - IVO)
)

exhaust_lift[(crank_angles >= EVO) & (crank_angles <= EVC)] = 8.5 * np.sin(
    np.pi * (crank_angles[(crank_angles >= EVO) & (crank_angles <= EVC)] - EVO) / (EVC - EVO)
)

plt.figure(figsize=(10, 5))
plt.plot(crank_angles, intake_lift, label='Intake Valve Lift', color='blue', linewidth=2)
plt.plot(crank_angles, exhaust_lift, label='Exhaust Valve Lift', color='red', linewidth=2)

plt.title('Valve Lift Profile', fontsize=14)
plt.xlabel('Crank Angle (deg)', fontsize=12)
plt.ylabel('Valve Lift (mm)', fontsize=12)
plt.xlim(-180, 560)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()


# In[2]:


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


# In[1]:


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


# In[ ]:




