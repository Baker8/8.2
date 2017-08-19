# imports and stuff
# THINGS TO DO IN ORDERS OF IMPORTANCE

# what gameplay to have?
# Running around, going for score. Stay low but don't touch the ground

# also checking to see what midis are already stored in there




import pygame, sys
from mido import MidiFile
from pygame.locals import *
import GLOBALS
import re
import mido


class Note(pygame.sprite.Sprite):
    def __init__(self, width, color, length, channel, time):
        pygame.sprite.Sprite.__init__(self)  # overlap correction?
        self.image = pygame.Surface([int(width * GLOBALS.SpeedOMeter), int(2*(resolution.current_h - 42) / score_range)])
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.length = length
        self.channel = channel
        self.height = int((resolution.current_h - 42) / score_range)
        self.time = 0
        self.image.set_alpha(180)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.color = color
        """Above is necessary, below, not so much"""
        self.image.fill(self.color)

        self.vspeed = 0
        self.hspeed = 0
        self.grounded = False
        self.crouched = False
        self.score = 0
        self.jumpfuel = GLOBALS.jumpfuel
        self.jumping = False
        self.superjump = False

    def jump(self):
        if self.grounded == True:
            if self.superjump == True:
                self.vspeed = -GLOBALS.jumpspeed * 2
                self.jumping = True
                self.superjump = False
            else:
                self.vspeed = -GLOBALS.jumpspeed
                self.jumping = True
        elif self.jumpfuel > 0 and self.jumping == True:
            self.jumpfuel -= 1
            self.vspeed -= GLOBALS.jumpspeed/16

    def right(self):
        if self.grounded and self.rect.x > 0:
            self.hspeed = GLOBALS.player_speed
            if self.crouched:
                self.hspeed -= GLOBALS.player_speed / GLOBALS.crouch_scaler
        elif self.rect.x <= 0:
            self.hspeed += GLOBALS.player_speed
        else:
            if self.hspeed < GLOBALS.player_speed:
                self.hspeed += (GLOBALS.player_speed) / GLOBALS.air_control

    def left(self):
        if self.grounded and self.rect.x > 0:
            self.hspeed = -(GLOBALS.player_speed + GLOBALS.SpeedOMeter)

        elif self.rect.x > 0:
            if self.hspeed > -(GLOBALS.player_speed + GLOBALS.SpeedOMeter):
                self.hspeed -= (GLOBALS.player_speed + GLOBALS.SpeedOMeter) / GLOBALS.air_control

    def crouch(self):
        if self.crouched == False:
            self.crouched = True
            self.rect.y += 1 + GLOBALS.notebuffer

    def uncrouch(self):
        if self.crouched == True:
            self.crouched = False


pygame.init()
resolution = pygame.display.Info()
pygame.display.set_caption('KlangfarbenMIDI')
DISPLAYSURF = pygame.display.set_mode((resolution.current_w, (resolution.current_h - 42)))
clock = pygame.time.Clock()
outport = mido.open_output("SimpleSynth virtual input")


def ROYALRESET():
    global winner
    winner = False

    # key inputs
    global w
    w = False
    global s
    s = False
    global a
    a = False
    global d
    d = False

    global i
    i = False
    global j
    j = False
    global k
    k = False
    global l
    l = False

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
    CLOCK = 50

    global note_list
    note_list = pygame.sprite.Group()

    global player_list
    player_list = pygame.sprite.Group()

    global misc_list
    misc_list = pygame.sprite.Group()

    global score_range  # scales the score based on min/max in particular midi
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

play_position = resolution.current_w * (2/3)#* (2/3)

latest = -play_position / GLOBALS.SpeedOMeter

