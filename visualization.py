import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

x_axis = [5,10,15,20,25,30,35,40]
y_min_degree = [0.024224634170532226, 0.05546354293823242, 0.10960419178009033, 0.13241652488708497, 0.23422173500061036, 0.21953582763671875, 0.26385112762451174, 0.31724456787109373]
y_min_fill = [0.02442502498626709, 0.055252723693847657, 0.10894662857055665, 0.1325468349456787, 0.23132236003875734, 0.22063642978668213, 0.2647183609008789, 0.31444629192352297]
y_random = [0.0239223051071167, 0.055743441581726075, 0.11162259101867676, 0.14230809688568116, 0.7441509962081909, 1.6792025089263916, 8.385221614837647, 26.11791625022888]

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
plt.yticks(y_random)

plt.legend()
plt.show()

