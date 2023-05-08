import matplotlib.pyplot as plt

#parameters
site_cutoff = 700
lnl_cuttoff = 15

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"

#loading data
v5_v6_convertion = open("data/3r_v5_v6").readlines()
morgan_convertion = open("data/3r_v5_morg").readlines()
ahmms_out = open("data/ahmms_gss_3r_2_10").readlines()



v5_coords = []
morg_coords = []
coords = []
coords_million = []
lnl_ratio = []
sel_coeff = []

i = 0
j = 0
for line in ahmms_out:
    line = line.split()
    while v5_v6_convertion[i].split()[0] != line[0]:
        i += 1
    coords.append(float(v5_v6_convertion[i].split()[1]))
    v5_coords.append(float(line[0]))
    morg_coords.append(float(morgan_convertion[j].split()[1]))
    lnl_ratio.append(float(line[2]))
    sel_coeff.append(float(line[1]))
    j +=1



sites_loc_v6 = []
sites_loc_v5 = []
sites_loc_morgan = []
sites_lnl = []
sites_sel = []



for i in range(len(coords)):
    coords_million.append(coords[i] / 1000000)
    peak = True

    if lnl_ratio[i] < lnl_cuttoff:
        continue


    
    j = i - 1
    while j >= 0 and i - j <= site_cutoff: 
        if lnl_ratio[j] >= lnl_ratio[i]:
            peak = False
        j -= 1

    j = i + 1
    while j < len(coords) and j - i <= site_cutoff: 
        if lnl_ratio[j] >= lnl_ratio[i]:
            peak = False
        j += 1
    
    if peak:
        sites_loc_v6.append(coords[i])
        sites_loc_v5.append(v5_coords[i])
        sites_loc_morgan.append(morg_coords[i])
        sites_lnl.append(lnl_ratio[i])
        sites_sel.append(sel_coeff[i])





peaks = list(zip(sites_loc_morgan, sites_lnl))



#Sorting peaks by lnl
def Sort_Tuple(tup):
 
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):
        
        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

peaks = Sort_Tuple(peaks)
peaks.reverse()


print("Morgans\tlnL ratio")
for i in range(len(peaks)):
    print(peaks[i][0], peaks[i][1],sep='\t')



sites_loc_million = []
for i in range(len(sites_loc_v6)):
    sites_loc_million.append(sites_loc_v6[i] / 1000000)


plt.figure(figsize=(6, 2))

plt.xlabel('Position (Mbp)')
plt.ylabel('Lnl Ratio')


plt.scatter(sites_loc_million, sites_lnl, color=color_scheme["yellow"], s=20)
plt.plot(coords_million,lnl_ratio, color=color_scheme["blue"])

plt.tight_layout()

plt.show()