import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import chi2
import seaborn as sns



#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

# Loading data
slowanalysis = open("data/pop_size_large_slow_temp_4_7", "r").readlines()
slowanalysis = slowanalysis[1:]
for i in range(len(slowanalysis)):
    slowanalysis[i] = slowanalysis[i].split("\t")


# Mapping values
pop_to_i = {"1000000":0, "100000":1, "10000":2, "1000":3}
pop = [1000000, 100000, 10000, 1000]

lnl_slow = [[[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]

for line in slowanalysis:
	lnl_slow[0][pop_to_i[line[1]]].append(float(line[2]))
	lnl_slow[1][pop_to_i[line[1]]].append(float(line[3]))




lnl_slow1_0 = [[],[],[],[]] # ratio of 1 parameter to 0 parameter



for i in range(4):
	for j in range(50):
		lnl_slow1_0[i].append(lnl_slow[1][i][j] - lnl_slow[0][i][j])




chi2_sample = np.random.chisquare(1,50)




x = [chi2_sample] + lnl_slow1_0
xlabels = ["$\chi^2_1$", 'Ne = 1,000,000','Ne = 100,000','Ne = 10,000', 'Ne = 1,000']

#sns.set(font="DejaVu Sans")
sns.set(rc={'figure.figsize':(7,8)}, font="DejaVu Sans")
sns.set_style("whitegrid")
ax = sns.swarmplot(data=x, size=3, color="black")

plt.xticks([0,1,2,3,4],xlabels)
ax.set(ylabel="lnL ratio")
plt.show()