import matplotlib.pyplot as plt


#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]


#Loading data
trueanalysis = open("data/two_site_true_4_14", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")



# Mapping values
sel_to_i = {"0.001":0, "0.005":1, "0.01":2, "0.05":3}
sel = [0.001,0.005, 0.01, 0.05]

dist_to_i = {"0.005":0, "0.01":1, "0.02":2, "0.05":3}
dist = [0.005, 0.01, 0.02, 0.05]


#Creating arrays
one_site_sel   = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
two_site_0_sel = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
two_site_1_sel = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]


for line in trueanalysis:
    true_sel_0 = float(line[1].split(",")[0][1:])
    true_sel_1 = float(line[1].split(",")[1][:-1])

    if(true_sel_0 == true_sel_1):
        one_site_sel[sel_to_i[str(true_sel_0)]][dist_to_i[line[2]]].append(float(line[4]))
        two_site_0_sel[sel_to_i[str(true_sel_0)]][dist_to_i[line[2]]].append(float(line[7]))
        two_site_1_sel[sel_to_i[str(true_sel_0)]][dist_to_i[line[2]]].append(float(line[9]))


fig, axe = plt.subplots(3, 4, constrained_layout=True, sharex=True, sharey="row")

x = [[],[],[]]
for i in range(3):
    for j in range(20):
        x[i].append((i+1) - 0.25 + (j/20)*0.5)

xlabels = ["Two site\none","Two site\ntwo","One\nsite"]

for i in range(3):
    for j in range(4):
        ax = axe[i,j]
        ax.set_xticks([1,2,3])
        ax.set_xticklabels(xlabels, fontsize=7.5)
        ax.yaxis.set_label_position("right")

        ax.scatter(x[0], two_site_0_sel[i+1][j], s=1, color=color_scheme["blue"])
        ax.scatter(x[1], two_site_1_sel[i+1][j], s=1, color=color_scheme["cyan"])
        ax.scatter(x[2], one_site_sel[i+1][j], s=1, color=color_scheme["yellow"])
        
        ax.axhline(y = sel[i+1], color='black')
        ax.grid(axis = 'y')

        if (i == 0):
            ax.set_title("dist = " + str(dist[j]))
            ax.set_yticks([0,0.005,0.01,0.015])
            ax.set_ylim([0,0.015])
        if (i == 1):
            ax.set_yticks([0,0.01,0.02,0.03])
            ax.set_ylim([0,0.03])
        if (i == 2):
            ax.set_yticks([0,0.05,0.1,0.15,0.2])
            ax.set_ylim([0,0.2])
        if (j == 3):
            ax.set_ylabel("s = "+str(sel[i+1]))



fig.text(-0, 0.5, 'Selection Coefficient', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(wspace=0.1, hspace=0.2)


plt.show()