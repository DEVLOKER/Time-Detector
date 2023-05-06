"""
	python program for detecting time based on of analog clock image, created by DevLoker
"""


import cv2
import numpy as np
import math
import sys, os, time
import json


class TimeDetector(object):
	
	"""         static variables      """
	INPUT_PATH = os.path.join("clocks", "uploaded")
	OUTPUT_PATH = os.path.join("clocks", "processed")
	MINUTES_CLOCKWISE = "minutes"
	HOURS_CLOCKWISE = "hours"

	# def __init__(self):
	# 	pass

	@staticmethod
	def detectTime(clockImage):

		file = os.path.basename(clockImage)
		name, extension = os.path.splitext(file)
		processedImage = name+extension

		result = {
			"srcImage": processedImage, #clockImage,
			"size": os.path.getsize(os.path.join(clockImage)),
			"time": "??:??",
			"processedImage": processedImage,
			"message": None
		}

		# firstly, searching of analog clock center, and drawing circle on it
		xc, yc, img = TimeDetector.drawClockCenter(clockImage)
		if(xc==None or yc==None):
			result["message"] = "can't find clock center"
			return result
		
		cv2.imwrite(os.path.join(TimeDetector.OUTPUT_PATH, processedImage), img)
		result["center"] = [int(xc), int(yc)]
		
		# draw clockwise lines from center of analog clock.
		lines_H_M, img = TimeDetector.drawClockwiseLines(clockImage, xc, yc)
		cv2.imwrite(os.path.join(TimeDetector.OUTPUT_PATH, processedImage), img)

		# must have only two (02) lines (clockwise), one for hours and the second for minutes
		if(len(lines_H_M)!=2):
			result["message"] = "can't detect clockwise (should get 02 lines)"
			return result
	
		time_ = {}			
		line1, line2 = lines_H_M[0], lines_H_M[1]

		# calculate the length of each clockwise
		d1 = TimeDetector.distance(line1[0], line1[1])
		d2 = TimeDetector.distance(line2[0], line2[1])
		# calculate angle of each clockwise
		a1 = TimeDetector.angle(line1[0], line1[1])
		a2 = TimeDetector.angle(line2[0], line2[1])

		# the shortest clockwise for hours, and the longest one for minutes
		if(d1<d2):
			# based of clockwise angles, we can calculate time
			time_[TimeDetector.HOURS_CLOCKWISE] = TimeDetector.anglesToHours(a1)
			time_[TimeDetector.MINUTES_CLOCKWISE] = TimeDetector.anglesToMinutes(a2)
		else:
			time_[TimeDetector.HOURS_CLOCKWISE] = TimeDetector.anglesToHours(a2)
			time_[TimeDetector.MINUTES_CLOCKWISE] = TimeDetector.anglesToMinutes(a1)
		
		result["clockwise"] = [
				{
					"type": TimeDetector.MINUTES_CLOCKWISE,
					"line": {"start": {"x": int(line1[0][0]), "y": int(line1[0][1])}, "end": {"x": int(line1[1][0]), "y": int(line1[1][1])}},
					"angle": a1,
					"distance": format(d1,".2f")
				},
				{
					"type": TimeDetector.HOURS_CLOCKWISE,
					"line": {"start": {"x": int(line2[0][0]), "y": int(line2[0][1])}, "end": {"x": int(line2[1][0]), "y": int(line2[1][1])}},
					"angle": a2,
					"distance": format(d2,".2f")
				}
			]
		result["time"] = str(time_[TimeDetector.HOURS_CLOCKWISE])+":"+str(time_[TimeDetector.MINUTES_CLOCKWISE])
		
		return result
	

	@staticmethod
	def drawClockwiseLines(clockImage,  xc, yc):
		img = cv2.imread(clockImage)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,100,200,apertureSize = 3)
		#cv2.imshow('edges',edges)
		#cv2.waitKey(0)
		rng_ = 10
		lines_H_M = []
		clr, thickness = (25, 255, 84), 4 #(25, 135, 84), 2 #(0,0,255), 4
		# 	10, 30, 10		10, 20, 15
		#lines = cv2.HoughLinesP(edges,rho = 1,theta = 1*np.pi/180,threshold = 20,minLineLength = 30,maxLineGap = 20)
		lines = cv2.HoughLinesP(edges,1,np.pi/180,22,minLineLength=25,maxLineGap=18)
		for x in range(0, len(lines)):
			for x1,y1, x2,y2 in lines[x]:
				#cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
				if(TimeDetector.IsPointInRange(x2, y2, xc, yc, rng_)):
					x1 , y1 , x2 , y2 = x2, y2 , x1, y1
				if(TimeDetector.IsPointInRange(x1, y1, xc, yc, rng_)):
					exist_similar_line = False
					for i in range(0, len(lines_H_M)):
						lp2x, lp2y = lines_H_M[i][1][0], lines_H_M[i][1][1]
						if(TimeDetector.IsPointInRange(x2, y2, lp2x, lp2y, 10)):
							d1 = TimeDetector.distance(lines_H_M[i][0], lines_H_M[i][1])
							d2 = TimeDetector.distance((x1,y1), (x2,y2))
							if(d2<d1):
								lines_H_M[i] = [(x1,y1), (x2,y2)]
								cv2.line(img,(x1,y1),(x2,y2),clr, thickness)
							exist_similar_line = True
							break
					if(not exist_similar_line and len(lines_H_M)<2):
						cv2.line(img,(x1,y1),(x2,y2),clr, thickness)
						lines_H_M.append( [(x1,y1), (x2,y2)] )


		cv2.circle(img,(xc,yc),rng_,clr, thickness)	# draw the outer circle
		cv2.circle(img,(xc,yc),1,clr, 1)		# draw the center of the circle

		return lines_H_M, img

	@staticmethod
	def drawClockCenter(clockImage):
		img = cv2.imread(clockImage, 0)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=0,maxRadius=0)
		print(np.any(circles)==None)
		# if(type(circles)=="<class 'NoneType'>"):
		if(np.any(circles)==None):
			return None, None, img
		
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			return i[0], i[1] , img


	@staticmethod
	def IsPointInRange(px1, py1, px2, py2, rng_):
		if( px1 in range(px2-rng_, px2+rng_) and py1 in range(py2-rng_, py2+rng_) ):
			return True
		return False

	@staticmethod
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

	@staticmethod
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

	@staticmethod
	def distance(p1, p2):
		x1, y1 = p1[0], p1[1]
		x2, y2 = p2[0], p2[1]
		d = math.hypot(x2-x1, y2-y1)
		return d

	@staticmethod
	def angle(p1, p2):
		x1, y1 = p1[0], p1[1]
		x2, y2 = p2[0], p2[1]
		angle = int(np.rad2deg(np.arctan2(y1 - y2, x1 - x2)))
		return angle


#___________________________________________________________
#					Main Program
#___________________________________________________________


def __get_files(path):
    files = []
    name_list = os.listdir(path)
    full_list = [os.path.join(path,i) for i in name_list]
    time_sorted_list = sorted(full_list, key=os.path.getmtime)
    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]
    sorted_filename_list.reverse()
    
    for filename in sorted_filename_list:
        sz = os.path.getsize(os.path.join(path, filename))
        files.append({"name":filename, "size": sz, "path": os.path.join(path) })
	
    return files

def __cleanDirectory(dir):
    now = time.time()
    timer = 0# 730 * 86400 # 60 minutes : 60 * 60      30 days : 30 * 86400
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.getmtime(path) < now - timer:
            if os.path.isfile(path):
                os.remove(path)


if __name__ == '__main__':

	__cleanDirectory(os.path.join(TimeDetector.OUTPUT_PATH))

	files = __get_files(os.path.join(TimeDetector.INPUT_PATH))
	for file in files:
		name, size, path = file.values()
		clockImage = os.path.join(path, name)

		result = TimeDetector.detectTime(clockImage)
		if result["message"] != None:
			print(result["message"])
		else:
			print( json.dumps(result, indent=4) )
			# print( result["time"] )
