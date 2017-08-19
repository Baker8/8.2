# imports and stuff
#THINGS TO DO IN ORDERS OF IMPORTANCE

#what gameplay to have?
#Notes coming from above. Trying to bop eachother into notes. Need to navigate all the way right to left to gain score.
#make bopper sprites that can only collide once with stuff and then can't be used for a while. ONLY COLLIDE ONCE OR ELSE STUFF GETS REAL WEIRD REAL FAST

#also checking to see what midis are already stored in there




import pygame, sys
from mido import MidiFile
from pygame.locals import *
import GLOBALS
import random
import re
import mido

class Note(pygame.sprite.Sprite):
    def __init__(self, width, color, length, channel, time):
        pygame.sprite.Sprite.__init__(self)                             #overlap correction?
        self.image = pygame.Surface([int((resolution.current_w)/score_range), int(width * GLOBALS.SpeedOMeter)])
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.length = length
        self.channel = channel
        self.height = int((resolution.current_w)/score_range)
        self.time = 0
        self.image.set_alpha(180)
        self.width = width

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.color = color
        self.width = width
        self.height = height
        """Above is necessary, below, not so much"""
        self.image.fill(self.color)

        self.vspeed = 0
        self.hspeed = 0
        self.grounded = False
        self.crouched = False
        self.score = 8
        self.deathanim = False
        self.deathanimtimer = 50
        self.crouchframes = 180

    def jump(self):
        if self.grounded == True:
            self.grounded = False
            self.vspeed = -GLOBALS.jumpspeed
    def right(self):
        if self.grounded:
            self.hspeed = GLOBALS.player_speed
            if self.crouched:
                self.hspeed -= GLOBALS.player_speed/GLOBALS.crouch_scaler
        else:
            if self.hspeed < GLOBALS.player_speed:
                self.hspeed += (GLOBALS.player_speed) / GLOBALS.air_control
    def left(self):
        if self.grounded:
            self.hspeed = -GLOBALS.player_speed
            if self.crouched:
                self.hspeed += GLOBALS.player_speed/GLOBALS.crouch_scaler
        else:
            if self.hspeed > -GLOBALS.player_speed:
                self.hspeed -= GLOBALS.player_speed / GLOBALS.air_control
    def crouch(self):
        if self.crouched == False:
            self.crouched = True
            self.image.set_alpha(100)

    def uncrouch(self):
        if self.crouched == True:
            self.crouched = False
            self.image.set_alpha(255)

    def bopped(self, direction):
        if direction == 'left':
            self.hspeed = -GLOBALS.bop_force_h
        else:
            self.hspeed = GLOBALS.bop_force_h
        self.vspeed = -GLOBALS.bop_force_v


    def deathanimation(self):
        if self.deathanim == False:
            self.deathanim = True

