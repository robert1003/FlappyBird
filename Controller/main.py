import pygame as pg

import Model.main as model
from EventManager import *
from MainConst import *

class Control(object):
    """
    Handles control input.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            # Called for each game tick. We check our keyboard presses here.
            for event in pg.event.get():
                # handle window manager closing our window
                if event.type == pg.QUIT:
                    self.evManager.Post(Event_Quit())
                # handle key down events
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.ctrl_menu(event)
                    elif cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    elif cur_state == model.STATE_STOP:
                        self.ctrl_stop(event)
                    elif cur_state == model.STATE_DEAD:
                        self.ctrl_dead(event)
        elif isinstance(event, Event_Initialize):
            self.initialize()

    def ctrl_menu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            # escape closes the game
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # space plays the game
            elif event.key == pg.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_play(self, event):
        """
        Handles play events.
        """
        if event.type == pg.KEYDOWN:
            # escape pops the menu
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
                """
                BONUS 5
                """
                self.evManager.Post(Event_Initialize())
            # key p to stop the game
            elif event.key == pg.K_p:    
                self.evManager.Post(Event_StateChange(model.STATE_STOP))
            elif event.key == pg.K_SPACE or event.key == pg.K_UP:
                self.evManager.Post(Event_Jump())
            #TASK 3
            #elif event.key == pg.K_SPACE:
             #   self.evManager.Post(Event_Jump())

    def ctrl_stop(self, event):
        """
        Handles stop events.
        """
        if event.type == pg.KEYDOWN:
            # key p to return the game
            if event.key == pg.K_p:
                self.evManager.Post(Event_StateChange(None))

    def ctrl_dead(self, event):
        """
        Handles dead events.
        """
        """
        TASK 4 & BONUS 1 & BONUS 5
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
                self.evManager.Post(Event_StateChange(None))
            elif event.key == pg.K_SPACE:
                rectBird = pg.Rect(self.model.birdX, self.model.birdY, 34, 24)
                rectBase1 = pg.Rect(self.model.baseX, self.model.baseY, 336, 112)
                rectBase2 = pg.Rect(self.model.baseX - ScreenSize[0], self.model.baseY, 336, 112)

                if rectBird.colliderect(rectBase1) or rectBird.colliderect(rectBase2):
                    self.evManager.Post(Event_StateChange(None))
                    #self.evManager.Post(Event_StateChange(model.STATE_PLAY))
                    self.evManager.Post(Event_Initialize())

    def initialize(self):
        """
        init pygame event
        """
        pass