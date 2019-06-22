-- model in Solvespace 500 mm = 5000 mm in V-rep
--[[
Simulation is 10 times of realistic environment
floor in Solvespace 2.5 m x 2.5 m = 25 m x 25 m in V-rep
ball is in Solivespace 1g (0.001) = 0.01 kg in V-rep
hammer is in Solvespace 0.1 kg (100g) = 1kg in V-rep (0.1 for Inertia)
]]
local joint_r = {'left_joint1','left_joint3','left_joint5','left_joint7'}
local joint_b = {'left_joint','left_joint2','left_joint4','left_joint6'}
local slider_r ={'left_slider1','left_slider3','left_slider5','left_slider7'}
local slider_b ={'left_slider','left_slider2','left_slider4','left_slider6'}
local player_r ={'left_bearing1','left_bearing3','left_bearing5','left_bearing7'}


threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
        message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
key=auxiliaryData[1]
sim.addStatusbarMessage('key:'..key)

            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==119) then
                    -- up key
                    joint_all_c1=sim.getObjectHandle(joint_b[1])
                    joint_all_c2=sim.getObjectHandle(joint_b[2])
                    joint_all_c3=sim.getObjectHandle(joint_b[3])
                    joint_all_c4=sim.getObjectHandle(joint_b[4]) 
                    velocity=100
                    torque=200
                    hammer_back = 0
                end
                if  (auxiliaryData[1]==115) then
                    -- down key
                    joint_all_c1=sim.getObjectHandle(joint_b[1])
                    joint_all_c2=sim.getObjectHandle(joint_b[2])
                    joint_all_c3=sim.getObjectHandle(joint_b[3])
                    joint_all_c4=sim.getObjectHandle(joint_b[4])
                     hammer_back = 1
                     torque=-200
                     velocity =-100
                end
                if  (auxiliaryData[1]==100) then
                    -- right key 
                if (sliding_b>=0.3)then else sliding_b = sliding_b + 0.05 end
                sim.addStatusbarMessage('sliding_b:'..sliding_b)
                end
                if  (auxiliaryData[1]==97) then
                    -- left key
                    if (sliding_b<=-0.3)then else sliding_b = sliding_b - 0.05 end
                    sim.addStatusbarMessage('sliding_b:'..sliding_b)
                end
            end
            message,auxiliaryData=sim.getSimulatorMessage()
        end
 
        -- We take care of setting the desired hammer position:
        if hammer_back == 1
            then 
        sim.setJointTargetPosition(joint_all_c1, velocity)
        sim.setJointTargetPosition(joint_all_c2, velocity)
        sim.setJointTargetPosition(joint_all_c3, velocity)
        sim.setJointTargetPosition(joint_all_c4, velocity)
               --sim.setObjectPosition(hammer, -1, position)
        end
        sim.setJointTargetPosition(joint_all_c1, velocity)
        sim.setJointTargetPosition(joint_all_c2, velocity)
        sim.setJointTargetPosition(joint_all_c3, velocity)
        sim.setJointTargetPosition(joint_all_c4, velocity)

        sim.setJointTargetPosition(slider_b_c1, sliding_b)
        sim.setJointTargetPosition(slider_b_c2, sliding_b)
        sim.setJointTargetPosition(slider_b_c3, sliding_b)
        sim.setJointTargetPosition(slider_b_c4, sliding_b)
        --Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end

end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:



joint_all_c1=sim.getObjectHandle(joint_b[1])
joint_all_c2=sim.getObjectHandle(joint_b[2])
joint_all_c3=sim.getObjectHandle(joint_b[3])
joint_all_c4=sim.getObjectHandle(joint_b[4])

slider_b_c1=sim.getObjectHandle(slider_b[1])
slider_b_c2=sim.getObjectHandle(slider_b[2])  
slider_b_c3=sim.getObjectHandle(slider_b[3])
slider_b_c4=sim.getObjectHandle(slider_b[4]) 

hammer=sim.getObjectHandle('player')
velocity=0
hammer_back=0
torque=0
--sliding_r = 0
sliding_b = 0
Bplayer1_slider=0
orientation=sim.getJointPosition(joint_all_c1, -1)
position=sim.getObjectPosition(hammer, -1)
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
 
-- Put some clean-up code here: