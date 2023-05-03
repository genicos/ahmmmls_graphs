import matplotlib.pyplot as plt
import copy

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"

# Loading data
trueanalysis = open("data/two_site_miss_t_true_2_8", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/two_site_miss_t_false_2_8", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")



# Mapping values
missf_to_i = {"0.5":0, "0.8":1, "1.2":2, "2":3}
missf = [0.5 , 0.8, 1.2, 2]

generations_to_i = {"100":0, "200":1, "500":2, "1000":3}
generations = [100, 200, 500, 1000]






#Creating arrays of selection
true_sel_0 = [None]*4
true_sel_1 = [None]*4

for i in range(4):
    true_sel_0[i] = [[],[],[],[]]
    true_sel_1[i] = [[],[],[],[]]


for line in trueanalysis:
    true_sel_0[generations_to_i[line[1]]][missf_to_i[line[2]]].append(float(line[7]))
    true_sel_1[generations_to_i[line[1]]][missf_to_i[line[2]]].append(float(line[9]))





xlabels = ["0.5","0.8","1.2","2"]




x = [[],[],[],[]]
for i in range(4):
    for j in range(20):
        x[i].append((i+1) - 0.25 + (j/20)*0.5)

fig, axe = plt.subplots(1, 4, figsize=(8, 2.5),constrained_layout=True, sharex=False, sharey=True)


count_all = 20*4*2*2
count_close = 0

for i in range(4):
    ax = axe[i]
    ax.set_xticks([1,2,3,4])

    ax.scatter(x[0], true_sel_0[i][0], s=1, color=color_scheme["blue"])
    ax.scatter(x[0], true_sel_1[i][0], s=1, color=color_scheme["yellow"])
    ax.scatter(x[1], true_sel_0[i][1], s=1, color=color_scheme["blue"])
    ax.scatter(x[1], true_sel_1[i][1], s=1, color=color_scheme["yellow"])
    ax.scatter(x[2], true_sel_0[i][2], s=1, color=color_scheme["blue"])
    ax.scatter(x[2], true_sel_1[i][2], s=1, color=color_scheme["yellow"])
    ax.scatter(x[3], true_sel_0[i][3], s=1, color=color_scheme["blue"])
    ax.scatter(x[3], true_sel_1[i][3], s=1, color=color_scheme["yellow"])

    ax.axhline(y = 0.01, color='black')
    ax.grid(axis = 'y')

    
    ax.yaxis.set_label_position("right")

    xlabels = missf.copy()
    for j in range(len(xlabels)):
        xlabels[j] *= generations[i]
        xlabels[j] = int(xlabels[j])
    ax.set_xticklabels(xlabels)

    if i > 1:
        for j in range(4):
            for k in range(20):
                if true_sel_0[i][j][k] >= 0.01*(1/1.3) and true_sel_0[i][j][k] <= 0.01*(1.3):
                    count_close += 1
                if true_sel_1[i][j][k] >= 0.01*(1/1.3) and true_sel_1[i][j][k] <= 0.01*(1.3):
                    count_close += 1

    
    ax.set_title("t = " + str(generations[i]))



fig.text(0.5, 0.015, 'Misspecified Time (Generations)', ha='center')
fig.text(0.01, 0.5, 'Selection Coefficient', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(bottom=0.2, left=0.08, top=0.8, right=0.92, wspace=0.2)


plt.show()