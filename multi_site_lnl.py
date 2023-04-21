import matplotlib.pyplot as plt
import copy

# Loading data
trueanalysis = open("data/multi_site_true_2_8", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/multi_site_false_2_11", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")



# Mapping values
sel_to_i = {"0.005":0, "0.01":1}
selections = [0.005, 0.01]

dist_to_i = {"0.01":0, "0.02":1}
dist = [0.01, 0.02]

generations_to_i = {"200":0, "500":1}
generations = [200, 500]

sites_to_i = {"3":0,"4":1}
sites = [3,4]





#Creating arrays of lnl
truelnl_diff = [[None]*2,[None]*2]

for i in range(2):
    for j in range(2):
        truelnl_diff[i][j] = [[[],[]],[[],[]]]

falselnl_diff = [[None]*2,[None]*2]

for i in range(2):
    for j in range(2):
        falselnl_diff[i][j] = [[[],[]],[[],[]]]


for line in trueanalysis:
    truelnl_diff[sel_to_i[line[1]]][generations_to_i[line[2]]][dist_to_i[line[3]]][sites_to_i[line[4]]].append(float(line[6]) - float(line[5]))

for line in falseanalysis:
    falselnl_diff[sel_to_i[line[1]]][generations_to_i[line[2]]][dist_to_i[line[3]]][sites_to_i[line[4]]].append(float(line[6]) - float(line[5]))






alt_correct = [[None]*2,[None]*2]
for i in range(2):
    for j in range(2):
        alt_correct[i][j] = [[0,0],[0,0]]

null_correct = [[None]*2,[None]*2]
for i in range(2):
    for j in range(2):
        null_correct[i][j] = [[0,0],[0,0]]


for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                cutoff = 0


                sorted_list = copy.deepcopy(falselnl_diff[i][j][k][l])
                sorted_list.sort()

                cutoff = sorted_list[-2]

                for h in range(20):
                    if truelnl_diff[i][j][k][l][h] > cutoff:
                        alt_correct[i][j][k][l] += 0.05
                    if falselnl_diff[i][j][k][l][h] < cutoff:
                        null_correct[i][j][k][l] += 0.05






fig, axe = plt.subplots(2, 4, figsize=(7, 4), constrained_layout=True, sharex=True, sharey=True)


for i in range(2):
    for j in range(4):
        a, b, c = i , j // 2, j % 2

        ax = axe[i,j]
        ax.set_ylim([0,1.1])
        ax.set_yticks([0,0.25,0.5,0.75,1])
        ax.grid(axis = 'y')

        null_correct_time = [null_correct[a][0][b][c], null_correct[a][1][b][c]]
        alt_correct_time = [alt_correct[a][0][b][c], alt_correct[a][1][b][c]]
        
        ax.set_xticks([0,1])
        ax.set_xlim([-0.5,1.5])
        ax.set_xticklabels(["200","500"])


        #ax.plot([0,1], null_correct_time,color='black', linestyle='-', marker='D', markerfacecolor='none', markersize=3)
        ax.plot([0,1], alt_correct_time,color='black', linestyle='-', marker='s', markersize=5)

        ax.yaxis.set_label_position("right")

        if (i == 0):
            if (j == 0):
                ax.set_title("dist = 0.01\nsites=3")
            if (j == 1):
                ax.set_title("dist = 0.01\nsites=4")
            if (j == 2):
                ax.set_title("dist = 0.02\nsites=3")
            if (j == 3):
                ax.set_title("dist = 0.02\nsites=4")
        if (j == 3):
            ax.set_ylabel("s = "+str(selections[i]))

        
fig.text(0.5, -0, 'Admixture Time (Generations)', ha='center')
fig.text(-0, 0.5, 'Proportion Correct', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(wspace = 0.2, hspace = 0.2)

plt.show()