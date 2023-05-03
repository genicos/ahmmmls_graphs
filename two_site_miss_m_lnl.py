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
trueanalysis = open("data/two_site_miss_m_true_3_8", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")

falseanalysis = open("data/two_site_miss_m_false_3_8", "r").readlines()
falseanalysis = falseanalysis[1:]
for i in range(len(falseanalysis)):
    falseanalysis[i] = falseanalysis[i].split("\t")



# Mapping values
missf_to_i = {"0.5":0, "0.8":1, "1.2":2, "2":3}
missf = [0.5 , 0.8, 1.2, 2]


m_to_i = {'0.05':0,'0.1':1,'0.2':2,'0.4':3}
m = [0.05, 0.1, 0.2, 0.4]







#Creating arrays of lnl
truelnl_diff = [None]*4

for i in range(4):
    truelnl_diff[i] = [[],[],[],[]]

falselnl_diff = [None]*4

for i in range(4):
    falselnl_diff[i] = [[],[],[],[]]


for line in trueanalysis:
    truelnl_diff[m_to_i[line[1]]][missf_to_i[line[2]]].append(float(line[6]) - float(line[3]))

for line in falseanalysis:
    falselnl_diff[m_to_i[line[1]]][missf_to_i[line[2]]].append(float(line[6]) - float(line[3]))




alt_correct = [None]*4
for i in range(4):
    alt_correct[i] = [0,0,0,0]

null_correct = [None]*4
for i in range(4):
    null_correct[i] = [0,0,0,0]

for i in range(4):
    for j in range(4):
        cutoff = 0

        sorted_list = copy.deepcopy(falselnl_diff[i][j])
        sorted_list.sort()

        cutoff = sorted_list[-2]

        for h in range(20):
            if truelnl_diff[i][j][h] > cutoff:
                alt_correct[i][j] += 0.05
            if falselnl_diff[i][j][h] < cutoff:
                null_correct[i][j] += 0.05







fig, axe = plt.subplots(1, 4, figsize=(7, 2.5),constrained_layout=True, sharex=False, sharey=True)



x = [1,2,3,4]
xlabels = ["0.5","0.8","1.2","2"]




for i in range(4):
    ax = axe[i]
    ax.set_ylim([0,1.1])
    ax.set_yticks([0,0.25,0.5,0.75,1])
    ax.grid(axis = 'y')
    ax.set_xticks([1,2,3,4])

    ax.plot(x, alt_correct[i] ,color='black', linestyle='-', marker='s', markersize=5)
    
    xlabels = missf.copy()
    for j in range(len(xlabels)):
        xlabels[j] *= m[i]
        xlabels[j] = round(float(xlabels[j]),3)
    
    ax.set_xticklabels(xlabels)
    ax.yaxis.set_label_position("right")

    
    ax.set_title("m = " + str(m[i]))




fig.text(0.5, 0.015, 'Misspecified Admixture Fraction', ha='center')
fig.text(0.01, 0.5, 'Proportion Correct', va='center', rotation='vertical')


plt.tight_layout()
plt.subplots_adjust(bottom=0.2, left=0.1, top=0.8, right=0.9, wspace=0.2)

plt.show()