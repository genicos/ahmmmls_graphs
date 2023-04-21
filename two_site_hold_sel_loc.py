import matplotlib.pyplot as plt

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

# Loading data
trueanalysis = open("data/two_site_hold_selection_true_2_8", "r").readlines()
trueanalysis = trueanalysis[1:]
for i in range(len(trueanalysis)):
    trueanalysis[i] = trueanalysis[i].split("\t")



# Mapping values
m_to_i = {"0.05":0, "0.1":1, "0.2":2, "0.5":3}
m = [0.05,0.1, 0.2, 0.5]

generations_to_i = {"100":0, "200":1, "500":2, "1000":3}
generations = [100, 200, 500, 1000]

dist_to_i = {"0.005":0, "0.01":1, "0.02":2, "0.05":3}
dist = [0.005, 0.01, 0.02, 0.05]





#Creating arrays of location
location_two1 = [[None]*4,[None]*4,[None]*4,[None]*4]
location_two2 = [[None]*4,[None]*4,[None]*4,[None]*4]

for i in range(4):
    for j in range(4):
        location_two1[i][j] = [[],[],[],[]]
        location_two2[i][j] = [[],[],[],[]]


for line in trueanalysis:
    location_two1[dist_to_i[line[3]]][m_to_i[line[2]]][generations_to_i[line[1]]].append(float(line[9]))
    location_two2[dist_to_i[line[3]]][m_to_i[line[2]]][generations_to_i[line[1]]].append(float(line[11]))



#Plotting
fig, axe = plt.subplots(4, 4, constrained_layout=True, sharex=True,sharey=True)


for i in range(4):
    for j in range(4):
        ax = axe[i,j]

        ax.yaxis.set_label_position("right")
        
        ax.scatter(location_two1[i][2][j],location_two2[i][2][j],s=1, color=color_scheme["blue"])


        ax.axhline(0.1 + dist[i]/2,color='black', zorder=0, linewidth=0.5)
        ax.axvline(0.1 - dist[i]/2,color='black', zorder=0, linewidth=0.5)
        

        if (i == 0):
            ax.set_title("t = " + str(generations[j]))
        if (j == 3):
            ax.set_ylabel("dist = "+str(dist[i]))


fig.text(0.5, 0.0, 'Position (Morgans)', ha='center')
fig.text(0.0, 0.5, 'Position (Morgans)', va='center', rotation='vertical')




plt.subplots_adjust(wspace=0.15, hspace=0.15)

plt.tight_layout()
plt.show()
