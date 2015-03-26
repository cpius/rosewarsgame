from view.viewcommon import pygame
from enum import Enum
from gamestate.gamestate_library import Unit, Type


class SoundSample(Enum):
    War_Elephant = 1
    Archer = 2
    War_Machine = 3
    Melee = 4
    Fanfare = 5
    Unit_Defeated = 6


soundpath = "./../sounds/"

soundfile = {
    SoundSample.War_Elephant: soundpath + "Elephant.wav",
    SoundSample.Archer: soundpath + "Archer.wav",
    SoundSample.Melee: soundpath + "Melee.wav",
    SoundSample.Fanfare: soundpath + "Fanfare.wav",
    SoundSample.Unit_Defeated: soundpath + "Unit_Defeated.wav"
}


class Sound:
    def __init__(self):
        pass

    def play_fanfare(self):
        sound = pygame.mixer.Sound(soundfile[SoundSample.Fanfare])
        sound.play()

    def play_action(self, action):
        sample = None
        if action.is_attack:
            if action.unit.unit == Unit.War_Elephant:
                sample = SoundSample.War_Elephant
            elif action.unit.unit == Unit.Archer:
                sample = SoundSample.Archer
            elif action.unit.range == 1:
                sample = SoundSample.Melee

        if sample:
            sound = pygame.mixer.Sound(soundfile[sample])
            sound.play()
