import matplotlib.pyplot as plt

#parameters
site_cutoff = 150
lnl_cuttoff = 40

#Loading colors
color_file = open("color_scheme").readlines()
color_scheme = {}
for line in color_file:
    line = line.split()
    color_scheme[line[0]] = line[1]

plt.rcParams["font.family"] = "Arial"



#loading data
#morgan_convertion = open("data/passer_bp_morg").readlines()
ahmms_out = open("data/ahmms_gss_italiae").readlines()



bp_coords = []
coords_million = []
lnl_ratio = []
sel_coeff = []


for line in ahmms_out:
    line = line.split()
    bp_coords.append(float(line[0]))
    lnl_ratio.append(float(line[2]))
    sel_coeff.append(float(line[1]))



sites_loc = []
sites_lnl = []
sites_sel = []



for i in range(len(bp_coords)):
    coords_million.append(bp_coords[i] / 1000000)
    peak = True

    if lnl_ratio[i] < lnl_cuttoff:
        continue


    
    j = i - 1
    while j >= 0 and i - j <= site_cutoff: 
        if lnl_ratio[j] >= lnl_ratio[i]:
            peak = False
        j -= 1

    j = i + 1
    while j < len(bp_coords) and j - i <= site_cutoff: 
        if lnl_ratio[j] >= lnl_ratio[i]:
            peak = False
        j += 1
    
    if peak:
        sites_loc.append(bp_coords[i])
        sites_lnl.append(lnl_ratio[i])
        sites_sel.append(sel_coeff[i])


 


peaks = list(zip(sites_loc, sites_lnl))





sites_loc_million = []
for i in range(len(sites_loc)):
    sites_loc_million.append(sites_loc[i] / 1000000)


plt.figure(figsize=(6, 2))

plt.xlabel('Position (Mbp)')
plt.ylabel('Lnl Ratio')


plt.scatter(sites_loc_million, sites_lnl, color=color_scheme["yellow"], s=20)
plt.plot(coords_million,lnl_ratio, color=color_scheme["blue"])
plt.yticks([0, 50, 100,150])

plt.tight_layout()

plt.show()