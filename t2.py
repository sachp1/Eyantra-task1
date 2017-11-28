#####################################################################################################
    #Write your code here!!!
#####################################################################################################
import cv2
import numpy as np
import os
areashape=np.zeros(8)
class shaperecognition():     #A class is defined
    def __init__(self, img):
        self.img= img
    def detect(self, c):
        shape = "Shape Not Detected"                      #if the shape is not detected then 'shape not detected ' is returned
        per = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * per, True)
        if len(approx) == 3:
            shape = "triangle"                            # if shape is triangle, it will have 3 vertices

        elif len(approx) == 4:                            # when vertices =4 it can be a square or a rectangle
            (x, y, wi, h) = cv2.boundingRect(approx)
            ar = wi / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle" #when aspect ration ~ 1 it is a square

        elif len(approx) == 5:                           #when vertices is 5 ,it is a pentagon
            shape = "pentagon"

        else:
            shape = "circle"                             #if approx is any other value then it is a circle
        return shape    
    def areacalc(self):
        sh=np.empty((8), dtype=object)
        sh[0]=cv2.imread(".\\Sample Images\\Sample_circle_large.png")
        sh[1]=cv2.imread(".\\Sample Images\\Sample_circle_small.png")
        sh[2]=cv2.imread(".\\Sample Images\\Sample_rectangle_large.png")
        sh[3]=cv2.imread(".\\Sample Images\\Sample_rectangl_small.png")
        sh[4]=cv2.imread(".\\Sample Images\\Sample_square_large.png")
        sh[5]=cv2.imread(".\\Sample Images\\Sample_square_small.png")
        sh[6]=cv2.imread(".\\Sample Images\\Sample_triangle_large.png")
        sh[7]=cv2.imread(".\\Sample Images\\Sample_triangle_small.png")
        for i in range(0,8):
            mask=cv2.cvtColor(sh[i],cv2.COLOR_BGR2GRAY)
            tres=cv2.threshold(mask,230,255,cv2.THRESH_BINARY)[1]                       #apply threshold
            invmask=cv2.bitwise_not(tres)                                               #the mask is inverted
            _,cont,h=cv2.findContours(invmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)        #the thresholded image is shown 
            c2 = cont[0]
            epsilon = 0.1*cv2.arcLength(c2,True)
            approx = cv2.approxPolyDP(c2,epsilon,True)
            #for k in cont:
            #c2 = c2.astype("float")
            #c2 = c2.dtype("int")
            cv2.drawContours(sh[i], approx, -1, (255, 0, 255),2)   
            area = cv2.contourArea(c2)
            print "\n area of : sh ",i,"  is ", area,"px x px"
            areashape[i]=area
    #        cv2.imshow("okay",sh[i])
    #        cv2.waitKey(0)





    def preprocessing(self):                                            #the Fucntion preprocessing is declared                              
        lower=np.array([100,100,100],dtype=np.uint16)
        upper=np.array([255,255,255],dtype=np.uint16)       
        mask=cv2.inRange(self.img,lower,upper)                                  #Masks the BGR image between the values lower and upper 
        tres=cv2.threshold(mask,100,255,cv2.THRESH_BINARY)[1]                       #apply threshold
        invmask=cv2.bitwise_not(tres)                                               #the mask is inverted
        cont=cv2.findContours(invmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)                                              #the thresholded image is shown 
        cont = cont[1] 
        self.areacalc()
        for c in cont:                                                              #the moments are found
            M=cv2.moments(c)
            if(M["m00"]==0):                                        
                break                                                   #The fuction breaks if divide by zero condition occurs
            cval=''                                                     #the value for color is intitally a blank space
            cx=int((M["m10"]/M["m00"]))
            cy=int((M["m01"]/M["m00"]))
            shape=self.detect(c)                              #the shape of each contour is returned by the function detect inside the class ShapeDetector
            col=hsv[cy][cx][0]                              #the hue value of each contour is given to the function col

            if((col>=0)&(col<43)):
                cval="red "
            elif((col>=43)&(col<128)):                      #The H values of (H,S,V) are checked to find out the color
                cval="green "
            elif((col>=128)&(col<213)):
                cval="blue "
            siz=""
            c = c.astype("float")
            c = c.astype("int")
            cv2.drawContours(img, [c], -1, (255, 0, 255), 2)   
            area = cv2.contourArea(c)
            print area 
            if (shape=='triangle'):
                if((area/areashape[6])>=0.95):
                    siz="large"
                elif((area/areashape[7])<=1.05):
                    siz="small"
                else:
                    siz="medium"
            sshape=siz+" "+cval+shape
            cv2.putText(img, sshape, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX,0.65, (15, 50, 60), 1)  #the required text is written
            cv2.imshow("masked",img)    
im=cv2.imread("test1.png")   
img=im                            #the final image with the color and shape of each contour is given as output
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV_FULL)                        #hsv is img in HSV format  
sr =shaperecognition(img)                              #the class shaperecognition is called in sr with the image img
sr.preprocessing()                                       #the selected image img is processed( function preprocessing is called)
cv2.waitKey(0)                                           #waits for an imput fromm the user
pt=path[2:]
pt2=pt.replace("test","output")
cv2.imwrite(pt2,img,[cv2.IMWRITE_PNG_STRATEGY_DEFAULT,9])
cv2.destroyAllWindows()