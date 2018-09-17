import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import math

path = str(sys.argv[1]) #folder argument
#print(path)
file = open(path+'/'+'labels.txt',"r") #open given label file
output = open('output.txt',"w")# this file writes approximated position of the phone
param = open('parameter.txt',"w") #this file writes maximum no of parameters required 
n = 4# How many points to detect; phone has a rectangular shape;rectangle has minimum 4 points
n0 = 0# keeps the maximum no of points
low_limit = 0.030 #lowest distance between two selected feature points
high_limit = 0.11 #highest distance between two selected feature points
coordinate = np.zeros((n,2)) #numpy array to store the coordinate
row = 0 # row counter for the numpy array
x0 = []  # keeps x coordinate within high and low limit
y0 = []  # keeps  y coordinate within high and low limit
total = 0  #total no of images for training
correct = 0 #correct no of images within 0.05 radius of the given position of the phone
#loops through each image file
for line in file:
     s = line
     f,ax,ay = s.split(' ') #gets image file name, position of the phone from labels.txt
     ax = float(ax) #converts str to float
     ay = float(ay)
     print(f)
     img = cv2.imread(path+'/'+f) #reads image file
     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #converts to gray color
     height, width = img.shape[:2] #gets height, width of the image for normalization
     print('height: ',height, 'width: ', width)
     iteration = 1
     x0.clear()
     y0.clear()
     n = 4 #initial no of points to detect
     while len(x0) != 4:
        print('iteration', iteration, 'no of points', n)
        corners = cv2.goodFeaturesToTrack(gray,n,0.01,0.11) #gets N strongest corners
        corners = np.int0(corners)
        row = 0
        #loops through each corner
        for i in corners:
             x,y = i.ravel()
            #print(x/width,y/height)
            #print(x,y)
             coordinate[row,0]=x/width  #normalize and store it in the numpy array
             coordinate[row,1]=y/height
             row = row+1
             cv2.circle(img,(x,y),3,255,-1)
        j = 0
        k = 0
        #store those points that fall within low limit and high limit
        for j in range(0,n,1):
             x0.append(coordinate[j,0])
             y0.append(coordinate[j,1]) 
             for k in range(0,n,1):
                   if  j!=k:
                       dis = math.sqrt((coordinate[j,0]-coordinate[k,0])*(coordinate[j,0]-coordinate[k,0])+(coordinate[j,1]-coordinate[k,1])*(coordinate[j,1]-coordinate[k,1]))
                       #print(dis)
                       if low_limit <= dis <= high_limit:
                           x0.append(coordinate[k,0])  #store normalized x coordinate
                           y0.append(coordinate[k,1])  #store normalized y coordinate
                       if len(x0) == 4:  #4 points of a rectangular shape has been recognized
                           break
             if k < n-1:
                 break
             else:
                 x0.clear()
                 y0.clear()
        n = n+1 #increasing no of points to find 4 coordinates
        iteration = iteration+1
        coordinate = np.resize(coordinate,(n,2))#resizes current coordinates
        coordinate.fill(0)
        #print(len(x0), len(y0))
     cx = np.mean(x0)  #current x coordinate is the mean of 4 x coordinates of the rectangle
     cy = np.mean(y0)  #current y coordinate is the mean of 4 x coordinates of the rectangle
     print(cx, cy,gray[int(cx*height),int(cy*width)])
     total = total+1
     dis = math.sqrt((ax-cx)*(ax-cx)+(ay-cy)*(ay-cy))
     if 0.0 <= dis <= 0.05:
          correct = correct+1
     fo = f+str(' ')+str(cx)+str(' ')+str(cy)+(' ')+str(dis)+' '+str(n)+'\n' #writes output to file
     if n0 < n:
         n0 = n
     output.write(fo)
#plt.imshow(img),plt.show()
#print(n)
#print('total',total)
#print('correct',correct)
#print('%correct', correct/total)
param.write(str(n0)) #writes maximum no of corners required to calculate the phone position correctly
#close all the files
param.close()
file.close()
output.close()