#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