class Bopper(pygame.sprite.Sprite):
    def __init__(self, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([GLOBALS.bopper_length, GLOBALS.bopper_width])
        self.rect = self.image.get_rect()
        self.color = GLOBALS.bopper_color

        """Above is necessary, below, not so much"""
        self.image.fill(self.color)
        self.deathanim = False
        self.deathanimtimer = 50
        self.rect.x = 0
        self.rect.y = 0
        self.owner = owner
        self.jabbing = False
        self.jabout = False
        self.jabin = False
        self.jabdirection = ""

    def deathanimation(self):
        if self.deathanim == False:
            self.deathanim = True

    def follow(self):
        if self.owner == 'player1':
            self.rect.x = player1.rect.x - (GLOBALS.bopper_length - GLOBALS.player_width)/2
            self.rect.y = player1.rect.y + GLOBALS.bopper_height
        elif self.owner == 'player2':
            self.rect.x = player2.rect.x - (GLOBALS.bopper_length - GLOBALS.player_width)/2
            self.rect.y = player2.rect.y + GLOBALS.bopper_height

    def jab(self, direction):
        if self.jabbing == False:
            if direction == 'left':
                print("leftjab")
                self.jabdirection = 'left'
                self.jabout = True
                self.jabbing = True
            else:
                print('rightjab')
                self.jabdirection = 'right'
                self.jabout = True
                self.jabbing = True



pygame.init()
resolution = pygame.display.Info()
pygame.display.set_caption('KlangfarbenMIDI')
DISPLAYSURF = pygame.display.set_mode((resolution.current_w, (resolution.current_h - 42)))
clock = pygame.time.Clock()
outport = mido.open_output("SimpleSynth virtual input")


def ROYALRESET():

    pygame.mixer.music.stop()

    # key inputs
    global e
    e = False
    global d
    d = False
    global s
    s = False
    global f
    f = False

    global i
    i = False
    global j
    j = False
    global k
    k = False
    global l
    l = False

    global g
    g = False
    global a
    a = False

    global h
    h = False
    global semicolon
    semicolon = False



    global START_GAME
    START_GAME = False
    global settings
    settings = False
    global LOAD_GAME
    LOAD_GAME = False
    global readytostart
    readytostart = False
    global homescreen
    homescreen = True
    global notdone
    notdone = False

    global speed_settings
    speed_settings = False

    global midi_settings
    midi_settings = False

    global myfont
    myfont = pygame.font.Font(None, 80)

    global CLOCK
    CLOCK = 60

    global note_list
    note_list = pygame.sprite.Group()

    global player_list
    player_list = pygame.sprite.Group()

    global misc_list
    misc_list = pygame.sprite.Group()

    global barz_list
    barz_list = pygame.sprite.Group()

    global bopper_list
    bopper_list = pygame.sprite.Group()




    global score_range  #scales the score based on min/max in particular midi
    score_range = 88

    global scalar
    scalar = []

    global currentmusicname
    currentmusicname = "midis/" + musicinputname + ".mid"

    global currentmusic
    currentmusic = MidiFile("midis/" + musicinputname + ".mid")

    global notestobeplayed
    notestobeplayed = []

    global firetime
    firetime = 0

    global list_of_messages
    list_of_messages = []

    global pre_note_list
    pre_note_list = []

global musicinputname
musicinputname = GLOBALS.MUSIC

ROYALRESET()

window_height = resolution.current_h - 90

latest = int(-(window_height/2) / GLOBALS.SpeedOMeter)

while True:
    clock.tick(CLOCK)
    DISPLAYSURF.fill((0, 0, 0))

    if START_GAME:
        latest += 1
        p1score_label = myfont.render(str(int(player1.score)), 1, (255, 0, 0))
        p2score_label = myfont.render(str(int(player2.score)), 1, (0, 0, 255))




        """SCores look annonying"""




            #just gotta set correct start position and line up the music to boot. I"m seeing more unit conversions in the future
        for note in pre_note_list:
            #print(note)
            if note[1] * 60 < latest + ((window_height/2) / GLOBALS.SpeedOMeter):
                            #WIDTH          COLOR     LENGTH                                  channel   time
                newnote = Note(note[2] * CLOCK, note[4], (note[2] * GLOBALS.SpeedOMeter * CLOCK), note[3], note[0])
                newnote.rect.x = int((note[0] - int(minscalar) + 1) * (resolution.current_w / (score_range + 1))) - resolution.current_w/score_range
                newnote.rect.y = 0 - int(note[2] * CLOCK * GLOBALS.SpeedOMeter)
                note_list.add(newnote)
                pre_note_list.remove(note)


        for noteything in note_list:
            noteything.rect.y += GLOBALS.SpeedOMeter
            if noteything.rect.y > - int(noteything.length * CLOCK * GLOBALS.SpeedOMeter):
                if noteything.rect.y > window_height + noteything.length:
                    noteything.kill()
                else:
                    misc_list.add(noteything)

        FIRE = []
        for note in notestobeplayed:
            if note.time * 60 < latest:
                FIRE.append(note)
                notestobeplayed.remove(note)

        for firing in FIRE:
            outport.send(firing)


        for player in player_list:

            note_collisions = pygame.sprite.spritecollide(player, note_list, False)
            player.grounded = False


            if player.crouched == True:
                player.crouchframes -= 1
            else:
                if player.crouchframes <= 200:
                    player.crouchframes += 0.2
                for note in note_collisions:
                    player.deathanimation()
            if player.crouchframes <= 0:
                player.uncrouch()


            if player.deathanim == True:
                player.vspeed = 0
                player.hspeed = 0
                if player.deathanimtimer > 0:
                    if latest % 2 == 0:
                        player.image.fill(player.color)
                    else:
                        player.image.fill(GLOBALS.YELLOW)
                    player.deathanimtimer -= 1
                else:
                    player.image.fill(player.color)
                    player.crouchframes = 400
                    player.crouch()
                    player.rect.x = random.randint(0, resolution.current_w - GLOBALS.player_width)
                    player.rect.y = 100
                    player.deathanim = False
                    player.deathanimtimer = 50
                    player.score -= 1




            #KEEPING IN BOUNDS
            if player.rect.y + GLOBALS.player_height > window_height:
                player.grounded = True
                player.rect.y = window_height - GLOBALS.player_height
            if player.rect.x <= 0:
                player.rect.x = 0
            if player.rect.x >= resolution.current_w - GLOBALS.player_width:
                player.rect.x = resolution.current_w - GLOBALS.player_width
            if player.grounded:
                player.vspeed = 0
                if player.hspeed > 4:
                    player.hspeed -= 4
                elif player.hspeed < -4:
                    player.hspeed += 4
                else:
                    player.hspeed = 0
            else:
                player.vspeed += GLOBALS.fallspeed


        for bopper in bopper_list:
            bopper.follow()
            bop = pygame.sprite.spritecollide(bopper, player_list, False)

            if bopper.owner == 'player1' and player2 in bop and player2.crouched == False and player1.crouched == False:
                print("2 bop'd")
                if player1.rect.x > player2.rect.x:
                    player2.bopped('left')
                else:
                    player2.bopped('right')
            elif bopper.owner == 'player2' and player1 in bop and player1.crouched == False and player2.crouched == False:
                print("1 bop'd")
                if player2.rect.x > player1.rect.x:
                    player1.bopped('left')
                else:
                    player1.bopped('right')
        #MOVEMENT
        if f:
            player1.right()
        if s:
            player1.left()
        if e:
            player1.jump()

        if l:
            player2.right()
        if j:
            player2.left()
        if i:
            player2.jump()




        #P1 bopper
        '''
        if g:
            
        
        if a:
        
        #p2 bopper
        if h:
        
        if semicolon:
        '''


        misc_list.draw(DISPLAYSURF)
        barz_list.draw(DISPLAYSURF)
        DISPLAYSURF.blit(p1score_label, (20, window_height + 0))
        DISPLAYSURF.blit(p2score_label, (resolution.current_w - 40, window_height + 0))
        bopper_list.draw(DISPLAYSURF)

        # crouch bars

        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), [80, window_height + 8, player1.crouchframes * 1.2, resolution.current_h])
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255),
                         [resolution.current_w - 80, window_height + 8, -player2.crouchframes * 1.2, resolution.current_h])

        player1.rect.x += int(player1.hspeed)
        player1.rect.y += int(player1.vspeed)
        player2.rect.x += int(player2.hspeed)
        player2.rect.y += int(player2.vspeed)


        for event in pygame.event.get():

            #KILL ALL AND GO BACK TO MAIN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    f = True
                elif event.key == pygame.K_s:
                    s = True
                elif event.key == pygame.K_e:
                    e = True
                elif event.key == pygame.K_d:
                    if player1.crouchframes > 0:
                        player1.crouch()
                        player1.crouchframes -= 2


                elif event.key == pygame.K_l:
                    l = True
                elif event.key == pygame.K_j:
                    j = True
                elif event.key == pygame.K_i:
                    i = True
                elif event.key == pygame.K_k:
                    if player2.crouchframes > 0:
                        player2.crouch()
                        player2.crouchframes -= 2


                elif event.key == pygame.K_g:
                    g = True
                elif event.key == pygame.K_a:
                    a = True

                elif event.key == pygame.K_h:
                    h = True
                elif event.key == pygame.K_SEMICOLON:
                    semicolon = True

                elif event.key == pygame.K_ESCAPE:
                    for entry in misc_list:
                        entry.remove(misc_list)
                        entry.remove(note_list)
                        entry.remove(player_list)
                        entry.kill()
                    ROYALRESET()
                    outport.panic()
                    outport.close()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    f = False
                elif event.key == pygame.K_s:
                    s = False
                elif event.key == pygame.K_e:
                    e = False
                elif event.key == pygame.K_d:
                    d = False
                    player1.uncrouch()

                if event.key == pygame.K_l:
                    l = False
                elif event.key == pygame.K_j:
                    j = False
                elif event.key == pygame.K_i:
                    i = False
                elif event.key == pygame.K_k:
                    k = False
                    player2.uncrouch()

                elif event.key == pygame.K_g:
                    g = False
                elif event.key == pygame.K_a:
                    a = False

                elif event.key == pygame.K_h:
                    h = False
                elif event.key == pygame.K_SEMICOLON:
                    semicolon = False

            #important
            elif event.type == QUIT:
                outport.panic()
                outport.close()
                pygame.quit()
                sys.exit()

    else:

        #working fine but need to add the creaton of note played class objects
        if LOAD_GAME:
            readytostart = True
            LOAD_GAME = False
            filevents = []
            print("reading file...")
            file = open("infomidi/"+musicinputname, "r")
            filevents = file.read()
            file.close()
            rangefinder = filevents.find("&")
            score_range = filevents[1:int(rangefinder)]
            score_range = int(score_range)
            minfinder = filevents.find("$")
            minscalar = filevents[8:int(minfinder)]
            minscalar = minscalar.strip()
            filevents = filevents[int(minfinder)+4:len(filevents)-2]
            filevents = filevents.split("), (")
            print(str(filevents))

            notefile = open("infomidi/" + musicinputname + "MUSICLINE", 'r')
            raw = notefile.read()
            list_of_messages = raw.split("@")
            list_of_messages = list_of_messages[:-1]

            firetime = 0

            for entry in list_of_messages:
                if "meta message" in entry:  # meta messages appear to mean absolutely nothing
                    entry = re.split(' |=', entry)
                    entry = mido.MetaMessage('key_signature', key='Eb',
                                             time=float(entry[len(entry) - 1][0:len(entry[len(entry) - 1]) - 1]))
                else:
                    entry = re.split(' |=', entry)
                    if "note_on" in entry:
                        sleep = float(entry[8])
                        entry = mido.Message('note_on', channel=int(entry[2]), note=int(entry[4]),
                                             velocity=int(entry[6]), time=float(entry[8]))
                        # print("on")
                    elif "note_off" in entry:
                        sleep = float(entry[8])
                        entry = mido.Message('note_off', channel=int(entry[2]), note=int(entry[4]),
                                             velocity=int(entry[6]), time=float(entry[8]))
                        # print("off")
                    elif 'control_change' in entry:
                        sleep = float(entry[8])
                        entry = mido.Message('control_change', channel=int(entry[2]), control=int(entry[4]),
                                             value=int(entry[6]), time=float(entry[8]))
                        # print("control")
                    elif 'program_change' in entry:
                        sleep = float(entry[6])
                        entry = mido.Message('program_change', channel=int(entry[2]), program=int(entry[4]),
                                             time=float(entry[6]))
                        # print("program")
                    elif 'pitchwheel' in entry:
                        sleep = float(entry[6])
                        entry = mido.Message('pitchwheel', channel=int(entry[2]), pitch=int(entry[4]),
                                             time=float(entry[6]))
                        # print('pitchwheel')
                    else:
                        print("UNDEFINED MESSAGE    " + str(entry))
                firetime += entry.time
                entry.time = firetime
                notestobeplayed.append(entry)


            for note_values in filevents:
                eachof4 = note_values.split(", ")
                STO4 = (int(eachof4[0]), float(eachof4[1]), float(eachof4[2]), int(eachof4[3]))
                if STO4[3] == 0:
                    color = GLOBALS.channel0color
                elif STO4[3] == 1:
                    color = GLOBALS.channel1color
                elif STO4[3] == 2:
                    color = GLOBALS.channel2color
                elif STO4[3] == 3:
                    color = GLOBALS.channel3color
                elif STO4[3] == 4:
                    color = GLOBALS.channel4color
                elif STO4[3] == 5:
                    color = GLOBALS.channel5color
                elif STO4[3] == 6:
                    color = GLOBALS.channel6color
                elif STO4[3] == 7:
                    color = GLOBALS.channel7color
                elif STO4[3] == 8:
                    color = GLOBALS.channel8color
                elif STO4[3] == 9:  #ew drums gross
                    color = GLOBALS.channel9color
                elif STO4[3] == 10:
                    color = GLOBALS.channel10color
                elif STO4[3] == 11:
                    color = GLOBALS.channel11color
                elif STO4[3] == 12:
                    color = GLOBALS.channel12color
                elif STO4[3] == 13:
                    color = GLOBALS.channel13color
                elif STO4[3] == 14:
                    color = GLOBALS.channel14color
                elif STO4[3] == 15:
                    color = GLOBALS.channel15color
                else:
                    color = GLOBALS.WHITE
                STO4 = (int(eachof4[0]), float(eachof4[1]), float(eachof4[2]), int(eachof4[3]), color)
                pre_note_list.append(STO4)


    #"""

        #also working fine
        elif readytostart: #after it loads but before you actually go
            MAINGAME_LABEL = myfont.render("Ready to start", 1, (255, 255, 255))
            DISPLAYSURF.blit(MAINGAME_LABEL, (int(resolution.current_w / 2) - 200, 20))
            pygame.display.update()
            started = False
            while started == False:
                broke = False
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_SPACE:
                            started = True
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            START_GAME = True
            print("playersetup")
            player1 = Player((255, 0, 0), GLOBALS.player_width, GLOBALS.player_height)
            player1.rect.y = 50
            player1.rect.x = 100
            player_list.add(player1)
            player2 = Player((0, 0, 255), GLOBALS.player_width, GLOBALS.player_height)
            player2.rect.y = 50
            player2.rect.x = resolution.current_w - 100
            player_list.add(player2)
            misc_list.add(player1)
            misc_list.add(player2)

            barz = Player((88, 88, 88), resolution.current_w, 2)
            barz.rect.y = window_height/2
            barz.rect.x = 0
            misc_list.add(barz)

            p1bopper = Bopper("player1")
            bopper_list.add(p1bopper)

            p2bopper = Bopper("player2")
            bopper_list.add(p2bopper)

            bottomcover = Player((0, 0, 0), resolution.current_w, 50)
            bottomcover.rect.y = resolution.current_h - 90
            barz_list.add(bottomcover)

        elif settings:

            """THIS THING IS GETTING SPAGHETTIFIED IN ORDER TO LOAD STUFF OUTSIDE THE ACTUAL GAME"""
            MAINGAME_LABEL = myfont.render("Settings", 1, (255, 255, 255))
            CHANGESTUFF_LABEL = myfont.render("Press S for speed settings, press M for midi settings", 1, (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        speed_settings = True
                        settings = False
                    elif event.key == pygame.K_m:
                        midi_settings = True
                        settings = False

                    elif event.key == pygame.K_ESCAPE:
                        settings = False

                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAYSURF.blit(MAINGAME_LABEL, (int(resolution.current_w / 2) - 200, 20))
            DISPLAYSURF.blit(CHANGESTUFF_LABEL, (int(resolution.current_w / 2) - 500, 400))

        elif speed_settings:
            MAINGAME_LABEL = myfont.render("Press numbers 1-9 to set gamespeed", 1, (255, 255, 255))
            CHANGESTUFF_LABEL = myfont.render("Current: " + str(GLOBALS.SpeedOMeter), 1, (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        GLOBALS.SpeedOMeter = 1
                    elif event.key == pygame.K_2:
                        GLOBALS.SpeedOMeter = 2
                    elif event.key == pygame.K_3:
                        GLOBALS.SpeedOMeter = 3
                    elif event.key == pygame.K_4:
                        GLOBALS.SpeedOMeter = 4
                    elif event.key == pygame.K_5:
                        GLOBALS.SpeedOMeter = 5
                    elif event.key == pygame.K_6:
                        GLOBALS.SpeedOMeter = 6
                    if event.key == pygame.K_7:
                        GLOBALS.SpeedOMeter = 7
                    elif event.key == pygame.K_8:
                        GLOBALS.SpeedOMeter = 8
                    elif event.key == pygame.K_9:
                        GLOBALS.SpeedOMeter = 9
                    elif event.key == pygame.K_0:
                        GLOBALS.SpeedOMeter = 12
                    elif event.key == pygame.K_MINUS:
                        GLOBALS.SpeedOMeter = 16
                    elif event.key == pygame.K_EQUALS:
                        GLOBALS.SpeedOMeter = 21


                    elif event.key == pygame.K_ESCAPE:
                        speed_settings = False
                        settings = True

                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAYSURF.blit(MAINGAME_LABEL, (int(resolution.current_w / 2) - 200, 20))
            DISPLAYSURF.blit(CHANGESTUFF_LABEL, (int(resolution.current_w / 2) - 500, 400))

        elif midi_settings:
            musicinputname = ""
            MAINGAME_LABEL = myfont.render("Enter midi name. (no special chars)", 1, (255, 255, 255))
            CHANGESTUFF_LABEL = myfont.render("Current: " + str(musicinputname), 1, (255, 255, 255))



        #working fine
        elif homescreen:
            MAINGAME_LABEL = myfont.render("Press SPACE to start " + musicinputname, 1, (255, 255, 255))
            CHANGESTUFF_LABEL = myfont.render("Press G for options", 1, (255, 255, 255))
            DISPLAYSURF.blit(MAINGAME_LABEL, (int(resolution.current_w / 2) - 500, 20))
            DISPLAYSURF.blit(CHANGESTUFF_LABEL, (int(resolution.current_w / 2) - 200, 300))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        LOAD_GAME = True
                    elif event.key == pygame.K_g:
                        settings = True
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    pygame.display.update()

