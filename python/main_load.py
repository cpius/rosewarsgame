import sys
from controller import Controller
from common import *
import random
import pygame
import view
from viewcommon import *
from view import View


if __name__ == '__main__':

    view = View()

    controller = Controller.from_replay('./replay/a.json')

    controller.run_game()
