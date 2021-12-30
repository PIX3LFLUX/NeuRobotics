import os,  inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

import pybullet as p
import numpy as np
import pybullet_data
import time
import math
import random

class env1D:
    
    def __init__(self, startPos=[0,0,0],gui=False, stepSize = 0.00314, timeStep=0.01, gravity=-9.81, dt = 1e-3):
        self.gui = gui
        self.timeStep = timeStep
        self.stepSize = stepSize
        self.maxVelocity = .35
        self.maxForce = 300
        self.startPosition = startPos
        self.startOrientation =p.getQuaternionFromEuler([0.,0,math.pi/2])
        self.jointPosition = [0,0,0,0,0,0,0]
        self.moveable = [True,True,False,True,False,False,False]
        self.moveDir = [0,0,0,0,0,0,0]
        self.jumpFlag = False
        self.moveFlag = False
        self.collisionFlag = False
        self.setup()
        
        
    def setup(self):#Loads Plane and Robot, determins number of Joints and their upper and lower bounds. Sets Robot to starting Position
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeId = p.loadURDF("plane.URDF")
        self.botId = p.loadURDF("kuka_iiwa/model.urdf", self.startPosition, self.startOrientation)
        self.numJoints = p.getNumJoints(self.botId)
        self.upperLimits = []
        self.lowerLimits = []
        for i in range(self.numJoints):
            self.upperLimits.append(p.getJointInfo(self.botId, i)[9])
            self.lowerLimits.append(p.getJointInfo(self.botId, i)[8])
            p.setJointMotorControl2(self.botId, i, p.POSITION_CONTROL, targetPosition=self.jointPosition[i])
        #print(self.upperLimits)
        #print(self.lowerLimits)
        
    
    
    def evaluateState(self):
        for index in range(self.numJoints):
            self.jointPosition[index] = p.getJointState(botId, i)[0]
            
    def moveStep(self):
        for index in range(self.numJoints):
            if self.moveable:
                self.jointPosition[index] += (self.moveDir[index]*self.stepSize)
                if index%2 == 0:
                    if self.jointPosition[index] < self.lowerLimits[index]:
                        self.jointPosition[index] = self.upperLimits[index]
                        self.jumpFlag = True
                        for i in range(5):
                            p.stepSimulation()
                            time.sleep(1/240)
                    elif self.jointPosition[index] > self.upperLimits[index]:
                        self.jointPosition[index] = self.lowerLimits[index]
                        self.jumpFlag = True
                        for i in range(5):
                            p.stepSimulation()
                            time.sleep(1/240)                    
                p.setJointMotorControl2(self.botId, index, p.POSITION_CONTROL, targetPosition=self.jointPosition[index])
    
    

                
    




            
    
    


        
        
        
    