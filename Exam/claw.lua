-- model in Solvespace 500 mm = 5000 mm in V-rep
--[[
Simulation is 10 times of realistic environment
floor in Solvespace 2.5 m x 2.5 m = 25 m x 25 m in V-rep
ball is in Solivespace 1g (0.001) = 0.01 kg in V-rep
hammer is in Solvespace 0.1 kg (100g) = 1kg in V-rep (0.1 for Inertia)
]]
local slider_x ='move_x'
local slider_y ='move_y'
local slider_z ='move_z'
local slider_paw ='paw_slider'
local player_r ='box_Handle1'

threadFunction=function()
    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
        -- Read the keyboard messages (make sure the focus is on the main window, scene view):
        message,auxiliaryData=sim.getSimulatorMessage()
        while message~=-1 do
            key=auxiliaryData[1]
            sim.addStatusbarMessage('key:'..key)
            if (message==sim.message_keypress) then
                if (auxiliaryData[1]==119) then
                    -- y+ key
                    if (position_y>=0.3)then else position_y = position_y + 0.05 end
                    sim.addStatusbarMessage('position_y:'..position_y)
                end
                
                if  (auxiliaryData[1]==115) then
                    -- y- key
                    if (position_y<=0)then else position_y = position_y - 0.05 end
                    sim.addStatusbarMessage('position_y:'..position_y)
                end
                
                if  (auxiliaryData[1]==100) then
                    -- x+ key 
                    if (position_x>=0.35)then else position_x = position_x + 0.05 end
                    sim.addStatusbarMessage('position_x:'..position_x)
                end
                
                if  (auxiliaryData[1]==97) then
                    -- x- akey
                    if (position_x <= 0)then else position_x = position_x - 0.05 end
                    sim.addStatusbarMessage('position_x:'..position_x)
                end
                if  (auxiliaryData[1]==200) then
                    -- claw go akey
                    if (position_z>=0.3)then else position_z = position_z + 0.05 end
                    sim.addStatusbarMessage('position_z:'..position_z)
                end
                if  (auxiliaryData[1]==120) then
                    -- claw back akey
                    if (position_z >= 0)then else position_z = position_z + 0.05 end
                    sim.addStatusbarMessage('position_z:'..position_z)
                end
                if  (auxiliaryData[1]==122) then
                    -- claw back akey
                    if (position_z <= -0.31)then else position_z = position_z - 0.05 end
                    sim.addStatusbarMessage('position_z:'..position_z)
                end
                if  (auxiliaryData[1]==99) then
                    -- claw back akey
                    if claw_back == 0 then
                        position_paw = 0.021
                        claw_back = 1
                    else
                        position_paw = 0
                        claw_back = 0
                    end
                end
            end
            message,auxiliaryData=sim.getSimulatorMessage()
        end
 
        -- We take care of setting the desired hammer position:
        if claw_back == 1
            then 
        sim.setJointTargetPosition(move_paw, position_paw)
        end
        sim.setJointTargetPosition(move_paw, position_paw)

        sim.setJointTargetPosition(move_x, position_x)
        sim.setJointTargetPosition(move_y, position_y)
        sim.setJointTargetPosition(move_z, position_z)
        --Since this script is threaded, don't waste time here:
        sim.switchThread() -- Resume the script at next simulation loop start
    end

end
-- Put some initialization code here:
-- Retrieving of some handles and setting of some initial values:


move_x = sim.getObjectHandle(slider_x)
move_y = sim.getObjectHandle(slider_y)
move_z = sim.getObjectHandle(slider_z)
move_paw = sim.getObjectHandle(slider_paw)
velocity=0
hammer_back=0
torque=0
position_x = 0
position_y = 0
position_z = 0
position_paw = 0
--orientation=sim.getJointPosition(joint_all_c1, -1)
-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
    sim.addStatusbarMessage('Lua runtime error: '..err)
end
 
-- Put some clean-up code here: