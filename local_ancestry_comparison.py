import math
import sys
import matplotlib.pyplot as plt 


#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]


#Opening data files
output_file_0 = open("data/la_out_peak_0").readlines()
model_la_0 = open("data/model_ancestry_peak_0.tsv").readlines()
del model_la_0[0]
data_la_0 = open("data/3r_la").readlines()
del data_la_0[0]

output_file_1 = open("data/la_out_peak_1").readlines()
model_la_1 = open("data/model_ancestry_peak_1.tsv").readlines()
del model_la_1[0]
data_la_1 = open("data/3r_la").readlines()
del data_la_1[0]





v5_v6_convertion = open("data/3r_v5_v6").readlines()
v6_coords = []
for line in v5_v6_convertion:
    line = line.split()
    v6_coords.append(float(line[1]))





# Sampling average local ancestry
morgans = []
v6_coords_sampled = []
v6_coords_sampled_million = []

model_traj_0 = []
data_traj_0 = []
model_traj_1 = []
data_traj_1 = []

sub_sample = 5
i = 0
j = 0
for line in model_la_0:
    line = line.split()
    if i == sub_sample:
        morgans.append(float(line[1]))
        v6_coords_sampled.append(v6_coords[j])
        v6_coords_sampled_million.append(v6_coords[j] / 1000000)
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


i = 0
for line in model_la_1:
    line = line.split()
    if i == sub_sample:
        model_traj_1.append(float(line[2]))
        i = 0
    i += 1

i = 0
for line in data_la_1:
    line = line.split()
    if i == sub_sample:
        data_traj_1.append(float(line[2]))
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

model_loc_morg_1 = []
model_sel_1 = []
model_line_1 = output_file_1[0].split()
i = 6
while i < len(model_line_1):
    model_loc_morg_1.append(float(model_line_1[i]))
    model_sel_1.append(float(model_line_1[i + 4]))
    i += 6


model_loc_bp_0 = []
model_loc_million_bp_0 = []
for i in range(len(model_loc_morg_0)):
    for j in range(len(morgans)):
        if morgans[j] > model_loc_morg_0[i]:
            model_loc_bp_0.append(v6_coords_sampled[j])
            model_loc_million_bp_0.append(v6_coords_sampled[j] / 1000000)
            break

model_loc_bp_1 = []
model_loc_million_bp_1 = []
for i in range(len(model_loc_morg_1)):
    for j in range(len(morgans)):
        if morgans[j] > model_loc_morg_1[i]:
            model_loc_bp_1.append(v6_coords_sampled[j])
            model_loc_million_bp_1.append(v6_coords_sampled[j] / 1000000)
            break


million_bp_range_0 = [8, 19]
million_bp_range_1 = [19, 26]



#Taking error or difference between the two
difference_0 = []
difference_1 = []

for i in range(len(morgans)):
    difference_0.append(data_traj_0[i] - model_traj_0[i])
for i in range(len(morgans)):
    difference_1.append(data_traj_1[i] - model_traj_1[i])


diff_bound = 0.4


fig, axe = plt.subplots(3, 2, figsize=(7,5), constrained_layout=True, sharex="col", sharey="row", gridspec_kw={'height_ratios': [2, 5, diff_bound*10]})
fig.align_ylabels(axe[:])



axe[0][0].set_xlim(million_bp_range_0)
axe[0][0].set_ylim([0,0.011])
markerline, stemlines, baseline = axe[0][0].stem(model_loc_million_bp_0, model_sel_0, bottom=-2)
plt.setp(stemlines, 'color', color_scheme["yellow"])
plt.setp(markerline, 'color', color_scheme["yellow"])
plt.setp(markerline, markersize = 3)
axe[0][0].set_ylabel("Selection\nCoefficient", fontsize=12)

axe[1][0].set_ylim([0,1])
axe[1][0].plot(v6_coords_sampled_million, data_traj_0, color=color_scheme["blue"])
axe[1][0].plot(v6_coords_sampled_million, model_traj_0, color=color_scheme["yellow"])
axe[1][0].set_ylabel("Average LA\nProportion", fontsize=12)

axe[2][0].set_ylim([-diff_bound,diff_bound])
axe[2][0].plot(v6_coords_sampled_million, difference_0, color=color_scheme["blue"])
axe[2][0].axhline(0, ls='--', color=color_scheme["gray"], lw=1)
axe[2][0].set_ylabel("LA Proportion\nError", fontsize=12)
axe[2][0].set_xlabel("Position (Mbp)", fontsize=12)



axe[0][1].set_xlim(million_bp_range_1)
axe[0][1].set_ylim([0,0.011])
markerline, stemlines, baseline = axe[0][1].stem(model_loc_million_bp_1, model_sel_1, bottom=-2)
plt.setp(stemlines, 'color', color_scheme["yellow"])
plt.setp(markerline, 'color', color_scheme["yellow"])
plt.setp(markerline, markersize = 3)

axe[1][1].set_ylim([0,1])
axe[1][1].plot(v6_coords_sampled_million, data_traj_1, color=color_scheme["blue"])
axe[1][1].plot(v6_coords_sampled_million, model_traj_1, color=color_scheme["yellow"])

axe[2][1].set_ylim([-diff_bound,diff_bound])
axe[2][1].plot(v6_coords_sampled_million, difference_1, color=color_scheme["blue"])
axe[2][1].axhline(0, ls='--', color=color_scheme["gray"], lw=1)
axe[2][1].set_xlabel("Position (Mbp)", fontsize=12)

plt.tight_layout()
plt.show()
