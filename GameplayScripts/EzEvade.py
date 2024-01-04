from turtle import delay
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
import json, time, math, random
import sys
from evade import checkEvade
from API.summoner import *
from commons.timer import Timer
import array
from copy import copy
import itertools, math
import commons.damage_calculator as damage_calculator
from commons.damage_calculator import DamageSpecification, DamageType
from win32api import GetSystemMetrics
import requests
import ctypes
import typing
import enum
from re import S, search
from typing import Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
SendInput = ctypes.windll.user32.SendInput
import keyboard

#sqrt = math.sqrt
#                                                                                                              
# ██████████████ ██████████████████   ██████████████ ██████  ██████ ██████████████ ████████████   ██████████████ 
# ██          ██ ██              ██   ██          ██ ██  ██  ██  ██ ██          ██ ██        ████ ██          ██ 
# ██  ██████████ ████████████    ██   ██  ██████████ ██  ██  ██  ██ ██  ██████  ██ ██  ████    ██ ██  ██████████ 
# ██  ██                 ████  ████   ██  ██         ██  ██  ██  ██ ██  ██  ██  ██ ██  ██  ██  ██ ██  ██         
# ██  ██████████       ████  ████     ██  ██████████ ██  ██  ██  ██ ██  ██████  ██ ██  ██  ██  ██ ██  ██████████ 
# ██          ██     ████  ████       ██          ██ ██  ██  ██  ██ ██          ██ ██  ██  ██  ██ ██          ██ 
# ██  ██████████   ████  ████         ██  ██████████ ██  ██  ██  ██ ██  ██████  ██ ██  ██  ██  ██ ██  ██████████ 
# ██  ██         ████  ████           ██  ██         ██    ██    ██ ██  ██  ██  ██ ██  ██  ██  ██ ██  ██         
# ██  ██████████ ██    ████████████   ██  ██████████ ████      ████ ██  ██  ██  ██ ██  ████    ██ ██  ██████████ 
# ██          ██ ██              ██   ██          ██   ████  ████   ██  ██  ██  ██ ██        ████ ██          ██ 
# ██████████████ ██████████████████   ██████████████     ██████     ██████  ██████ ████████████   ██████████████ 
#                                                                                                              
#                                                                                                 By Jimapas#8758

class DangerLevels:
    Easy = 1
    Fastes = 2
    UseSpell = 3
    VeryDangerous = 4

class Spell:
    def __init__(
        self, name, missile_names, flags, delay=0.0, danger=DangerLevels.Fastes
    ):
        global MissileToSpell, Spells

        self.flags = flags
        self.name = name
        self.missiles = missile_names
        self.delay = delay
        self.danger = danger
        Spells[name] = self
        for missile in missile_names:
            if len(missile) < 1:
                MissileToSpell[name] = self
            MissileToSpell[missile] = self

    delay = 0.0
    danger = DangerLevels.Fastes
    flags = 0
    name = "?"
    missiles = []
    skills = []



q_spell = getSkill(game, "Q")
w_spell = getSkill(game, "W")
e_spell = getSkill(game, "E")
r_spell = getSkill(game, "R")

ChampionSpells = {
    "aatrox": [
        Spell("AatroxQ", ["AatroxQ"], displayName = "The Darkin Blade [First]", slot = q_spell, type = "linear", speed = max, range = 650, delay = 0.6, radius = 130, danger = 3, cc = True, collision = False, windwall = False, hitbox = False, fow = False, exception = False, extend = True),
        Spell("AatroxQ2", ["AatroxQ2"], displayName = "The Darkin Blade [Second]", slot = q_spell, type = "polygon", speed = max, range = 500, delay = 0.6, radius = 200, danger = 3, cc = True, collision = False, windwall = False, hitbox = False, fow = False, exception = False, extend = True),
        Spell("AatroxQ3", ["AatroxQ3"], displayName = "The Darkin Blade [Third]", slot = q_spell, type = "circular", speed = max, range = 200, delay = 0.6, radius = 300, danger = 4, cc = True, collision = False, windwall = False, hitbox = False, fow = False, exception = False, extend = False),
        Spell("AatroxW", ["AatroxW"], displayName = "Infernal Chains", missileName = "AatroxW", slot = w_spell, type = "linear", speed = 1800, range = 825, delay = 0.25, radius = 80, danger = 2, cc = True, collision = True, windwall = True, hitbox = True, fow = True, exception = False, extend = True),
    ]}
