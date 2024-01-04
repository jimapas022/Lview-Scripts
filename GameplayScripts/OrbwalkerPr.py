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
import evade
from datetime import datetime



##

from commons.JJ_flags import EvadeFlags, Orbwalker


winstealer_script_info = {
    "script": "Pr Orbwalker",
    "author": "jim",
    "description": "",
}
DrawCircle = None


dead_zone = DrawCircle
target_selector = GetBestTargetsInRange(game, 700)
target_selector_monster = GetBestJungleInRange(game, 700)

max_atk_speed = 5.0
key_kite = 57, True
key_last_hit = 45, True
key_lane_clear = 47, True
move_interval = 0.10

delay_percent = 0.115

extra_delay = 00
atk_speed_override = None


self = game.player

class OrbwalkKite:
    type = Orbwalker.ModeKite

    def get_target(game, distance):
        target = GetBestTargetsInRange(game, 700)
        if target:
            return target

class OrbwalkLastHit:
    type = Orbwalker.ModeKite

    def last_hit_score(self, minion):
        ''' Returns a priority score for last hitting, first siege above all then the minion that is most attacked '''
        for minion in game.minions:
            if (
                not minion.is_alive
                or not minion.is_visible
                or not minion.isTargetable
                or minion.is_ally_to(game.player)
                ):
                continue
            if "siege" in minion.name:
                return 10000
            else:
                num_attackers = 0
                for m in game.minions:
                    if (
                        not m.is_alive
                        or not m.is_visible
                        or not m.isTargetable
                        or m.is_ally_to(game.player)
                        ):
                        continue
                    if m.id and m.id == minion.id:
                        num_attackers += 1
                return num_attackers
        
        #def get_target(game, distance):
        #    lasthits = 

            
#removed

def winstealer_load_cfg(cfg):
    pass

def winstealer_save_cfg(cfg):
    pass

def winstealer_draw_settings(game, ui):
    pass

def winstealer_update(game, ui):
    pass