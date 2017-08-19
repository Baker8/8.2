from mido import MidiFile
import GLOBALS

ontimer = 0
musicinputname = GLOBALS.MUSIC

currentmusicname = "midis/" + musicinputname + ".mid"

currentmusic = MidiFile("midis/" + musicinputname + ".mid")

scalar = []
channelevents = []
musicevents = []
musiclist = []

print("Parsing MIDI...")
for m in currentmusic:
   musiclist.append(m)

'''regular gen'''

for m in musiclist:
    musicevents.append(str(m) + "@")
    if m.type == "note_on" or m.type == "note_off":
        ontimer += m.time
        if m.type == 'note_on' and m.velocity > 0:  # only care about on notes
            offtimer = 0  # reset off timer
            currenton = m.note  # sets the note to be checked
            duration = .1
            for lookingforoff in musiclist:  # loops through whole thing again
                if lookingforoff.type == 'note_off' or (lookingforoff.type == "note_on" and lookingforoff.velocity == 0):
                    offtimer += lookingforoff.time
                    if lookingforoff.note == m.note and offtimer > ontimer and lookingforoff.channel == m.channel:
                        duration = offtimer - ontimer
                        break
                else:
                    offtimer += lookingforoff.time
            STO = (m.note, ontimer, duration, m.channel)
            scalar.append(m.note)
            channelevents.append(STO)
    else:
        ontimer += m.time

#'''



score_range = max(scalar) - min(scalar)
file = open("infomidi/"+str(musicinputname), "w+")
file.write("("+str(score_range) + "&)        " + str(min(scalar)) + "$ " + str(channelevents))
file.close()

musfile = open("infomidi/"+str(musicinputname)+"MUSICLINE", "w+")
for item in musicevents:
    musfile.write(item)
musfile.close()
