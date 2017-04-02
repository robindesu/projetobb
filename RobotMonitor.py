from Robot import Robot
from ObjectDetectionListener import IObjectDetectionListener
from ObjectDetectionListener import DetectedObject
from PositionListener import IPositionListener
from time import sleep
import threading
from typing import List


class RobotMonitor(threading.Thread):
    def __init__(self, robot: Robot, stopEvent: threading.Event, intervalMs=200):
        threading.Thread.__init__(self)
        self.robot = robot
        self.intervalSeconds = intervalMs/1000
        self.stopEvent = stopEvent
        self.frontObjDetecListeners = []
        self.positionListeners = []

    def run(self):
        while not self.stopEvent.is_set():
            self.robot.update()
            self.readSonarReadings()  
            self.readPosition()    
            sleep(self.intervalSeconds)

    def readSonarReadings(self):
        #FIXME: robot should know the position of each sonar
        # 0: 90
        # 1: 50
        # 2: 30
        # 4: 10
        # 5: -10
        # ...
        angles = [90, 50, 30, 10, -10, -30, -50, -90]
        detectedObjs = []
        for i in range(0,8):
            if self.robot.sonarReading[i] != -1:
                detectedObjs.append(DetectedObject(self.robot.sonarReading[i], angles[i]))

        self.__frontObjectDetected(detectedObjs)

    def readPosition(self):
        if self.robot.lastPosition != self.robot.position:
            self.__positionChanged(self.robot.position)

    def subscribeToFrontObjectDetection(self, listener: IObjectDetectionListener ):
        self.frontObjDetecListeners.append(listener)
    
    def subscribeChangePosition(self, listener: IPositionListener):
        self.positionListeners.append(listener)

    def __frontObjectDetected(self, detectedObjs: List[DetectedObject]):
        for l in self.frontObjDetecListeners:
            l.objectDetected(detectedObjs)
    
    def __positionChanged(self, newPosition):
        for l in self.positionListeners:
            l.newPosition(newPosition)
            