while True:
    clock.tick(60)
    DISPLAYSURF.fill((0, 0, 0))

    if START_GAME:
        '''
        if clock.get_fps() < 58 and CLOCK >= 30:
            CLOCK -= 2
        elif CLOCK < 53:
            CLOCK += 1
        '''
        latest += 1 + GLOBALS.SpeedScaler
        if GLOBALS.SpeedOMeter < GLOBALS.MaxSpeed and latest > 60:
            GLOBALS.SpeedOMeter += GLOBALS.SpeedScaler
        #p1score_label = myfont.render(str(int(player1.score/5000)), 1, (255, 0, 0))
        p2score_label = myfont.render(str(int(player2.score/5000)), 1, (0, 0, 255))
        p1score_label = myfont.render(str(int(clock.get_fps())), 1, (255, 0, 0))

        exclusionlist = [9]
        for note in pre_note_list[0:2]:
            if note[1] * 60 < latest + (resolution.current_w - play_position) / GLOBALS.SpeedOMeter:
                # WIDTH          COLOR     LENGTH                                  channel   time
                if note[3] not in exclusionlist:
                    if int(note[2] * CLOCK * GLOBALS.SpeedOMeter) > 2000:
                        newnote = Note(2000/GLOBALS.SpeedOMeter, note[4], (note[2] * GLOBALS.SpeedOMeter * CLOCK), note[3], note[0])
                    else:
                        newnote = Note(note[2] * CLOCK, note[4], (note[2] * GLOBALS.SpeedOMeter * CLOCK), note[3], note[0])
                    newnote.rect.y = window_height - int((note[0] - int(minscalar) + 1) * (window_height / (score_range + 1)))
                    newnote.rect.x = resolution.current_w
                    note_list.add(newnote)
                    misc_list.add(newnote)
                pre_note_list.remove(note)


        for noteything in note_list:
            noteything.rect.x -= GLOBALS.SpeedOMeter
            if noteything.rect.x <= 0:
                noteything.rect.x -= 1
                if noteything.rect.x < -(noteything.length):
                    if noteything.color == (255, 0, 0):
                        player1.score += ((888888 / noteything.length) + 888) * GLOBALS.SpeedOMeter
                    elif noteything.color == (0, 0, 255):
                        player2.score += ((888888 / noteything.length) + 888) * GLOBALS.SpeedOMeter
                    note_list.remove(noteything)
                    misc_list.remove(noteything)
                    noteything.kill()

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
            for note in note_collisions:
                if player.rect.y + GLOBALS.player_height < note.rect.y + GLOBALS.notebuffer and player.vspeed > 0:
                    player.rect.y = note.rect.y - GLOBALS.player_height
                    if note.color == (255, 0, 0) and player.color == (0, 0, 255) or note.color == (0, 0, 255) and player.color == (255, 0, 0):
                        note.color = (222, 0, 222)
                        note.image.fill(note.color)
                    elif note.color != (222, 0, 222):
                        note.color = player.color
                        note.image.fill(note.color)
                    player.grounded = True
                    player.superjump = False
            if player.rect.y + GLOBALS.player_height >= window_height:
                player.grounded = True
                player.rect.y = window_height - GLOBALS.player_height
                if player.superjump == False:
                    player.score -= GLOBALS.ground_penalty
                    player.superjump = True
                player.score -= abs(player.rect.y) + 40
                player.hspeed = 0
            if player.rect.x >= resolution.current_w - GLOBALS.player_width:
                player.rect.x = (resolution.current_w - GLOBALS.player_width) - 1
            if player.grounded:
                player.jumpfuel = GLOBALS.jumpfuel
                player.jumping = False
                player.vspeed = 0
                if player.rect.x >= 0:
                    player.hspeed = -(GLOBALS.SpeedOMeter + 1)
            if player.rect.x <= 0:
                player.hspeed = 0
                if player.rect.x < -5:
                    player.rect.x = 0
            if player.grounded == False:
                player.vspeed += GLOBALS.fallspeed
            player.score += abs(player.rect.y)
            player.update()
        if d:
            player1.right()
        elif a:
            player1.left()
        if w:
            player1.jump()

        if l:
            player2.right()
        elif j:
            player2.left()
        if i:
            player2.jump()



        player1.rect.x += int(player1.hspeed)
        player1.rect.y += int(player1.vspeed)
        player2.rect.x += int(player2.hspeed)
        player2.rect.y += int(player2.vspeed)

        if latest < 120:
            player1.rect.y = -GLOBALS.player_height - 1
            player1.rect.x = 100
            player2.rect.y = -GLOBALS.player_height - 1
            player2.rect.x = 300
            player1.hspeed = 0
            player2.hspeed = 0
            player1.vspeed = 0
            player2.vspeed = 0



        misc_list.draw(DISPLAYSURF)
        DISPLAYSURF.blit(p1score_label, (20, window_height + 0))
        DISPLAYSURF.blit(p2score_label, (resolution.current_w - 200, window_height + 0))

        for event in pygame.event.get():

            # KILL ALL AND GO BACK TO MAIN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    d = True
                elif event.key == pygame.K_a:
                    a = True
                elif event.key == pygame.K_w:
                    w = True
                elif event.key == pygame.K_s:
                    player1.crouch()

                if event.key == pygame.K_l:
                    l = True
                elif event.key == pygame.K_j:
                    j = True
                elif event.key == pygame.K_i:
                    i = True
                elif event.key == pygame.K_k:
                    player2.crouch()

                elif event.key == pygame.K_ESCAPE:
                    for entry in misc_list:
                        entry.remove(misc_list)
                        entry.remove(note_list)
                        entry.remove(player_list)
                        entry.kill()
                    for entry in pre_note_list:
                        pre_note_list.remove(entry)
                    ROYALRESET()
                    outport.panic()
                    outport.close()
                    homescreen = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    d = False
                elif event.key == pygame.K_a:
                    a = False
                elif event.key == pygame.K_w:
                    w = False
                elif event.key == pygame.K_s:
                    s = False
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

            # important
            elif event.type == QUIT:
                outport.panic()
                outport.close()
                pygame.quit()
                sys.exit()
        if len(misc_list) <= 4 and latest > 50 and winner == False:
            print("OVER")
            winner = True
            if player1.score > player2.score:
                print("RED WINS")
            elif player2.score > player1.score:
                print("BLUE WINS")

    else:

        # working fine but need to add the creaton of note played class objects
        if LOAD_GAME:
            readytostart = True
            LOAD_GAME = False
            filevents = []
            print("reading file...")
            file = open("infomidi/" + musicinputname, "r")
            filevents = file.read()
            file.close()
            rangefinder = filevents.find("&")
            score_range = filevents[1:int(rangefinder)]
            score_range = int(score_range)
            minfinder = filevents.find("$")
            minscalar = filevents[8:int(minfinder)]
            minscalar = minscalar.strip()
            filevents = filevents[int(minfinder) + 4:len(filevents) - 2]
            filevents = filevents.split("), (")
            print(str(filevents))
            if int(resolution.current_h/score_range) * 2 > GLOBALS.notebuffer:
                GLOBALS.notebuffer = int((resolution.current_h/score_range) * 2) + 8

            notefile = open("infomidi/" + musicinputname + "MUSICLINE", 'r')
            raw = []
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
                firetime += entry.time - GLOBALS.SOOPERSPEED
                entry.time = firetime
                notestobeplayed.append(entry)
            if firetime != 0:
                GLOBALS.SpeedScaler = (GLOBALS.MaxSpeed / (firetime * 60))

            for note_values in filevents:
                eachof4 = note_values.split(", ")
                STO4 = (int(eachof4[0]), float(eachof4[1]) - (GLOBALS.SOOPERSPEED/60), float(eachof4[2]) - (GLOBALS.SOOPERSPEED/60), int(eachof4[3]))
                print(STO4)
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
                elif STO4[3] == 9:  # ew drums gross
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


                # """


        # also working fine
        elif readytostart:  # after it loads but before you actually go
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
            if GLOBALS.singleplayer == False:
                player_list.add(player1)
            player2 = Player((0, 0, 255), GLOBALS.player_width, GLOBALS.player_height)
            player2.rect.y = 50
            player2.rect.x = 100 + GLOBALS.player_width
            player_list.add(player2)
            barz = Player((88, 88, 88), 2, window_height)
            barz.rect.y = 0
            barz.rect.x = play_position
            misc_list.add(barz)
            misc_list.add(player1)
            misc_list.add(player2)

        elif settings:

            """THIS THING IS GETTING SPAGHETTIFIED IN ORDER TO LOAD STUFF OUTSIDE THE ACTUAL GAME"""
            MAINGAME_LABEL = myfont.render("Settings", 1, (255, 255, 255))
            CHANGESTUFF_LABEL = myfont.render("Press S for speed settings, press M for midi settings", 1,
                                              (255, 255, 255))

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



        # working fine
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
