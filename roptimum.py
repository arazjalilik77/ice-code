#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

