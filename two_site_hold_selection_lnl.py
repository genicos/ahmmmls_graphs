import matplotlib.pyplot as plt 
import copy

# Loading data
trueanalysis = open("data/two_site_hold_selection_true_8_9", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/two_site_hold_selection_false_8_9", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")


plt.rcParams["font.family"] = "Arial"


# Mapping values
m_to_i = {"0.05":0, "0.1":1, "0.2":2, "0.5":3}
m = [0.05,0.1, 0.2, 0.5]

generations_to_i = {"100":0, "200":1, "500":2, "1000":3}
generations = [100, 200, 500, 1000]

dist_to_i = {"0.005":0, "0.01":1, "0.02":2, "0.05":3}
dist = [0.005, 0.01, 0.02, 0.05]





#Creating arrays of lnl
truelnl_diff = [[None]*4,[None]*4,[None]*4,[None]*4]

for i in range(4):
    for j in range(4):
        truelnl_diff[i][j] = [[],[],[],[]]

falselnl_diff = [[None]*4,[None]*4,[None]*4,[None]*4]

for i in range(4):
    for j in range(4):
        falselnl_diff[i][j] = [[],[],[],[]]


for line in trueanalysis:
    truelnl_diff[dist_to_i[line[3]]][m_to_i[line[2]]][generations_to_i[line[1]]].append(float(line[7]) - float(line[4]))

for line in falseanalysis:
    falselnl_diff[dist_to_i[line[3]]][m_to_i[line[2]]][generations_to_i[line[1]]].append(float(line[7]) - float(line[4]))





alt_correct = [[None]*4,[None]*4,[None]*4,[None]*4]
for i in range(4):
    for j in range(4):
        alt_correct[i][j] = [0,0,0,0]

null_correct = [[None]*4,[None]*4,[None]*4,[None]*4]
for i in range(4):
    for j in range(4):
        null_correct[i][j] = [0,0,0,0]

for i in range(4):
    for j in range(4):
        for k in range(4):
            cutoff = 0

            sorted_list = copy.deepcopy(falselnl_diff[i][j][k])
            sorted_list.sort()

            cutoff = sorted_list[-2]

            for h in range(20):
                if truelnl_diff[i][j][k][h] > cutoff:
                    alt_correct[i][j][k] += 0.05
                if falselnl_diff[i][j][k][h] < cutoff:
                    null_correct[i][j][k] += 0.05
                
                







#Plotting
fig, axe = plt.subplots(4, 4, constrained_layout=True, sharex=True, sharey=True)

x = [1,2,3,4]
xlabels = ["100","200","500","1000"]

for i in range(4):
    for j in range(4):
        ax = axe[i,j]
        ax.set_ylim([0,1.1])
        ax.set_yticks([0,0.25,0.5,0.75,1])
        ax.grid(axis = 'y')
        ax.set_xticks([1,2,3,4])

        ax.plot(x, alt_correct[i][j] ,color='black', linestyle='-', marker='s', markersize=5)

        ax.set_xticklabels(xlabels)
        ax.yaxis.set_label_position("right")

        if (i == 0):
            ax.set_title("m = " + str(m[j]))
        if (j == 3):
            ax.set_ylabel("dist = "+str(dist[i]))




fig.text(0.5, 0.01, 'Admixture Time (Generations)', ha='center')
fig.text(0.01, 0.5, 'Proportion Correct', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(bottom=0.1, left=0.1, top=0.9, right=0.9,wspace=0.2, hspace=0.3)

plt.show()