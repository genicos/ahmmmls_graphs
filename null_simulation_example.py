import matplotlib.pyplot as plt

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
	line = line.split()
	color_scheme[line[0]] = line[1]


plt.rcParams["font.family"] = "Arial"

# Loading data
subsampling = 100

morgans  = []
model_la = []
for i in range(5):
	model_la.append([])

	with open("data/model_ancestry_test"+str(i)+".tsv") as model_file:
		model_file = model_file.readlines()
		model_file = model_file[1:]
		j = 0
		for line in model_file:
			if j % subsampling == 0:
				line = line.split()
				if i == 0:
					morgans.append(float(line[1]))
				model_la[i].append(float(line[2]))
			j += 1


data_la = []
for i in range(5):
	data_la.append([])

	with open("data/data_ancestry_test"+str(i)+".tsv") as data_file:
		data_file = data_file.readlines()
		data_file = data_file[1:]
		j = 0
		for line in data_file:
			if j % subsampling == 0:
				line = line.split()
				data_la[i].append(float(line[2]))
			j += 1


lnl = [0] * 5

lnl[0] = -152647175.456766
lnl[1] = -152646771.113338
lnl[2] = -152646589.027148
lnl[3] = -152646326.16351
lnl[4] = -152646316.644291



null_dist = []
null_dist.append([
1.2578980028629303,
2.9931219816207886,
4.0195159912109375,
7.868909001350403,
7.990144997835159,
8.926688015460968,
9.863739997148514,
12.186973005533218,
12.222694993019104,
14.489106982946396,
16.6664380133152,
17.631489992141724,
18.01274099946022,
18.565716981887817,
22.63018500804901,
23.075765997171402,
27.192236989736557,
44.705626010894775,
50.223785012960434,
75.12630200386047,
])
null_dist.append([
-0.011908024549484253,
0.32634198665618896,
0.5764769911766052,
0.6476309895515442,
0.7603690028190613,
1.8664079904556274,
2.7328470051288605,
2.7664609849452972,
2.9963789880275726,
5.120691001415253,
11.136411994695663,
11.608801007270813,
12.531442999839783,
12.672453999519348,
18.535371989011765,
19.187702983617783,
27.69853201508522,
34.769315004348755,
38.78727099299431,
57.82872799038887,
])
null_dist.append([
0.9591610133647919,
1.1702959835529327,
2.3790929913520813,
3.258553981781006,
4.144927024841309,
4.526528000831604,
4.688356995582581,
5.055670976638794,
10.252855002880096,
16.42028099298477,
21.33924800157547,
22.1618410050869,
26.03378102183342,
28.219074010849,
30.756999999284744,
30.809381008148193,
31.268456012010574,
36.980183988809586,
38.55277398228645,
56.66627299785614,
])
null_dist.append([
-0.022918015718460083,
0.679548978805542,
3.85139200091362,
4.5731439888477325,
6.074968993663788,
6.201779007911682,
7.490948021411896,
7.7113839983940125,
10.410336017608643,
11.162889987230301,
12.211006999015808,
12.449205994606018,
18.1076700091362,
23.425929009914398,
24.06870698928833,
29.22493401169777,
41.25058001279831,
45.71944499015808,
49.284274995326996,
60.25060999393463,
])

for i in range(4):
	null_dist[i].sort()


morgan_cutoff = 0.25
cutoff_index = 0
for i in range(len(morgans)):
	if morgans[i] > morgan_cutoff:
		cutoff_index = i
		break

morgans = morgans[:cutoff_index]
for i in range(5):
	data_la[i] = data_la[i][:cutoff_index]
	model_la[i] = model_la[i][:cutoff_index]

fig, axe = plt.subplots(4, 2, constrained_layout=True, width_ratios=[5,1], sharex='col')

flierprops = dict(markersize=2)
medianprops = dict(color='black')

for i in range(4):
	axe[i][0].set_ylim([0,1])

	axe[i][0].axvline(0.1, color=color_scheme["gray"])
	if i > 0:
		axe[i][0].axvline(0.2, color=color_scheme["gray"])
	if i > 1:
		axe[i][0].axvline(0.12, color=color_scheme["gray"])
	if i > 2:
		axe[i][0].axvline(0.179, color=color_scheme["gray"])

	axe[i][0].plot(morgans,data_la[i], c = "black")
	axe[i][0].plot(morgans,model_la[i+1], c = color_scheme["blue"], linestyle='--')
	axe[i][0].plot(morgans,model_la[i], c = color_scheme["orange"], linestyle='--')
	axe[i][0].set_xticklabels(["0","0","5","10","15","20","25"])

	axe[i][0].text(y = 0.5, x = 0.05, s = "lnL ratio:\n"+str(round(lnl[i+1] - lnl[i],2)), horizontalalignment='center')

	cutoff = round(null_dist[i][-2], 2)

	
	axe[i][1].boxplot(null_dist[i], vert=False, flierprops=flierprops, medianprops=medianprops)
	axe[i][1].axvline(cutoff, color = "black")
	axe[i][1].axvline(lnl[i+1] - lnl[i], color = color_scheme["blue"])
	print(lnl[i+1] - lnl[i])

	axe[i][1].set_yticks([])
	axe[i][1].set_xlim([0,420])

	axe[i][1].yaxis.set_label_position("right")
	axe[i][1].set_ylabel("95% cutoff:\n"+str(cutoff))

axe[0][1].set_title("Null Model\nDistribution")


axe[3][0].text(morgan_cutoff/2, -0.5, 'Position (Mbp)', horizontalalignment='center')

axe[3][1].text(210, -0.0, 'lnL ratio', horizontalalignment='center')

fig.text(-0, 0.5, 'Local Ancestry Proportion', va='center', rotation='vertical')

plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.2)

plt.show()