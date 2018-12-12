import pygame as pg
import random

import Model.main as model
from EventManager import *
from View.const import *
from MainConst import *

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
        """
        TASK 1
        """
        self.image = {'background': None,
                      'message': None,
                      'base': None,
                      'bird': None,
                      'lowerPipe': None,
                      'upperPipe': None,
                      'number': None,
                      'gameover': None}

        self.audio = {'die': None,
                      'hit': None,
                      'wing': None,
                      'point': None,
                      'swooth': None}
        """
        BONUS 3 & BONUS 4
        self.backgroundType = 0
        self.birdType = 0
        self.pipeType = 0
        self.wing = 0
        self.swingVal = 0
        self.swingDir = 0
        """

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            elif cur_state == model.STATE_PLAY:
                self.render_play()
                self.render_score()
            elif cur_state == model.STATE_STOP:
                self.render_stop()
                self.render_score()
            elif cur_state == model.STATE_DEAD:
                self.render_dead()
                self.render_score()
            # update surface
            pg.display.flip()
            # show the programs FPS in the window handle
            caption = "{} - FPS: {:.2f}".format(GameCaption, self.clock.get_fps())
            pg.display.set_caption(caption)
            # limit the redraw speed to 30 frames per second
            self.clock.tick(FramePerSec)
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Jump):
            self.audio['wing'].play()
        elif isinstance(event, Event_Score):
            self.audio['point'].play()
        elif isinstance(event, Event_Hit):
            self.audio['hit'].play()
            self.audio['die'].play()
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pg.quit()
        """
        BONUS 5
        """

    def render_menu(self):
        """
        Render the game menu.
        """
        """
        TSAK 1 & BONUS 3 & BONUS 4
        """
        # background
        self.screen.blit(self.image['background'], (0, 0))

        # moving base
        self.screen.blit(self.image['base'], (self.model.baseX, self.model.baseY))
        self.screen.blit(self.image['base'], (self.model.baseX-ScreenSize[0], self.model.baseY))

        # messsage
        (messageX, messageY) = self.image['message'].get_size()
        self.screen.blit(self.image['message'], (ScreenSize[0]*0.5-messageX*0.5, ScreenSize[1]*0.4-messageY*0.5))

        # moving bird
        self.screen.blit(self.image['bird'][BirdWing[self.model.birdState]], (self.model.birdX, self.model.birdY))

    def render_play(self):
        """
        Render the game play.
        """
        """
        TASK 1 & TASK 5 & BONUS 4
        """
        # background
        self.screen.blit(self.image['background'], (0, 0))

        # moving base
        self.screen.blit(self.image['base'], (self.model.baseX, self.model.baseY))
        self.screen.blit(self.image['base'], (self.model.baseX-ScreenSize[0], self.model.baseY))
        
        # moving pipes
        for i in range(0, len(self.model.pipes), 2):
            self.screen.blit(self.image['upperPipe'], (self.model.pipes[i], self.model.pipes[i+1]))
            self.screen.blit(self.image['lowerPipe'], (self.model.pipes[i], self.model.pipes[i+1]+model.PipeGap+model.PipeHeight))
       
        # moving bird
        self.screen.blit(self.image['bird'][BirdWing[self.model.birdState]], (self.model.birdX, self.model.birdY))

    def render_stop(self):
        """
        Render the stop screen.
        """
        """
        TASK 1 & TASK 5
        """
        # background
        self.screen.blit(self.image['background'], (0, 0))

        # base
        self.screen.blit(self.image['base'], (self.model.baseX, self.model.baseY))
        self.screen.blit(self.image['base'], (self.model.baseX-ScreenSize[0], self.model.baseY))
       
        # pipes
        for i in range(0, len(self.model.pipes), 2):
            self.screen.blit(self.image['upperPipe'], (self.model.pipes[i], self.model.pipes[i+1]))
            self.screen.blit(self.image['lowerPipe'], (self.model.pipes[i], self.model.pipes[i+1]+model.PipeGap+model.PipeHeight))

        # bird
        self.screen.blit(self.image['bird'][BirdWing[self.model.birdState]], (self.model.birdX, self.model.birdY))

    def render_dead(self):
        """
        Render the dead screen.
        """
        # background
        self.screen.blit(self.image['background'], (0, 0))

        # base
        self.screen.blit(self.image['base'], (self.model.baseX, self.model.baseY))
        self.screen.blit(self.image['base'], (self.model.baseX-ScreenSize[0], self.model.baseY))
        
        # pipes
        for i in range(0, len(self.model.pipes), 2):
            self.screen.blit(self.image['upperPipe'], (self.model.pipes[i], self.model.pipes[i+1]))
            self.screen.blit(self.image['lowerPipe'], (self.model.pipes[i], self.model.pipes[i+1]+model.PipeGap+model.PipeHeight))

        # bird
        self.screen.blit(self.image['bird'][BirdWing[self.model.birdState]], (self.model.birdX, self.model.birdY))

        # messsage
        (messageX, messageY) = self.image['gameover'].get_size()
        self.screen.blit(self.image['gameover'], (ScreenSize[0]*0.5-messageX*0.5, ScreenSize[1]*0.4-messageY*0.5))

        """
        TASK 1 & TASK 5
        """
        
    def render_score(self):
        """
        TASK 5 & BONUS 2
        """
        score = self.model.score
        numbers = []
        while score > 0:
            numbers.append(score % 10)
            score //= 10

        if len(numbers) == 0:
            numbers.append(0)
        numbers = numbers[::-1]
        numX = ScreenSize[0] * 0.5 - 24 * len(numbers) * 0.5
        numY = ScreenSize[1] * 0.15
        for num in numbers:
            self.screen.blit(self.image['number'][num], (numX, numY))
            numX += 24


    def decide_type(self):
        """
        BONUS 5
        """
        pass

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 20)
        self.bigfont = pg.font.Font(None, 60)
        self.isinitialized = True
        """
        TASK 1 & BONUS 2 & BONUS 3 & BONUS 5
        """
        self.image = {'background': pg.image.load(ImagePath['background'][self.model.backgroundType]),
                      'message': pg.image.load(ImagePath['message']),
                      'base': pg.image.load(ImagePath['base']),
                      'bird': [pg.image.load(ImagePath['bird'][self.model.birdType][i]) for i in range(3)],
                      'lowerPipe': pg.image.load(ImagePath['pipe'][self.model.pipeType][0]),
                      'upperPipe': pg.image.load(ImagePath['pipe'][self.model.pipeType][1]),
                      'number': [pg.image.load(ImagePath['number'][i]) for i in range(10)],
                      'gameover': pg.image.load(ImagePath['gameover'])}

        self.audio = {'die': pg.mixer.Sound(AudioPath['die'][1]),
                      'hit': pg.mixer.Sound(AudioPath['hit'][1]),
                      'wing': pg.mixer.Sound(AudioPath['wing'][1]),
                      'point': pg.mixer.Sound(AudioPath['point'][1]),
                      'swooth': pg.mixer.Sound(AudioPath['swoosh'][1])}

