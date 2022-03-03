#!/usr/bin/python
import sys,os,pprint
import matplotlib.pyplot as plt
import csv
import math
from matplotlib.patches import Ellipse
from itertools import combinations
#from mpl_toolkits.mplot3d import Axes3D

#function print red color text
def red(phrase):
    red = "\x1b[31m"
    none = "\x1b[0m"
    print "%s%s%s" %(red,phrase,none)

#function returns distance between two points
def dis_sq(a,b):
    return math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)

#checks for exactly two system arguments
if len(sys.argv) != 2:
    red("Usage: %s <chosen_folder>" %sys.argv[0])
    exit(0)

#first system argument in the program name, second is name of the folder
folder = sys.argv[1]

if not os.path.exists(folder):
    red("folder %s does not exist" %folder)
    exit(0)

#interates through argument folder for files that end in .dv.log
files = os.listdir(folder)
good_files= []
for item in files:
    if item.endswith(".dv.log"):
        good_files.append(item)

#interates through files for cell coordinates
coord={}
for item in good_files:
    content = open(os.path.join(folder,item),"r").read().splitlines()
    for line in content:
        if "Stage coordinates:" in line:
            a,b=line.split("(")
            c,d,e=b.split(",")
            f,g=e.split(")")
            coord[item]={'x' : float(c), 'y' : float(d), 'z' : float(f),'d' : 0}
            break

xs = []
ys = []
zs = []


#creates arrays of the x,y,z coordinates for each cell, in order
for k in coord.keys():
    xs.append(coord[k]['x'])
    ys.append(coord[k]['y'])
    zs.append(coord[k]['z'])

#searches for top and bottom cell chamber extreme by using maximum distance between two points
max_dis=0
for pair in combinations(coord.values(),2):
    distance=dis_sq(*pair)
    if distance > max_dis:
        max_dis = distance
        max_pair = pair

#ordonate max pair
if max_pair[1]['y']>max_pair[0]['y']:
    max_pair = (max_pair[1],max_pair[0])

#calculates rise, run, slope, and intercept of line between extreme points
rise = max_pair[0]['y']-max_pair[1]['y']
run = max_pair[0]['x']-max_pair[1]['x']

centers_x=[]
centers_y=[]

#calculates first center from top
topx=max_pair[0]['x']
topy=max_pair[0]['y']
disx=500*math.sin(math.atan(run/rise))
disy=500*math.cos(math.atan(run/rise))
xc=topx-disx
yc=topy-disy

#calculates first center from bottom
bottomx=max_pair[1]['x']
bottomy=max_pair[1]['y']
bxc=bottomx+disx
byc=bottomy+disy
centers=[{'x' : xc,'y':yc},{'x' : bxc,'y':byc}]

centers_x.extend((xc,bxc))
centers_y.extend((yc,byc))

#distance between centers
disx=2000*math.sin(math.atan(run/rise))
disy=2000*math.cos(math.atan(run/rise))

nxc=0
nyc=0

#calculates location of next three centers from top center
for i in range(0,3):
    nxc=xc-disx
    nyc=yc-disy
    bnxc=bxc+disx
    bnyc=byc+disy
    centers_x.extend([nxc,bnxc])
    centers_y.extend([nyc,bnyc])
    centers.extend([{'x':nxc,'y':nyc},{'x':bnxc,'y':bnyc}])
    xc=nxc
    yc=nyc
    bxc=bnxc
    byc=bnyc

for k,point in coord.items():
    candidates=[]
    for center in centers:
        cell_dis=dis_sq(point,center)
        candidates.append(cell_dis)
    coord[k]['d']=min(candidates)

#plots centers
plt.plot(centers_y,centers_x,'rs')
ax=plt.gca()
#ax.set_xlim([0,3000])
#ax.set_ylim([-6000,10000])

#plots chamber circles
for i in range(0,len(centers_x)):
    circle = plt.Circle((centers_y[i],centers_x[i]), 500, color='k',fill=False)
    ax.add_artist(circle)

plt.plot(ys,xs,'cs')
plt.plot([max_pair[0]['y'],max_pair[1]['y']],[max_pair[0]['x'],max_pair[1]['x']],marker='o')


"""ellipse = Ellipse((x_mid,y_mid),max(xs)-min(xs),max(ys)-min(ys),edgecolor='y',fc='None',lw=2)
ellipse.set_clip_box(ax.bbox)
ax.add_patch(ellipse)
"""
#writes file name, x,y,z coordinates, and cell distance from chamber to a file name
with open(folder+'.csv','wb') as csvfile:
    data = csv.writer(csvfile,delimiter = ',')
    data.writerow(['File','x','y','z','radius'])
    for k in coord.keys():
        #a=k.split("_")[-2]
        #plt.annotate('%s\n%s'%(a,int((coord[k]['d']))),(coord[k]['x'],coord[k]['y']),va="center", ha="center")
        plt.annotate('%s'%int((coord[k]['d'])),(coord[k]['y'],coord[k]['x']),va="center", ha="center")
        data.writerow([k,coord[k]['x'],coord[k]['y'],coord[k]['z'],coord[k]['d']])
ax.set_title(folder)
ax.set_xlabel('y')
ax.set_ylabel('x')
#ax.set_zlabel('z')
plt.show()
