import numpy as np
import scipy.stats as st
from scipy.stats import beta
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [10, 7]

# Bell shape
x = np.linspace(0, 1, 10000)
y1 = beta.pdf(x, 2, 8)

plt.title("PDF of Beta (Bell-shape)", fontsize=20)
plt.xlabel("X", fontsize=16)
plt.ylabel("Probability Density", fontsize=16)
plt.plot(x, y1, linewidth=3, color='firebrick')
plt.annotate("Beta(2,8)", xy=(0.15, 3.7), size = 14, ha='center', va='center', color='firebrick')
plt.ylim([0, 4])
plt.xlim([0, 1])
plt.show()

20/(20+590)