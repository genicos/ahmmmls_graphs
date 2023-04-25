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
trueanalysis = open("data/pop_size_true_3_27", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/pop_size_false_3_27", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")


# Mapping values
pop_to_i = {"10000":0, "5000":1, "1000":2, "500":3}
pop = [10000,5000,1000, 500]


#Creating arrays of lnl
truelnl_diff = [[],[],[],[]]

falselnl_diff = [[],[],[],[]]

for line in trueanalysis:
    truelnl_diff[pop_to_i[line[1]]].append(float(line[5]) - float(line[2]))

for line in falseanalysis:
    falselnl_diff[pop_to_i[line[1]]].append(float(line[5]) - float(line[2]))


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
	location_two0[pop_to_i[line[1]]].append(float(line[7]))
	location_two1[pop_to_i[line[1]]].append(float(line[9]))

#Creating arrays of selection
two_site_0_sel = [[],[],[],[]]
two_site_1_sel = [[],[],[],[]]

for line in trueanalysis:
	two_site_0_sel[pop_to_i[line[1]]].append(float(line[6]))
	two_site_1_sel[pop_to_i[line[1]]].append(float(line[8]))






def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

fig = plt.figure(layout="constrained")

gs = GridSpec(3, 4, figure=fig)
ax1 = fig.add_subplot(gs[0, :])
ax2 = [fig.add_subplot(gs[1,i]) for i in range(4)]
ax3 = [fig.add_subplot(gs[2,i]) for i in range(4)]


x = [1,2,3,4]
xlabels = ["Ne = 10000","Ne = 5000","Ne = 1000","Ne = 500"]




# Plotting lnl
ax1.set_ylim([0,1.1])
ax1.set_yticks([0,0.25,0.5,0.75,1])
ax1.grid(axis = 'y')
ax1.set_xticks([1,2,3,4])
ax1.set_xlim([0.65, 4.35])
ax1.tick_params(labelbottom=False)

ax1.set(ylabel='Proportion Correct')


ax1.plot(x, alt_correct ,color='black', linestyle='-', marker='s', markersize=5)




#Plotting location

for i in range(4):
	ax = ax2[i]

	ax.scatter(location_two0[i],location_two1[i],s=1, color=color_scheme["blue"])


	ax.axhline(0.11,color='black', zorder=0, linewidth=0.5)
	ax.axvline(0.09,color='black', zorder=0, linewidth=0.5)

	ax.set_xlim([0.075, 0.1])
	ax.set_ylim([0.1, 0.125])

	ax.set_xticks([0.08, 0.09, 0.1])

	if (i > 0):
		ax.set_yticklabels([])
	else:
		ax.set(ylabel='Position (Morgans)')
	#ax.set_title("N = " + str(pop[i]))


#Plotting selection
site_labels = ["Site one", "Site two"]


x = [[],[]]
for i in range(2):
	for j in range(20):
		x[i].append((i+1) - 0.25 + (j/20)*0.5)

for i in range(4):
	ax = ax3[i]
	ax.set_xticks([1,2])
	ax.set_xticklabels(site_labels, fontsize=7.5)

	ax.scatter(x[0], two_site_0_sel[i], s=1, color=color_scheme["blue"])
	ax.scatter(x[1], two_site_1_sel[i], s=1, color=color_scheme["cyan"])

	ax.set_ylim([0,0.04])
	ax.axhline(y = 0.01, color='black')
	ax.grid(axis = 'y')
	if (i > 0):
		ax.set_yticklabels([])
	else:
		ax.set(ylabel='Selection Coefficient')
	
	ax.set(xlabel=xlabels[i])


plt.show()