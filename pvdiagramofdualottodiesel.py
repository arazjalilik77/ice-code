#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

