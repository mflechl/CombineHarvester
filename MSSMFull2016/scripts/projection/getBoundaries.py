import json
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

def round_to_2(x):
    return round(x, -int(-1+floor(log10(abs(x)))))

json_name = "input/mssm_ggH_bbH_2D_boundaries_both.json"
boundaries = json.load(open(json_name))

masses =  ["90", "100", "110","120", "125", "130", "140", "160", "180", "200", "250", "350", "400", "450", "500", "600", "700", "800", "900","1000","1200","1400","1600","1800","2000","2300","2600","2900","3200"]
#masses = [ "700" ]

ggh_factor = [0.1195, 0.1232, 0.1307, 0.131, 0.1302, 0.1267, 0.1264, 0.13, 0.1307, 0.1426, 0.1356, 0.1331, 0.1297, 0.1257, 0.1222, 0.1207, 0.1241, 0.1241, 0.1229, 0.1107, 0.1025, 0.0971, 0.0936, 0.0894, 0.0882, 0.0866, 0.0851, 0.0845]
bbh_factor = [0.1196, 0.1237, 0.1348, 0.1421, 0.152, 0.1507, 0.1458, 0.1427, 0.1448, 0.1512, 0.1328, 0.1245, 0.1157, 0.1126, 0.1039, 0.0928, 0.091, 0.089, 0.0803, 0.0751, 0.0766, 0.0745, 0.0769, 0.0758, 0.0752, 0.0766, 0.0755, 0.0741]

new_g={}
new_b={}
#for mass in masses:
for mass,g,b in zip(masses,ggh_factor,bbh_factor):
    r_ggH_bounds, r_bbH_bounds = boundaries["r_ggH"][str(float(mass))],boundaries["r_bbH"][str(float(mass))]
    print mass,r_ggH_bounds[1],r_bbH_bounds[1],'           ',r_ggH_bounds[1]*g,r_bbH_bounds[1]*b,'           ',round_to_2(r_ggH_bounds[1]*g),round_to_2(r_bbH_bounds[1]*b)
    new_g[mass]=[ 0, round_to_2(r_ggH_bounds[1]*g*1.2) ]
    new_b[mass]=[ 0, round_to_2(r_bbH_bounds[1]*b*1.2) ]

data = { 'r_ggH'    : new_g, 'r_bbH'    : new_b }

with open('mssm_ggH_bbH_2D_boundaries_both_3000fb.json', 'w') as outfile:
    json.dump(data, outfile, indent=2, sort_keys=True)
    outfile.close
