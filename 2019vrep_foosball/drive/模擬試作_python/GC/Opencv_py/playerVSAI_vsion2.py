import vrep
import time

import pole
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
        centroid_x= 62- int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)-120
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = ((centroid_x/420), (centroid_y/-500))
    return ctr
def player_position (player_handle):
    position = vrep.simxGetObjectPosition(clientID,player_handle,table,vrep.simx_opmode_oneshot_wait)  
    #ret = vrep.simxSetJointPosition(clientID,player_handle,1,vrep.simx_opmode_oneshot)
    return position[1]#(Z,Y,X)
    
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
    print('Connected to remote API server')
  # get vision sensor objects
    res, v0 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
    res, v1 = vrep.simxGetObjectHandle(clientID, 'vs2', vrep.simx_opmode_oneshot_wait)
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
    err,Sphere_handle=vrep.simxGetObjectHandle(clientID,'Sphere',vrep.simx_opmode_oneshot_wait)
    err,table=vrep.simxGetObjectHandle(clientID,'table',vrep.simx_opmode_oneshot_wait)
    err,Bplayer_handle_1=vrep.simxGetObjectHandle(clientID,'player_cloth1',vrep.simx_opmode_oneshot_wait)
    err,Bslider_handle=vrep.simxGetObjectHandle(clientID,'left_slider1',vrep.simx_opmode_oneshot_wait)
    err,Bjoint_handle=vrep.simxGetObjectHandle(clientID,'left_joint1',vrep.simx_opmode_oneshot_wait)
    time.sleep(1)
    while (vrep.simxGetConnectionId(clientID) != -1):
        err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
        if err == vrep.simx_return_ok:
            Bplayer_position_1=player_position(Bplayer_handle_1)
            image_byte_array = array.array('b', image)
            image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), bytes(image_byte_array), "raw", "RGB", 0, 1)
            img2 = numpy.asarray(image_buffer)
            ret_green = track_green_object(img2)
            #y軸座標為0 x軸座標為1  #position(Z,Y,X)
            if ret_green != None:
                Y =round(float(ret_green[0])-float(Bplayer_position_1[1]),3)
                X =round(float(ret_green[1])-float(Bplayer_position_1[2]),3)
                YS=(Y*-0.5)
                slide_1=0
                print('G=',"%.2f" %ret_green[1],"%.2f" %ret_green[0]) #y軸座標為0 x軸座標為1
                print('player=',"%.2f" %Bplayer_position_1[2],"%.2f" %Bplayer_position_1[1])#position (Z,Y,X)
                print(X,Y)
                pole.pole_P1(Bjoint_handle,Bslider_handle,X,Y) 
                #'''
          # overlay rectangle marker if something is found by OpenCV
            if ret_green:
                cv2.rectangle(img2,(round(ret_green[0])-5,round(ret_green[1])-5), (round(ret_green[0])+5,round(ret_green[1])+5), (0x99,0xff,0x33), 1)
              # return image to sensor 'v1'
        elif err == vrep.simx_return_novalue_flag:
          print("no image yet")
          pass
        else:
          print(err)
else:
  print("Failed to connect to remote API Server")
  vrep.simxFinish(clientID)