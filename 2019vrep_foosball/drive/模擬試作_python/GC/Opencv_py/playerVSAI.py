import vrep
import time

from PIL import Image as I
import array

import cv2, numpy

# function based on: 
#   https://github.com/simondlevy/OpenCV-Python-Hacks/blob/master/greenball_tracker.py
def speed(handle,speed):
    vrep.simxSetJointTargetVelocity(clientID,handle,speed,vrep.simx_opmode_oneshot_wait)
        
def track_green_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only green colors
    range = 15
    lower_green = numpy.array([60-range,100,100])
    upper_green = numpy.array([60+range,255,255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr

def track_red_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only green colors
    range = 15
    lower_blue = numpy.array([120-range,100,100])
    upper_blue = numpy.array([120+range,255,255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)


if clientID!=-1:
  print('Connected to remote API server')
  # get vision sensor objects
  res, v0 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
  res, v1 = vrep.simxGetObjectHandle(clientID, 'vs2', vrep.simx_opmode_oneshot_wait)
  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
  err,Sphere_handle =   vrep.simxGetObjectHandle(clientID,'Sphere',vrep.simx_opmode_oneshot_wait)
  
  err,Bplayer1_handle  =   vrep.simxGetObjectHandle(clientID,'left_bearing1',vrep.simx_opmode_oneshot_wait)
  err,Bjoint1_handle  =   vrep.simxGetObjectHandle(clientID,'left_joint1',vrep.simx_opmode_oneshot_wait)
  err,Bslider1_handle  =   vrep.simxGetObjectHandle(clientID,'left_slider1',vrep.simx_opmode_oneshot_wait)
  
  err,Bplayer3_handle  =   vrep.simxGetObjectHandle(clientID,'left_bearing3',vrep.simx_opmode_oneshot_wait)
  err,Bjoint3_handle  =   vrep.simxGetObjectHandle(clientID,'left_joint3',vrep.simx_opmode_oneshot_wait)
  err,Bslider3_handle  =   vrep.simxGetObjectHandle(clientID,'left_slider3',vrep.simx_opmode_oneshot_wait)
  
  err,Bplayer5_handle  =   vrep.simxGetObjectHandle(clientID,'left_bearing5',vrep.simx_opmode_oneshot_wait)
  err,Bjoint5_handle  =   vrep.simxGetObjectHandle(clientID,'left_joint5',vrep.simx_opmode_oneshot_wait)
  err,Bslider5_handle  =   vrep.simxGetObjectHandle(clientID,'left_slider5',vrep.simx_opmode_oneshot_wait)
  
  err,Bplayer7_handle  =   vrep.simxGetObjectHandle(clientID,'left_bearing7',vrep.simx_opmode_oneshot_wait)
  err,Bjoint7_handle  =   vrep.simxGetObjectHandle(clientID,'left_joint7',vrep.simx_opmode_oneshot_wait)
  err,Bslider7_handle  =   vrep.simxGetObjectHandle(clientID,'left_slider7',vrep.simx_opmode_oneshot_wait)
  
  err,B=vrep.simxSetObjectPosition (clientID,'left_slider7',-1,vrep.simx_opmode_oneshot)
  time.sleep(1)
  while (vrep.simxGetConnectionId(clientID) != -1):
    # get image from vision sensor 'v0'
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
        image_byte_array = array.array('b', image)
        #print(image_byte_array)
        image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), bytes(image_byte_array), "raw", "RGB", 0, 1)
        img2 = numpy.asarray(image_buffer)
      # try to find something green
        ret_green = track_green_object(img2)
        ret_red = track_red_object(img2)
        #ret_blue = track_blue_object(img2) 玩家是藍色不用抓位置
        #print('B=',ret_blue[1],ret_blue[0])#y軸座標為0 x軸座標為1
        #print('R=',ret_red[1],ret_red[0])
        #print('G=',ret_green[1],ret_green[0])
        #'''
        if ret_green != None and ret_red != None:
            Rv = float(ret_green[0])-float(ret_red[0])#y軸座標為0 x軸座標為1
            RRv=float(ret_green[1])-float(ret_red[1])#y軸座標為0 x軸座標為1
            
            if Rv == 0.0:
                pass
            else:
                speed(Bslider1_handle , Rv*-0.02)and speed(Bslider3_handle , Rv*-0.02)and speed(Bslider5_handle , Rv*-0.02)and speed(Bslider7_handle , Rv*-0.02)
                
            if  ret_red[1] <=236 and ret_green[1] >= 237:
                if ret_green[0] >62.5:
                    speed(Bjoint1_handle,-20)and speed(Bjoint3_handle,-20) and speed(Bjoint5_handle,-20)and speed(Bjoint7_handle,-20)
                    time.sleep(0.1)
                    speed(Bslider1_handle , 2)and speed(Bslider3_handle ,2)and speed(Bslider5_handle , 2)and speed(Bslider7_handle , 2)
                    time.sleep(0.1)
                    if ret_green[1] != ret_red[1]:
                        Rv = float(ret_green[0])-float(ret_red[0])
                        if Rv == 0.0:
                            pass
                        else:
                            speed(Bslider1_handle , Rv*-0.02)and speed(Bslider3_handle , Rv*-0.02)and speed(Bslider5_handle , Rv*-0.02)and speed(Bslider7_handle , Rv*-0.02)
                    else:
                        speed(Bjoint1_handle,2)and speed(Bjoint3_handle,2) and speed(Bjoint5_handle,2)and speed(Bjoint7_handle,2)
                    
                elif ret_green[0] <62.5:
                    speed(Bjoint1_handle,-20)and speed(Bjoint3_handle,-20) and speed(Bjoint5_handle,-20)and speed(Bjoint7_handle,-20)
                    time.sleep(0.1)
                    speed(Bslider1_handle , 2)and speed(Bslider3_handle ,2)and speed(Bslider5_handle , 2)and speed(Bslider7_handle , 2)
                    time.sleep(0.1)
                    if ret_green[1] != ret_red[1]:
                        Rv = float(ret_green[0])-float(ret_red[0])
                        if Rv == 0.0:
                            pass
                        else:
                            speed(Bslider1_handle , Rv*-0.02)and speed(Bslider3_handle , Rv*-0.02)and speed(Bslider5_handle , Rv*-0.02)and speed(Bslider7_handle , Rv*-0.02)
                    else:
                        speed(Bjoint1_handle,2)and speed(Bjoint3_handle,2) and speed(Bjoint5_handle,2)and speed(Bjoint7_handle,2)
            elif ret_green[0]-ret_red[0] >= -3 and ret_green[0]-ret_red[0] <= 3:
                if RRv<-10.0:
                     speed(Bjoint1_handle,-2)and speed(Bjoint3_handle,-2) and speed(Bjoint5_handle,-2)and speed(Bjoint7_handle,-2)
                elif RRv>-10.0:
                     speed(Bjoint1_handle,2)and speed(Bjoint3_handle,2) and speed(Bjoint5_handle,2)and speed(Bjoint7_handle,2)
                else:
                    pass
            #'''
      # overlay rectangle marker if something is found by OpenCV
        if ret_green:
            cv2.rectangle(img2,(ret_green[0]-5,ret_green[1]-5), (ret_green[0]+5,ret_green[1]+5), (0x99,0xff,0x33), 1)
          # return image to sensor 'v1'
        if ret_red:
            cv2.rectangle(img2,(ret_red[0]-3,ret_red[1]-5), (ret_red[0]+3,ret_red[1]+5), (0xff,0x33,0x33), 1)
        img2 = img2.ravel()
        vrep.simxSetVisionSensorImage(clientID, v1, img2, 0, vrep.simx_opmode_oneshot)
    elif err == vrep.simx_return_novalue_flag:
      print("no image yet")
      pass
    else:
      print(err)
else:
  print("Failed to connect to remote API Server")
  vrep.simxFinish(clientID)