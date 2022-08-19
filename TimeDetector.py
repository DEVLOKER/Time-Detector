"""
	python program for detecting time based on of analog clock image, created by DevLoker
"""


import cv2
import numpy as np
import math
import sys


def lines(path,  xc, yc):
	img = cv2.imread(path)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,100,200,apertureSize = 3)
	#cv2.imshow('edges',edges)
	#cv2.waitKey(0)
	rng_ = 10
	lines_H_M = []
	# 	10, 30, 10		10, 20, 15
	#lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 20,minLineLength = 30,maxLineGap = 20)
	lines = cv2.HoughLinesP(edges,1,np.pi/180,22,minLineLength=25,maxLineGap=18)
	for x in range(0, len(lines)):
		for x1,y1, x2,y2 in lines[x]:
			#cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
			if(IsPointInRange(x2, y2, xc, yc, rng_)):
				x1 , y1 , x2 , y2 = x2, y2 , x1, y1
			if(IsPointInRange(x1, y1, xc, yc, rng_)):
				exist_similar_line = False
				for i in range(0, len(lines_H_M)):
					lp2x, lp2y = lines_H_M[i][1][0], lines_H_M[i][1][1]
					if(IsPointInRange(x2, y2, lp2x, lp2y, 10)):
						d1 = distance(lines_H_M[i][0], lines_H_M[i][1])
						d2 = distance((x1,y1), (x2,y2))
						if(d2<d1):
							lines_H_M[i] = [(x1,y1), (x2,y2)]
							cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
						exist_similar_line = True
						break
				if(not exist_similar_line and len(lines_H_M)<2):
					cv2.line(img,(x1,y1),(x2,y2),(0,0, 255),1)
					lines_H_M.append( [(x1,y1), (x2,y2)] )


	cv2.circle(img,(xc,yc),rng_,(0,0,255),1)	# draw the outer circle
	cv2.circle(img,(xc,yc),1,(0,0,255),1)		# draw the center of the circle

	cv2.imshow(path,img)

	return lines_H_M


def circleCenter(path):
	img = cv2.imread(path, 0)
	img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=0,maxRadius=0)

	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		return i[0], i[1]

def IsPointInRange(px1, py1, px2, py2, rng_):
	if( px1 in range(px2-rng_, px2+rng_) and py1 in range(py2-rng_, py2+rng_) ):
		return True
	return False

def anglesToHours(a):
	hours = []

	for i in range(1, 13):
		if(i<10):
			hours.append('0'+str(i))
		else:
			hours.append(i)

	angles = []
	for i in range(-180, 180, 30):
		angles.append( (i, i+30) )
	tmp = angles[len(angles)-1]
	angles[len(angles)-1]= (tmp[0], tmp[1]+1)
				
	parts = 4
	splited_list = [angles[(i*len(angles))//parts:((i+1)*len(angles))//parts] for i in range(parts)]	

	angles = splited_list[3]+splited_list[0]+splited_list[1]+splited_list[2]

	for i in range(len(angles)):
			min_, max_ = angles[i][0], angles[i][1]
			if a in range(min_,max_):
				index = i-1
				if a<=0:
					index = i-1
				return hours[index]


def anglesToMinutes(a):

	minutes = []

	for i in range(0, 60):
		if(i<10):
			minutes.append('0'+str(i))
		else:
			minutes.append(i)
		
	angles = []
	for i in range(-180, 180, 6):
		angles.append( (i, i+6) )
	tmp = angles[len(angles)-1]
	angles[len(angles)-1]= (tmp[0], tmp[1]+1)
		
	parts = 4
	splited_list = [angles[(i*len(angles))//parts:((i+1)*len(angles))//parts] for i in range(parts)]	

	angles = splited_list[3]+splited_list[0]+splited_list[1]+splited_list[2]

	for i in range(len(angles)):
			min_, max_ = angles[i][0], angles[i][1]
			if a in range(min_, max_):
				index = i
				return minutes[index]






def distance(p1, p2):
	x1, y1 = p1[0], p1[1]
	x2, y2 = p2[0], p2[1]
	d = math.hypot(x2-x1, y2-y1)
	return d

def angle(p1, p2):
	x1, y1 = p1[0], p1[1]
	x2, y2 = p2[0], p2[1]
	angle = int(np.rad2deg(np.arctan2(y1 - y2, x1 - x2)))
	return angle

#___________________________________________________________
#					Main Program
#___________________________________________________________

if __name__ == '__main__':

	path = 'clock-1.png'
	if(len(sys.argv)==2):
		path = sys.argv[1]

	
	xc, yc = circleCenter(path)
	print("center(%s, %s)"%(xc, yc))
	

	time_ = {"H":"", "M": ""}
	lines_H_M = lines(path, xc, yc)
	if(len(lines_H_M)==2):
		print("Getting Time based on lines : ")
		line1, line2 = lines_H_M[0], lines_H_M[1]
		d1 = distance(line1[0], line1[1])
		d2 = distance(line2[0], line2[1])
		a1 = angle(line1[0], line1[1])
		a2 = angle(line2[0], line2[1])
		print("%s --> angle : %s , distance : %s"%(line1, a1, format(d1,".2f") ))
		print("%s --> angle : %s , distance : %s"%(line2, a2, format(d2,".2f") ))
		if(d1<d2):
			time_["H"] = anglesToHours(a1)
			time_["M"] = anglesToMinutes(a2)
		else:
			time_["H"] = anglesToHours(a2)
			time_["M"] = anglesToMinutes(a1)

		print("Time is %s:%s"% (time_["H"], time_["M"]) )

	else:
		print("impossible to get Time from %s lines (shoud get only two (02) lines)"% (len(lines_H_M)))


	cv2.waitKey(0)
	cv2.destroyAllWindows()