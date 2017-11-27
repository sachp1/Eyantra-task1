#E yantra Robitics Competetion task 1A
# team #3416
#SET 2
import cv2
import numpy as np 
class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c):
		shape = "Shape Not Detected"					  #if the shape is not detected then 'shape not detected ' is returned
		per = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * per, True)
		if len(approx) == 3:
			shape = "triangle"							  # if shape is triangle, it will have 3 vertices

		elif len(approx) == 4:                            # when vertices =4 it can be a square or a rectangle
			(x, y, wi, h) = cv2.boundingRect(approx)
			ar = wi / float(h)
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle" #when aspect ration ~ 1 it is a square

		elif len(approx) == 5:							 #when vertices is 5 ,it is a pentagon
			shape = "pentagon"

		else:
			shape = "circle"              #if approx is any other value then it is a circle
		return shape                      #returns the value of shape

class shaperecognition():												#A class is declared
	def __init__(self, img):
		 self.img= img

	def preprocessing(self):                                            #the Fucntion preprocessing is declared                              
		lower=np.array([100,100,100],dtype=np.uint16)
		upper=np.array([255,255,255],dtype=np.uint16)		
		mask=cv2.inRange(self.img,lower,upper)									#Masks the BGR image between the values lower and upper 
		#blurred=cv2.medianBlur(mask,5)
		tres=cv2.threshold(mask,100,255,cv2.THRESH_BINARY)[1]						#apply threshold
		invmask=cv2.bitwise_not(tres)												#the mask is inverted
		cont=cv2.findContours(invmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)	
		cv2.imshow("thresholder",tres)												#the thresholded image is shown	
		cont = cont[1] 
		sd=ShapeDetector()															#the class Shape Detector is called
		for c in cont:																#the moments are found
			M=cv2.moments(c)
			if(M["m00"]==0):										
				break													#The fuction breaks if divide by zero condition occurs
			cval=''													    #the value for color is intitally a blank space
			cx=int((M["m10"]/M["m00"]))
			cy=int((M["m01"]/M["m00"]))
			shape=sd.detect(c)								#the shape of each contour is returned by the function detect inside the class ShapeDetector
			col=hsv[cy][cx][0]								#the hue value of each contour is given to the function col

			if((col>=0)&(col<43)):
				cval="red "
			elif((col>=43)&(col<128)):						#The H values of (H,S,V) are checked to find out the color
				cval="green "
			elif((col>=128)&(col<213)):
				cval="blue "
			sshape=cval+shape
			c = c.astype("float")
			c = c.astype("int")
			cv2.drawContours(img, [c], -1, (255, 0, 255), 2)	
			cv2.putText(img, sshape, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX,0.65, (15, 50, 60), 1)	#the required text is written
			cv2.imshow("masked",img)									 #the final image with the color and shape of each contour is given as output

		
value=raw_input("enter nnumber of file (value from 1 to 5)")			# the user inputs the number of the required image
cvalue=str(value)
filn="test"+cvalue+".png"
img=cv2.imread(filn)												#BGR image img
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV_FULL)						#hsv is img in HSV format
cv2.imshow("imgge init",img)							
sr =shaperecognition(img)								 #the class shaperecognition is called in sr with the image img
sr.preprocessing()										 #the selected image img is processed( function preprocessing is called)
cv2.waitKey(0)											 #waits for an imput fromm the user
cv2.destroyAllWindows()
