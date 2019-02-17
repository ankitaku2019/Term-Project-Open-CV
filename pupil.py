#Identify pupils. Based on beta 1
#This file is modified from: 
#https://gist.github.com/edfungus/67c14af0d5afaae5b18c
#Mate IG's post on Nov 2, 2017
import numpy as np
import cv2
import time

newXAvg, newYAvg, oldXAvg, oldYAvg=0, 0, 0, 0
		
def main(): 
	cap = cv2.VideoCapture(0) #640,480
	w = 640
	h = 480
	centerEyeLst=[]
	findEyes(centerEyeLst, cap)

#This entire function was written by me	
def determineChange(centerEyeLst): 
	if (len(centerEyeLst)>=20): 
		coords=centerEyeLst
		#sets up global variables so they can be passed in to the main tkinter
		global newXAvg
		global newYAvg
		global oldXAvg
		global oldYAvg
		#the last five values are being averaged
		length=len(coords)
		for i in range(length-5, length): 
			newXAvg+=coords[i][0]
			newYAvg+=coords[i][1]
		newXAvg=newXAvg/5
		newYAvg=newYAvg/5
		for j in range(length-10, length-5): 
			oldXAvg+=coords[j][0]
			oldYAvg+=coords[j][1]
		oldXAvg=oldXAvg/5
		oldYAvg=oldYAvg/5
		
	else: 
		return None

def findEyes(centerEyeLst, cap): 
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret==True:
			frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
			faces = cv2.CascadeClassifier(r"C:\Users\ankit\Box\Carnegie Mellon University\First Semester Freshman Year\15-112 Fundamentals of Programming\Term Project\xmlFiles\haarcascade_eye.xml")
			detected = faces.detectMultiScale(frame, 1.3, 5)
			pupilFrame = frame
			pupilO = frame
			windowClose = np.ones((5,5),np.uint8)
			windowOpen = np.ones((2,2),np.uint8)
			windowErode = np.ones((2,2),np.uint8)
		
			#draw square
			for (x,y,w,h) in detected:
				cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	
				cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
				cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
				pupilFrame = cv2.equalizeHist(frame[int(y+(h*.25)):(y+h), x:(x+w)])
				pupilO = pupilFrame
				ret, pupilFrame = cv2.threshold(pupilFrame,55,255,cv2.THRESH_BINARY)		#50 ..nothin 70 is better
				pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
				pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
				pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)
		
				#so above we do image processing to get the pupil..
				#now we find the biggest blob and get the centriod
				
				threshold = cv2.inRange(pupilFrame,250,255)		#get the eye "blobs"
				_, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
				
				if len(contours) >= 2:
					#find biggest blob
					maxArea = 0
					MAindex = 0			#to get the unwanted frame 
					distanceX = []		#delete the left most (for right eye)
					currentIndex = 0 
					for cnt in contours:
						area = cv2.contourArea(cnt)
						center = cv2.moments(cnt)
						# cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
						#solves a bug if the center equals 0
						if center['m00'] != 0:
							cx = int(center["m10"] / center["m00"])
							cy = int(center["m01"] / center["m00"])
							centerEyeLst.append([cx, cy])
							
						else:
							cx,cy = 0, 0
						distanceX.append(cx)	
						if area > maxArea:
							maxArea = area
							MAindex = currentIndex
						currentIndex = currentIndex + 1
			
					del contours[MAindex]		#remove the picture frame contour, keeping only the eye
					del distanceX[MAindex]
				
				eye = 'right'
		
		
				if len(contours) >= 1:		#get largest blob
					maxArea = 0
					for cnt in contours:
						area = cv2.contourArea(cnt)
						if area > maxArea:
							maxArea = area
							largeBlob = cnt
						
				if len(largeBlob) > 0:	
					center = cv2.moments(largeBlob)
					cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
					cv2.circle(pupilO,(cx,cy),5,255,-1)
				#determining if there is a significant change
				determineChange(centerEyeLst)
		cv2.imshow('frame',pupilO)
		cv2.imshow('frame2',pupilFrame)
		if cv2.waitKey(1) & 0xFF == ord('q'):break
		#show picture
	
	#else:
		#break
	# Release everything if job is finished
	cap.release()
	cv2.destroyAllWindows()