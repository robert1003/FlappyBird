import pygame as pg
import random

from EventManager import *
from Model.GameObject import *
from Model.StateMachine import *
from Model.const import *
from MainConst import *

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AIList):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            player (list.player()): all player object.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AIList = AIList
        self.player = []

        self.time = None
        self.preciseTime = None
        self.baseX = None
        self.baseY = None
        self.backgroundType = None
        self.birdType = None
        self.birdState = None
        self.birdX = None
        self.birdY = None
        self.birdVel = None
        self.swingVal = 1
        self.swingDir = 0
        self.swingMax = 16
        self.pipeType = None
        self.pipes = None
        self.score = None

        """
        TASK 1 & TASK 2 & TASK 3 & TASK 5
        self.size = {'bird': None,
                     'lowerPipe': None}
        self.pos = {'message': {'x': 0, 'y': 0},
                    'base': {'x': 0, 'y': 0},
                    'bird': {'x': 0, 'y': 0},
                    'gameover': {'x': 0, 'y': 0},
                    'lowerPipe': None,
                    'upperPipe': None}
        self.baseShift = 0
        self.vel = 0
        self.score = 0
        """

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_StateChange):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_MENU:
                self.birdY += self.swingVal
                self.swingDir += self.swingVal
                if abs(self.swingDir) >= self.swingMax:
                    self.swingVal = -self.swingVal

                self.updateBase()
                self.updateBird()
                self.time += 1
            elif cur_state == STATE_PLAY:
                if self.checkscore():
                    self.evManager.Post(Event_Score())
                self.birdY += self.birdVel
                self.birdVel = min(self.birdVel + 1, MaxVel)
                self.updateBase()
                self.updateBird()
                self.updatePipe()
                self.time += 1

                if self.checkcrash():
                    self.evManager.Post(Event_Hit())
                    self.evManager.Post(Event_StateChange(None))
                    self.evManager.Post(Event_StateChange(STATE_DEAD))
            elif cur_state == STATE_STOP:
                pass
            elif cur_state == STATE_DEAD:
                if self.birdY + 24 <= self.baseY:
                    self.updateBird()
                    self.birdY += MaxVel
        elif isinstance(event, Event_Jump):
            self.birdVel = FlapVel
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Quit):
            self.running = False
        """
        TASK 2 & TASK 3 & TASK 4 & TASK 5
        """

    def getRandomPipe(self):
        """
        TASK 2
        """
        pass

    def updateBase(self):
        """
        TASK 2
        """
        self.baseX = (self.baseX - MainSpeed) % ScreenSize[0]

    def updatePipe(self):
        """
        TASK 2
        """
        # update pipes
        for i in range(0, len(self.pipes), 2):
            self.pipes[i] -= MainSpeed

        # remove old pipes
        if len(self.pipes) > 0 and self.pipes[0] + PipeWidth < 0:
            self.pipes.remove(self.pipes[0])
            self.pipes.remove(self.pipes[0])
        
        # insert new pipes
        if len(self.pipes) <= 0 or self.pipes[-2] + PipeWidth + 100 < ScreenSize[0]:
            self.pipes.append(ScreenSize[0])
            self.pipes.append(random.randint(-220, 0))


    def updateBird(self):
        """
        TASK 3
        """
        if self.time % 3 == 0:
            self.birdState = (self.birdState + 1 ) % 4

    def checkcrash(self):
        """
        TASK 4
        """
        rectBird = pg.Rect(self.birdX, self.birdY, 34, 24)
        for i in range(0, len(self.pipes), 2):
            rectPipe1 = pg.Rect(self.pipes[i], self.pipes[i+1], PipeWidth, PipeHeight)
            rectPipe2 = pg.Rect(self.pipes[i], self.pipes[i+1] + PipeHeight + PipeGap, PipeWidth, PipeHeight)

            if rectBird.colliderect(rectPipe1) or rectBird.colliderect(rectPipe2):
                return True
            
        rectBase1 = pg.Rect(self.baseX, self.baseY, 336, 112)
        rectBase2 = pg.Rect(self.baseX - ScreenSize[0], self.baseY, 336, 112)

        if rectBird.colliderect(rectBase1) or rectBird.colliderect(rectBase2):
            return True

        return False

    def restart(self):
        """
        TASK 4 & TASK 5
        """
        pass

    def checkscore(self):
        """
        TASK 5
        """
        for i in range(0, len(self.pipes), 2):
            if self.birdX + 17 - self.pipes[i] - 26 < 5 and self.birdX + 17 - self.pipes[i] - 26 > 0:
                self.score += 1
                return True

        return False

    def initialize(self):
        """
        init pygame event
        """
        """
        TASK 1 & TASK 2 & TASK 3
        """
        self.time = 1
        self.preciseTime = 22.09
        self.baseX = 0
        self.baseY = ScreenSize[1]*0.8
        self.backgroundType = random.randint(0, 1)
        self.birdType = random.randint(0, 2)
        self.birdState = 0
        self.birdX = 40
        self.birdY = 244
        self.birdVel = 0
        self.pipeType = random.randint(0, 1)
        self.pipes = []
        self.score = 0

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)