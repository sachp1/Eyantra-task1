#classes and subclasses to import
import cv2
import numpy as np
import os

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape):
    #open csv file in append mode
    filep = open('results1A_teamid.csv','a')
    # create string data to write per image
    datastr = "," + color + "-" + shape
    #write to csv
    filep.write(datastr)

def main(path):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles[:-1]:
        #Open the csv to write in append mode
        filep = open('results1A_teamid.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results1A_teamid.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
