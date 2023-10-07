import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import copy

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"



# Loading data
trueanalysis = open("data/epistasis_true_8_7", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/epistasis_false_8_7", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")




# Mapping values
value_to_i = {"0.05False":0, "0.1False":1, "0.01True":2, "0.05True":3}

sel = [100, 200, 500, 1000]


#Creating arrays of lnl
truelnl_diff = [[],[],[],[]]

falselnl_diff = [[],[],[],[]]

for line in trueanalysis:
    truelnl_diff[value_to_i[line[1]+line[2]]].append(float(line[4]) - float(line[3]))

for line in falseanalysis:
    falselnl_diff[value_to_i[line[1]+line[2]]].append(float(line[4]) - float(line[3]))


alt_correct = [0,0,0,0]

for i in range(4):
    cutoff = 0

    sorted_list = copy.deepcopy(falselnl_diff[i])
    sorted_list.sort()

    cutoff = sorted_list[-2]

    for h in range(20):
        if truelnl_diff[i][h] > cutoff:
            alt_correct[i] += 0.05


#Creating arrays of location
location_two0 = [[],[],[],[]]
location_two1 = [[],[],[],[]]

for line in trueanalysis:
	location_two0[value_to_i[line[1]+line[2]]].append(float(line[6]) - 0.05)
	location_two1[value_to_i[line[1]+line[2]]].append(float(line[8]) - 0.35)



#Creating arrays of selection
two_site_0_sel = [[],[],[],[]]
two_site_1_sel = [[],[],[],[]]

for line in trueanalysis:
	two_site_0_sel[value_to_i[line[1]+line[2]]].append(float(line[5]))
	two_site_1_sel[value_to_i[line[1]+line[2]]].append(float(line[7]))




fig, ax = plt.subplots(2, 4, constrained_layout=True, sharex = "row", sharey="row", figsize=(7, 4))

x = [1,2,3,4]
xlabels = ["Recessive\ns = 0.05","Recessive\ns = 0.1","Dominant\ns = 0.01","Dominant\ns = 0.05"]


#ax1 = ax[0]
ax2 = ax[0]
ax3 = ax[1]

"""
# Plotting lnl
ax1[0].set_ylim([0,1.1])
ax1[0].set_yticks([0,0.25,0.5,0.75,1])
ax1[0].set_ylabel('Proportion Correct', labelpad=10 )
for i in range(4):
	ax1[i].grid(axis = 'y')
	ax1[i].set_xticks([1,2,3,4])
	ax1[i].set_xlim([0, 1])
	ax1[i].tick_params(labelbottom=False)

	ax1[i].plot(0.5, alt_correct[i],color='black', linestyle='-', marker='s', markersize=5)

	ax1[i].set_title(xlabels[i])

ax1[0].annotate("A", xy=(-0.82, 1), xycoords="axes fraction", weight="bold", fontsize=12)
"""


#Plotting location
for i in range(4):
	ax = ax2[i]

	ax.scatter(location_two0[i],location_two1[i],s=1, color=color_scheme["blue"])


	ax.axhline(0,color='black', zorder=0, linewidth=0.5)
	ax.axvline(0,color='black', zorder=0, linewidth=0.5)

	ax.set_xlim([-0.02, 0.02])
	ax.set_ylim([-0.02, 0.02])
	ax.set_aspect('equal')

	ax.set_title(xlabels[i])


	if i == 0:
		ax.set_yticks([-0.02,0,0.02])
		ax.set(ylabel='Position (Morgans)')
	
	ax.set(xlabel='Position (Morgans)')

ax2[0].annotate("A", xy=(-0.82, 1), xycoords="axes fraction", weight="bold", fontsize=12)


#Plotting selection
site_labels = ["Site one", "Site two"]


x = [[],[]]
for i in range(2):
	for j in range(20):
		x[i].append((i+1) - 0.25 + (j/20)*0.5)

print(x)

for i in range(4):
	ax = ax3[i]
	ax.set_xticks([1,2])
	ax.set_xticklabels(site_labels, fontsize=7.5)

	ax.scatter(x[0], two_site_0_sel[i], s=1, color=color_scheme["blue"])
	ax.scatter(x[1], two_site_1_sel[i], s=1, color=color_scheme["cyan"])
	

	ax.set_ylim([-0.04,0.04])
	ax.set_yticks([-0.04,-0.02,0, 0.02, 0.04])
	ax.set_xlim([0.7,2.3])
	ax.set_aspect(20)

	#ax.axhline(y = 0.01, color='black')
	ax.grid(axis = 'y')

	if i == 0:
		ax.set_ylabel('Selection Coefficient')
	
	

ax3[0].annotate("B", xy=(-0.82, 1), xycoords="axes fraction", weight="bold", fontsize=12)



plt.show()