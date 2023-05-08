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
trueanalysis = open("data/speed_ups_true_3_30", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/speed_ups_false_3_30", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")


# Mapping values
sel_to_i = {'(.01,.01)':0, '(.05,.05)':1}
dist_to_i = {'0.01':0,'0.05':1}
R_to_i = {'0.02':0,'0.1':1}
k_to_i = {'0':0,'4':1}

sel = [0.01,0.05]
dist = [0.01,0.05]
R = [0.02, 0.1]
k = [0, 4]





#Creating arrays of selection
two_site_0_sel = [[[[[],[]],[[],[]]],[[[],[]],[[],[]]]],[[[[],[]],[[],[]]],[[[],[]],[[],[]]]]]
two_site_1_sel = [[[[[],[]],[[],[]]],[[[],[]],[[],[]]]],[[[[],[]],[[],[]]],[[[],[]],[[],[]]]]]


for line in trueanalysis:
	two_site_0_sel[sel_to_i[line[1]]][dist_to_i[line[2]]][R_to_i[line[3]]][k_to_i[line[4]]].append(float(line[9]))
	two_site_1_sel[sel_to_i[line[1]]][dist_to_i[line[2]]][R_to_i[line[3]]][k_to_i[line[4]]].append(float(line[11]))



#Plotting selection
site_labels = ["Site one\nk = 4", "Site two\nk = 4","Site one\nk = 0", "Site two\nk = 0"]

fig, axe = plt.subplots(2, 2, constrained_layout=True, sharex=True, sharey="row")

x = [[],[],[],[]]
for i in range(4):
	for j in range(20):
		x[i].append((i+1) - 0.25 + (j/20)*0.5)

for i in range(2):
	for j in range(2):
		ax = axe[i,j]
		ax.set_xticks([1,2,3,4])
		ax.set_xticklabels(site_labels, fontsize=7.5)
		ax.yaxis.set_label_position("right")

		ax.scatter(x[0], two_site_0_sel[i][1][1 - j][0], s=1, color=color_scheme["blue"])
		ax.scatter(x[1], two_site_1_sel[i][1][1 - j][0], s=1, color=color_scheme["cyan"])
		ax.scatter(x[2], two_site_0_sel[i][1][1 - j][1], s=1, color=color_scheme["blue"])
		ax.scatter(x[3], two_site_1_sel[i][1][1 - j][1], s=1, color=color_scheme["cyan"])

		ax.axhline(y = sel[i], color='black')
		ax.grid(axis = 'y')
		ax.set_ylim([0,sel[i]*3])

		ax.set_yticks([0,sel[i],sel[i]*2,sel[i]*3])
		if (i == 0):
			ax.set_title("R = "+str(R[1-j]))
		if (j == 1):
			ax.set_ylabel("s = "+str(sel[i]), fontsize=10)



fig.text(0.005, 0.5, 'Selection Coefficient', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(left=0.1,wspace=0.1, hspace=0.2)


plt.show()