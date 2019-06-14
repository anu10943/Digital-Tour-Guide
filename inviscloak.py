import numpy as np
import time
import cv2
# red is cloak color and exists for hue values from 0-10 & 170_180
# hsb/hsv=hue saturation(darkness) brightness/value  hue depends on color and angle 0 - 360 degree 4 colours , in open cv 8 bits 2^8 =255, 0- 10(actually 30 but low shade skin also shade of red, total(0 to 180 ) & 170 -180
#RGB 3 matrices superimposed to get image ALL three matrices depend on color
#brain simliar to hsv colorspace
cap=cv2.VideoCapture(0)

time.sleep(4)
bckg=0
for i in range(50):
	ret,bckg=cap.read()
	
while (cap.isOpened()):
	ret,img=cap.read()
	if not ret:
		break
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	lower_red=np.array([0,0,0])#below 120 is white red, pink ,<70 really low brightness
	upper_red=np.array([10,255,255])

	mask1=cv2.inRange(hsv,lower_red,upper_red)#segmentation of cloak, checking if any hsv value btw lower and upper red
	 
	lower_red=np.array([170,0,0])#both saturation & brightness remain same
	upper_red=np.array([180,255,255])
	mask2=cv2.inRange(hsv,lower_red,upper_red)
 
	mask1=mask1+mask2#adds any value of red got from m1 &m2 yto m1
#morphology/morphological transformation check opencv site
#morphy-open removes noise in img, args=(mask,fn,(multiply 3X3 matix of 1s
	mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)
	mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8),iterations=1)

	mask2=cv2.bitwise_not(mask1)# except the floak
	res1=cv2.bitwise_and(bckg,bckg,mask=mask1)#bitwise and btw bckg and mask as bckg
	res2=cv2.bitwise_and(img,img,mask=mask2)# img subs in missing cloak part
	final_o=cv2.addWeighted(res1,1,res2,1,0)# addin res1 and res 2,(res1,alpha,res2,beta,gamma) Alpha*res1+beta*res2+gamma
	cv2.imshow('invisible',final_o)
	k=cv2.waitKey(1) & 0xFF
	if k==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
# addin res1 and res 2,
	 
	
	
