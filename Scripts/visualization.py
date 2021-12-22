import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

x_axis = [5,10,15,20,25,30,35,40]
y_min_degree = [0.007863903045654297, 0.08641791343688965, 0.08406186103820801, 0.1358199119567871, 0.19051003456115723, 0.7703280448913574, 7.841870784759521, 12.16676783561707]
y_min_fill = [0.00780177116394043, 0.05561709403991699, 0.058908939361572266, 0.0881948471069336, 0.135329008102417, 0.19744420051574707, 0.44266510009765625, 9.33929705619812]
y_random = [0.00843721628189087, 0.05370171070098877, 0.01399214267730713, 0.03424456119537354, 0.07466254234313965, 0.04159680604934692, 0.08788615465164185, 0.08117728233337403]

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize=(12, 8))

# set height of bar
IT = y_min_degree
ECE = y_min_fill
CSE = y_random

# Set position of bar on X axis
br1 = np.arange(len(IT))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, IT, color='navajowhite', width=barWidth,
        edgecolor='black', label='Min Degree')
plt.bar(br2, ECE, color='thistle', width=barWidth,
        edgecolor='black', label='Min Fill')
plt.bar(br3, CSE, color='mediumaquamarine', width=barWidth,
        edgecolor='black', label='Random')
plt.plot(CSE, color='darkred')

# Adding Xticks
plt.xlabel('# of Variables', fontweight='bold', fontsize=15)
plt.ylabel('Runtime in Seconds', fontweight='bold', fontsize=15)
plt.xticks([r + barWidth for r in range(len(IT))],
           ['5', '10', '15', '20', '25', '30', '35', '40'])
plt.yscale('log')
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.yticks(y_min_degree)

plt.legend()
plt.show()

