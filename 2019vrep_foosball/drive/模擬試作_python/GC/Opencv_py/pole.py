import vrep
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
def speed(handle,speed):
    vrep.simxSetJointTargetVelocity(clientID,handle,speed,vrep.simx_opmode_oneshot_wait)

def pole_P1 (joint,slider,X,Y) :
        YS=(Y*-0.5)
        slide=0
        if  Y<0.0:
            slide=slide-YS
        elif  Y>0.0:
            slide=slide-YS
        else:
            pass
        if X <= 0.01 and X > -0.01 : 
            speed(joint,10)
            speed(joint,1)
        else:
            speed(joint,-10)
            speed(joint,-1)
        speed(slider,slide)