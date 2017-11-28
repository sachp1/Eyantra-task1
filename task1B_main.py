#classes and subclasses to import
import cv2
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape,size,count):
    #open csv file in append mode
    filep = open('results1B_teamid.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + size + "-" + count
    #write to csv
    filep.write(datastr)

def main(path):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################
    areashape=np.zeros(2)
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
                if ar >= 0.95 and ar <= 1.05:
                    shape = "square" 

                else:
                    shape="rectangle" #when aspect ration ~ 1 it is a square

            else:
                shape = "circle"                             #if approx is any other value then it is a circle
            return shape    
        def areacalc(self,shpp):
            sh=np.empty((2), dtype=object)
            sh[0]=cv2.imread(".\\Sample Images\\Sample_{}_large.png".format(shpp))
            sh[1]=cv2.imread(".\\Sample Images\\Sample_{}_small.png".format(shpp))
            for i in range(0,2):
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
        #        print "\n area of : sh ",i,"  is ", area,"px x px"
                areashape[i]=area
        #        cv2.imshow("okay",sh[i])
        #        cv2.waitKey(0)
            return areashape




        def preprocessing(self):                                            #the Fucntion preprocessing is declared                              
            #lower=np.array([100,100,100],dtype=np.uint16)
            #upper=np.array([255,255,255],dtype=np.uint16)       
            #mask=cv2.inRange(self.img,lower,upper)   
            #nott=cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)                               #Masks the BGR image between the values lower and upper 
            #tres=cv2.threshold(nott,250,255,cv2.THRESH_TRIANGLE)[1]
            # tres=cv2.threshold(mask,200,255,cv2.THRESH_BINARY)[1]     
            blurrd=cv2.medianBlur(self.img,5)
            edges=cv2.Canny(blurrd,150,200)                    #apply threshold
            #invmask=cv2.bitwise_not(tres)
            cv2.imshow("threwe",edges)   
            #tres2=invmask  
                                                     #the mask is inverted
            __,cont,hir=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
                                                      #the thresholded image is shown 
            #self.areacalc()
            print"length of countoours is : " ,len(cont)
            i=0
            for c in cont:  
                if (i%2 ==0):                                                          
                    M=cv2.moments(c)                                             #the moments are found
                    if(M["m00"]==0):                                        
                        break                                                   #The fuction breaks if divide by zero condition occurs
                    cval=''                                                     #the value for color is intitally a blank space
                    cx=int((M["m10"]/M["m00"]))
                    cy=int((M["m01"]/M["m00"]))
                    shape=self.detect(c)                              #the shape of each contour is returned by the function detect inside the class ShapeDetector
                    if (shape=="rectangle" or shape=="square"):
                        x,y,w,h=cv2.boundingRect(c)
                        cx=x+10
                        cy=y+10
                    col=hsv[cy][cx][0]                              #the hue value of each contour is given to the function col

                    if((col>=0)&(col<5)):
                        cval="red"
                    elif((col>=5)&(col<30)):
                        cval="orange"
                    elif((col>=30)&(col<56)):
                        cval="yellow"
                    elif((col>=56)&(col<128)):                      #The H values of (H,S,V) are checked to find out the color
                        cval="green"
                    elif((col>=128)&(col<213)):
                        cval="blue"
                    siz=""
                    c = c.astype("float")
                    c = c.astype("int")
                    cv2.drawContours(img, [c], -1, (255, 0, 255), 2)   
                    area = cv2.contourArea(c)
                    print area 
                    areash=self.areacalc(shape)
                    if((area/areash[0])>=0.95):
                        siz="large"
                    elif((area/areashape[1])<=1.05):
                        siz="small"
                    else:
                        siz="medium"
                    sshape=siz+" "+cval+" "+shape
                    cv2.putText(img, sshape, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX,0.35, (15, 50, 60), 1)  #the required text is written
                    cv2.imshow("masked",img)
                    print "\n"+sshape
                i+=1 
    im=cv2.imread(path)   
    img=im                            #the final image with the color and shape of each contour is given as output
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV_FULL)                        #hsv is img in HSV format  
    sr =shaperecognition(img)                              #the class shaperecognition is called in sr with the image img
    sr.preprocessing()                                       #the selected image img is processed( function preprocessing is called)
    cv2.waitKey(0)                                           #waits for an imput fromm the user
    pt=path[2:]
    pt2=pt.replace("test","output")
   # cv2.imwrite(pt2,img,[cv2.IMWRITE_PNG_STRATEGY_DEFAULT,9])
    cv2.destroyAllWindows()
    return pt

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('results1B_teamid.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results1B_teamid.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
