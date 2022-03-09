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

def cartToSpher(x,y,z):
    r = math.sqrt(x*x+y*y+z*z)
    a = z/r
    theta = math.acos(a)
    phi = math.atan2(y,x)
    pol = [r,theta,phi]
    return pol

axisDict = {
                1 : [True, False, False, False, False, False, False],
                2 : [False, True, False, True, False, False, False],
                3 : [True, True, False, True, False, False, False],
                6 : [True, True, False, True, True, True, True],
                7 : [True,True,True,True,True,True, True]
    }
class botEnv:
    

    
    
    def __init__(self, startPos=[0,0,0], maxVelocity = .35, stepSize = 1, numAxis = 3, mode = 0):

        self.maxVelocity = maxVelocity
        self.maxForce = 300
        self.startPosition = startPos
        self.stepSize = stepSize * (math.pi/180)
        self.startOrientation =p.getQuaternionFromEuler([0.,0.,0.])
        self.jointPosition = [0,0,0,0,0,0,0]
        self.stepStartPosition = [0.,0.,0.]
        self.stepStartOrientation = [0., 0., 0.]
        self.numAxis = numAxis
        self.moveDir = [0,0,0,0,0,0,0]
        self.jointZOffset = 0.36
        self.jumpFlag = False
        self.moveFlag = False
        self.collisionFlag = False
        self.botScore = 0.
        self.orientationScore = [0., 0., 0.]
        self.setup()
        self.exist = True
        
        
    def setup(self):#Loads Plane and Robot, determins number of Joints and their upper and lower bounds. Sets Robot to starting Position
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeId = p.loadURDF("plane.urdf")
        self.botId = p.loadURDF("kuka_iiwa/model.urdf", self.startPosition, self.startOrientation)
        self.numJoints = p.getNumJoints(self.botId)
        self.moveable = axisDict[self.numAxis]
        #print(self.numJoints)
        self.upperLimits = []
        self.lowerLimits = []
        for i in range(self.numJoints):
            self.upperLimits.append(p.getJointInfo(self.botId, i)[9])
            self.lowerLimits.append(p.getJointInfo(self.botId, i)[8])
            p.setJointMotorControl2(self.botId, i, p.POSITION_CONTROL, targetPosition=self.jointPosition[i])

        
            
    def setStepStart(self):
        self.stepStartPosition = self.getBotHeadPos()
        self.stepStartOrientation = self.getBotHeadOrientation()
        
    
    def setMovement(self, actions): #Interpretiert die Outputs des knN und ordnet sie den Achsen zu
        if len(actions) != self.numAxis:
            print('Anzahl verwendeter Achsen stimmt nicht mit Outputs des knN überein')
        else:
            aIndex = 0
            for i in range(len(self.moveDir)):
                if self.moveable[i]:
                    self.moveDir[i] = (actions[aIndex]-0.5) * 2
                    aIndex += 1
                else:
                    self.moveDir[i] = 0
                
        
            
    def moveStep(self): #Führt die Drehung der Achsen aus, entfernt Roboter bei Kollision
        if not self.collisionFlag:
            for index in range(self.numJoints):
                if self.moveable[index]:
                    self.jointPosition[index] += (self.moveDir[index]*self.stepSize)
                    if self.jointPosition[index] < self.lowerLimits[index]:
                        self.jointPosition[index] = self.lowerLimits[index]
                    elif self.jointPosition[index] > self.upperLimits[index]:
                        self.jointPosition[index]= self.upperLimits[index]
                else:
                    self.jointPosition[index] = 0
                p.setJointMotorControl2(self.botId, index, p.POSITION_CONTROL, targetPosition=self.jointPosition[index])
        if self.collisionFlag:
            p.removeBody(self.botId)
    
    
    def getBotHeadPos(self): #Bestimmt Position des Endeffektors in kartesischen Koordinaten relative zur Basisposition
        headPos = [0., 0., 0.]
        headAbs = p.getLinkState(self.botId, self.numJoints - 1)[0]
        for i in range(3):
            headPos[i] = headAbs[i] - self.startPosition[i] 
        return headPos
        
    def getBotSpherical(self): #Bestimmt Position des Endeffektors in räumlichen Polarkoordinaten relative zu Achse 2
        endeffectorPos = list(p.getLinkState(self.botId, self.numJoints - 1)[0])
        endeffectorPos[2] = endeffectorPos[2]-self.jointZOffset
        relativePos = []
        for pos in range(3):
            relativePos.append(endeffectorPos[pos] - self.startPosition[pos])
        sphericalCoordinates = cartToSpher(relativePos[0], relativePos[1], relativePos[2])
        return sphericalCoordinates
        
    def getBotHeadOrientation(self): #Ausrichtung des Endeffektors in eulerschen Winkeln
        orientation = list(p.getEulerFromQuaternion(p.getLinkState(self.botId,self.numJoints-1)[1]))
        return orientation       
        
    def calcOrientationDistance(self, startOrientation):
        diffOrientation = [0., 0., 0.]
        isOrientation = self.getBotHeadOrientation()
        for i in range(3):
            diffOrientation[i] = abs(startOrientation[i] - isOrientation[i])
        return diffOrientation
    
    def botReset(self):
            if not self.collisionFlag:
                self.moveDir = [0,0,0,0,0,0,0]
                for i in range (self.numJoints):
                    p.resetJointState(self.botId, i, 0)
                self.jointPosition = [0,0,0,0,0,0,0]