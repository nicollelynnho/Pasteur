#!/usr/bin/python2.7
import sys,time,math, traceback, os.path, csv
from PIL import Image
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
#red text in terminal
def red(phrase):
    red = "\x1b[31m"
    none = "\x1b[0m"
    print "%s%s%s" %(red,phrase,none)

#checks if there are three arguments
if len(sys.argv)!=5 :
    red("Usage : %s <Directory> <First Image> <Last Image> <Interval Minutes>"%sys.argv[0])
    exit(0)

#checks if second and third argument are start and end images
try:
    int(sys.argv[2])
    int(sys.argv[3])
    interval = int(sys.argv[4])
except:
    red("Usage : %s <Directory> <First Image> <Last Image> <Interval Minutes>"%sys.argv[0])
    exit(0)

#checks to see if folder exists
folder = sys.argv[1]

if not os.path.exists(folder):
    red("folder %s does not exist" %folder)
    exit(0)

files = os.listdir(folder)
good_files= []
for item in files:
    if item.endswith(".tif"):
        good_files.append(item)

# activate bug mode to display computer generated images
DEBUG = False
#DEBUG = True

# DO WE SAVE THE PROCESSED IMAGE
SAVE = False #True

NEIGHBOR = 1

#ratio red to green image
RED_GREEN_COEF = 13

def processimage(image_path):
    #open image
    im = Image.open(open(image_path,'rb'))

# checking neighboring pixels
def neighbor(img,x,y):
    sum_ = 0
    for i in range(-NEIGHBOR,NEIGHBOR+1):
        for j in range(-NEIGHBOR,NEIGHBOR+1):
          sum_ += img[x+i,y+j]
    return (sum_/((NEIGHBOR*2+1)**2))


LIMIT_BEGINNING = int(sys.argv[2])
LIMIT_END = int(sys.argv[3])
#main infinite loop
new_folder = folder+'_output'
try:
    os.makedirs(new_folder)
except:
    pass

with open(os.path.join(new_folder,'general.csv'),'wb') as csvfile:
    data = csv.writer(csvfile,delimiter = ';')
    data.writerow(['tif','growth rate','doubling time','r^2'])

for item in good_files:
	nb_images = 0
	ys=[]
	processed_images=[]
	im = Image.open(os.path.join(sys.argv[1],item))
        average=0
	try:
	    while (nb_images < LIMIT_END) :
	      #red photo
	      im.seek(nb_images*3)
	      red_im = im.copy()
	      red_im_modif = im.copy()
	      im.seek(nb_images*3+1)
	      green_im = im.copy()
	      pix_red = red_im.load()
	      pix_red_modif = red_im_modif.load()
	      pix_green = green_im.load()
	      (x_m, y_m) = im.size
	      good = 0

	      for x in range(x_m):
                 for y in range(y_m):
		   pix_red_modif[x,y]=-pix_green[x,y]+pix_red[x,y]/RED_GREEN_COEF
                   if x < x_m/4 and nb_images==0:
                     average += pix_red_modif[x,y]
              if nb_images==0:
                average = average/((x_m/4)*y_m)
              print "AVERAGE: ",average
	      for x in range(NEIGHBOR,x_m-NEIGHBOR,1):
                 for y in range(NEIGHBOR,y_m-NEIGHBOR,1):
		   #black and white photos
		   if(neighbor(pix_red_modif,x,y)>average*170):
		      pix_red[x,y]=65535
		      good += 1
		   else:
		      pix_red[x,y]=0
	      tim = red_im_modif

	      ys.append(float(good))
	      nb_images += 1
	      print "Image %3d | number of pixels %6d "%(nb_images, good)
	      if DEBUG:
	  	red_im_modif.show()
	  	green_im.show()
	  	red_im.show()
		#time.sleep(50)
	      if SAVE:
		processed.append(om)
	except Exception as e:
	    traceback.print_exc(file=sys.stdout)
	    print e
	    print nb_images

	if SAVE:
	  processed[0].save("processed.tif",compression="tiff_deflate", tiffinfo={"315":"Nicolle Ho"}, save_all=True,append_images=processed[1:])

	coef_area = 66.87/1024#66.87**2/1024**2
	coef_time = 1
	def f(x,a,b):
	  return a*np.exp(b*x)

	x = np.array(range((LIMIT_END-LIMIT_BEGINNING)))
	y = np.array(ys[LIMIT_BEGINNING:LIMIT_END])
	print x,y
	interval = 0
	for value in y:
	    if value > 2*y[0]:
                break
            interval += 1
        doubling_time = interval*int(sys.argv[4])
	print "doubling time :%s mins"%doubling_time
	popt, pcov = curve_fit(f, x, y)
	calculated, = plt.plot(x, y, 'ro', label='from the video %s'%sys.argv[1])
	fitted, = plt.plot([i+LIMIT_BEGINNING for i in x], [f(y, *popt) for y in x], 'bo', label='%s+%s*EXP(%s*x)'%(0, round(popt[0]), round(popt[1],3)))
	plt.legend(handles=[fitted, calculated])

	print "GROWTH RATE FOUND : %3f"%(popt[1]*coef_area)

        if SAVE:
	    processed_images[0].save(item.replace(".tif","_copy.tif"),compression="tiff_deflate",save_all=True,append_images=processed_images[1:])


	with open(os.path.join(new_folder,'general.csv'),'a+') as csvfile:
	    data = csv.writer(csvfile,delimiter = ';')
	    data.writerow([item,popt[1],doubling_time,"WIP"])
