import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import math

path = str(sys.argv[1]) #given image path
#print(path)
low_limit = 0.030  #lowest distance between two selected feature points
high_limit = 0.11    #highest distance between two selected feature points
param = open('parameter.txt',"r") #read parameter n from the file
s = param.readline()
n = int(s) #convert to int
coordinate = np.zeros((n,2)) #numpy array to store the coordinate

img = cv2.imread(path) # read image file from the given path
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert to gray color
height, width = img.shape[:2] #get the image height and width for normalization
corners = cv2.goodFeaturesToTrack(gray,n,0.01,0.11) #gets the features
corners = np.int0(corners)
row = 0 # row counter for the numpy array
x0 = []  # keeps x coordinate within high and low limit
y0 = []  # keeps  y coordinate within high and low limit
for i in corners:
        x,y = i.ravel()
        #print(x/width,y/height)
        #print(x,y)
        coordinate[row,0]=x/width  #normalize to (0,1)
        coordinate[row,1]=y/height  #normalize to (0,1)
        row = row+1
        #cv2.circle(img,(x,y),3,255,-1)
        j = 0
        k = 0
        x0.clear()
        y0.clear()
        for j in range(0,n,1):
             x0.append(coordinate[j,0])
             y0.append(coordinate[j,1]) 
             for k in range(0,n,1):
                   if  j!=k:
                       dis = math.sqrt((coordinate[j,0]-coordinate[k,0])*(coordinate[j,0]-coordinate[k,0])+(coordinate[j,1]-coordinate[k,1])*(coordinate[j,1]-coordinate[k,1]))
                       #print(dis)
                       if low_limit <= dis <= high_limit:
                           x0.append(coordinate[k,0])
                           y0.append(coordinate[k,1])
                       if len(x0) == 4:
                           break
             if k < n-1:
                 break
             else:
                 x0.clear()
                 y0.clear()
        
      
     
cx = np.mean(x0)
cy = np.mean(y0)
print(cx, cy)
