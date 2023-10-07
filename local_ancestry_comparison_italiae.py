import math
import sys
import matplotlib.pyplot as plt 


#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"


#Opening data files
output_file_0 = open("data/la_out_italiae").readlines()
model_la_0 = open("data/model_ancestry_italiae_9_25.tsv").readlines()
del model_la_0[0]
data_la_0 = open("data/data_ancestry_italiae_9_25.tsv").readlines()
del data_la_0[0]

#output_file_1 = open("data/la_out_peak_1").readlines()
#model_la_1 = open("data/model_ancestry_peak_1.tsv").readlines()
#del model_la_1[0]
#data_la_1 = open("data/3r_la").readlines()
#del data_la_1[0]






peaks_Mbp = [
14.180647 ,
18.805566 ,
29.151015 ,
33.565440 ,
41.695798,
62.680556 ,
72.625209 ,
86.815699,
87.850243 ,
101.300767,
103.095764 ,
104.031022 ,
]

peaks_sel = [ 
0.00926148563009,
0.00795269518764,
0.00954791055831,
0.0122384278348,
0.0102752421711,
0.0125334617362,
0.00946636519352,
0.0199817659021,
0.014319627059,
0.00954791055831,
0.0119380732953,
0.0110841191487,
]







#v5_v6_convertion = open("data/3r_v5_v6").readlines()
#v6_coords = []
#for line in v5_v6_convertion:
#    line = line.split()
#    v6_coords.append(float(line[1]))





# Sampling average local ancestry
morgans = []
v6_coords_sampled = []
v6_coords_sampled_million = []

model_traj_0 = []
data_traj_0 = []


sub_sample = 5
i = 0
j = 0
for line in model_la_0:
    line = line.split()
    if i == sub_sample:
        morgans.append(float(line[1]))
        v6_coords_sampled.append(float(line[0]))
        v6_coords_sampled_million.append(float(line[0]) / 1000000)
        model_traj_0.append(float(line[2]))
        i = 0
    i += 1
    j += 1

i = 0
for line in data_la_0:
    line = line.split()
    if i == sub_sample:
        data_traj_0.append(float(line[2]))
        i = 0
    i += 1






#Grabbing model

model_loc_morg_0 = []
model_sel_0 = []
model_line_0 = output_file_0[0].split()
i = 6
while i < len(model_line_0):
    model_loc_morg_0.append(float(model_line_0[i]))
    model_sel_0.append(float(model_line_0[i + 4]))
    i += 6

"""

model_loc_morg_1 = []
model_sel_1 = []
model_line_1 = output_file_1[0].split()
i = 6
while i < len(model_line_1):
    model_loc_morg_1.append(float(model_line_1[i]))
    model_sel_1.append(float(model_line_1[i + 4]))
    i += 6
"""

model_loc_bp_0 = []
model_loc_million_bp_0 = []
for i in range(len(model_loc_morg_0)):
    for j in range(len(morgans)):
        if morgans[j] > model_loc_morg_0[i]:
            model_loc_bp_0.append(v6_coords_sampled[j])
            model_loc_million_bp_0.append(v6_coords_sampled[j] / 1000000)
            break

"""
model_loc_bp_1 = []
model_loc_million_bp_1 = []
for i in range(len(model_loc_morg_1)):
    for j in range(len(morgans)):
        if morgans[j] > model_loc_morg_1[i]:
            model_loc_bp_1.append(v6_coords_sampled[j])
            model_loc_million_bp_1.append(v6_coords_sampled[j] / 1000000)
            break
"""

million_bp_range_0 = [0, 113]
#million_bp_range_1 = [19, 26]



#Taking error or difference between the two
difference_0 = []
#difference_1 = []

for i in range(len(morgans)):
    difference_0.append(data_traj_0[i] - model_traj_0[i])
#for i in range(len(morgans)):
    #difference_1.append(data_traj_1[i] - model_traj_1[i])


diff_bound = 0.5


fig, axe = plt.subplots(3, 1, figsize=(7,5), constrained_layout=True, sharex="col", sharey="row", gridspec_kw={'height_ratios': [2, 5, diff_bound*10]})
fig.align_ylabels(axe[:])


axe[0].scatter(peaks_Mbp, peaks_sel, color=color_scheme["blue"], s=6, marker='*')
axe[0].scatter(peaks_Mbp, peaks_sel, color=color_scheme["blue"], s=6, marker='*')

axe[0].set_xlim(million_bp_range_0)
axe[0].set_ylim([0,0.021])
markerline, stemlines, baseline = axe[0].stem(model_loc_million_bp_0, model_sel_0, bottom=-2)
plt.setp(stemlines, 'color', color_scheme["yellow"])
plt.setp(markerline, 'color', color_scheme["yellow"])
plt.setp(markerline, markersize = 3)
axe[0].set_ylabel("Selection\nCoefficient", fontsize=12)

axe[0].annotate("A", xy=(-0.2, 1.1), xycoords="axes fraction", weight="bold", fontsize=12)

axe[1].set_ylim([0,1])
axe[1].plot(v6_coords_sampled_million, data_traj_0, color=color_scheme["blue"])
axe[1].plot(v6_coords_sampled_million, model_traj_0, color=color_scheme["yellow"])
axe[1].set_ylabel("Average LA\nProportion", fontsize=12)

axe[1].annotate("B", xy=(-0.2, 1.04), xycoords="axes fraction", weight="bold", fontsize=12)

axe[2].set_ylim([-diff_bound,diff_bound])
axe[2].plot(v6_coords_sampled_million, difference_0, color=color_scheme["blue"])
axe[2].axhline(0, ls='--', color=color_scheme["gray"], lw=1)
axe[2].set_ylabel("LA Proportion\nError", fontsize=12)
axe[2].set_xlabel("Position (Mbp)", fontsize=12)

axe[2].annotate("C", xy=(-0.2, 1.05), xycoords="axes fraction", weight="bold", fontsize=12)






plt.tight_layout()
plt.show()
