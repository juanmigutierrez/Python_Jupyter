import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x_list = []
y_list = []
for i in range(100, -100, -1):
    print(i)
    x = i
    y = np.abs(i)
    x_list.append(x)
    y_list.append(y)

plt.plot(x_list, y_list)
plt.show()