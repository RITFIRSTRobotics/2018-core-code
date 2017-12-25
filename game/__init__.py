"""
Package initializer for the game constants
"""
from core.game import constants
from core.utils.HeaderParser import HeaderParser

hp = HeaderParser("core/game/game.h")

# Read in everything from game.h
constants.GOAL0_VALUE = hp.contents['GOAL0_SCORE']
constants.GOAL1_VALUE = hp.contents['GOAL1_SCORE']
constants.GOAL2_VALUE = hp.contents['GOAL2_SCORE']
constants.GOAL3_VALUE = hp.contents['GOAL3_SCORE']
