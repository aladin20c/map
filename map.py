#!/usr/bin/env python3

# for mathematical functions
import math
# for manipulating images
from PIL import Image, ImageDraw
from numpy import array

###############################################################################

## mercator projection
##takes as arguments the longitude and the latitude coordinates of a point
##returns x and y coordinates on a mercator map

###############################################################################
def mercator_projection(longitude,latitude):
  x,y=0,0
  x=longitude
  y= math.log( abs( math.tan(latitude)+ 1/math.cos(latitude) ) )
  return x,y


###############################################################################

#intersection between two circles
##takes as arguments the coordinates and the radius of two circles
#return coordinates of ths two points of the intersection of the two circles

###############################################################################
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d
        y2=y0+a*(y1-y0)/d
        x3=x2+h*(y1-y0)/d
        y3=y2-h*(x1-x0)/d

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        print(" x3 "+str(x3) +" y3 "+str(y3)+" x4 "+str(x4) +" y4 "+str(y4))
        return (x3, y3, x4, y4)

###############################################################################
#reading the image
###############################################################################


image = Image.open("ndvi-2021-06-04-7J0k6pEFil.png")
arr=array(image)
height,width=arr.shape[0],arr.shape[1]

###############################################################################
#gett1ng the position of the first cooordinate (en haut à droite).
###############################################################################

x1,y1=0,0
for i in range(width-1,0,-1) :
    if arr[0][i][0]!=0 or arr[0][i][1]!=0 or arr[0][i][2]!=0 or arr[0][i][3]!=0:
        x1=i
        break

###############################################################################
#gett1ng the position of the second cooordinat (plus en bas à gauche)
###############################################################################

x2,y2=0,0
found = False
for j in range(height) :
    y2=j
    for i in range(width) :
        if arr[j][i][0]!=0 or arr[j][i][1]!=0 or arr[j][i][2]!=0 or arr[j][i][3]!=0 :
            if i-x2 != 2 :
                x2=i
                break
            else :
                found = True
                break
    if found : break




###############################################################################

#coordinate of the top right pixel on a mercator map
X1,Y1=mercator_projection(36.690702848085614,10.532794780008729)
#coordinate of the bottom left pixel on a mercator map
X2,Y2=mercator_projection(36.68638314797726,10.529198094023505)
#coordinate of the pixel to be found on a mercator map
X3,Y3=mercator_projection(36.688256333333335,10.531021333333333)

#distance between the top right pixel and the bottom left pixel on a mercator map
Delta= math.sqrt( (X1-X2)*(X1-X2)+(Y1-Y2)*(Y1-Y2) )
#distance between top right pixel and the pixel to be found on a mercator map
Delta1= math.sqrt( (X1-X3)*(X1-X3)+(Y1-Y3)*(Y1-Y3) )
#distance between the bottom left pixel and the pixel to be found on a mercator map
Delta2= math.sqrt( (X2-X3)*(X2-X3)+(Y2-Y3)*(Y2-Y3) )





#distance between the top right pixel and the bottom left pixel in the image
delta=math.sqrt( (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2) )

ratio_of_change= delta/Delta #the ratio of distance doesn't change
#since the picture is also a zoomed mercator projection the ratio of distance of
#mercator projection and the picture is constant.

#distance between top right pixel and the pixel to be found  in the image
delta1= Delta1*ratio_of_change
#distance between the bottom left pixel and the pixel to be found  in the image
delta2= Delta2*ratio_of_change


x3,y3,x4,y4=get_intersections(x1,y1,delta1,x2,y2,delta2)
#due to small inaccuracy in calculations since the scale is too small and that the mervator
#projection isn't perfect we take the median form the two points that we found as the
#point to be found
x5=(x3+x4)/2
y5=(y3+y4)/2

###############################################################################
# saving the pixel in a file named pixel.png
###############################################################################

print(image.getpixel((x5,y5)))
img = Image.new('RGBA', (200, 200), color = image.getpixel((x5,y5)))
img.save('pixel.png')


###############################################################################
# visual representation of the algorithm
###############################################################################

draw= ImageDraw.Draw(image)

draw.ellipse((x1-5,y1-5,x1+5,y1+5),fill=(0,250,0),outline='yellow' )
draw.ellipse((x2-5,y2-5,x2+5,y2+5),fill=(0,250,0),outline='yellow' )

draw.ellipse((x3-2,y3-2,x3+2,y3+2),fill=(0,250,0),outline='yellow' )
draw.ellipse((x4-2,y4-2,x4+2,y4+2),fill=(0,250,0),outline='yellow' )

draw.ellipse((x1-delta1,y1-delta1,x1+delta1,y1+delta1),outline='black' )
draw.ellipse((x2-delta2,y2-delta2,x2+delta2,y2+delta2),outline='blue' )

draw.ellipse((x5-2,y5-2,x5+2,y5+2),fill=(250,250,250),outline='purple' )


image.show()

newimg = Image.open("pixel.png")
newimg.show()
###############################################################################
