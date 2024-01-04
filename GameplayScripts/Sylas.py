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

winstealer_script_info = {
    "script": "JimAIO: Sylas",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "sylas"
}

JScolorWhite = Color.WHITE
JScolorWhite.a = 1
JScolorGreen = Color.GREEN
JScolorGreen.a = 1
JScolorYellow = Color.YELLOW
JScolorYellow.a = 1
JScolorGray = Color.GRAY
JScolorGray.a = 1
JScolorRed = Color.RED
JScolorRed.a = 1
JScolorPurple = Color.PURPLE
JScolorPurple.a = 1
JScolorOrange = Color.ORANGE
JScolorOrange.a = 1


sylas_activate = True
sylas_combo_key = 57
sylas_harass_key = 46
sylas_laneclear_key = 47
sylas_q_combo = True
sylas_w_combo_always = True
sylas_E1_combo = True
sylas_E2_combo = True
sylas_r_steal_only = True
sylas_r_steal_and_use = True
in_game_Rs = []
sylas_q_harass = True
sylas_q_laneclear = True
sylas_w_laneclear = True
sylas_e_laneclear = True
sylas_w_cannon_lasthit = True
syl_w_mode = 0
syl_w_clear_mode = 0
syl_HP = 0
syl_Q = {"Range": 775, "Mana": 55}
syl_W = {"Range": 400,} 
syl_W_mana = [60, 70, 80, 90, 100]
syl_E1 = {"Range": 400, "Mana": 65}
syl_E2 = {"Range": 800}
syl_R_St = {"Range": 950, "Mana": 75}
syl_R_cast = {"Range", 2000}


# Get player stats from local server
#ssl._create_default_https_context = ssl._create_unverified_context #//sec
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #//sec
#def getPlayerStats():
#    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
#    stats = json.loads(response)
#    return stats

class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius
def predict_pos(target, duration):
    """Predicts the target's new position after a duration"""
    target_direction = target.pos.sub (target.prev_pos).normalize ()
    # In case the target wasn't moving
    if math.isnan (target_direction.x):
        target_direction.x = 0.0
    if math.isnan (target_direction.y):
        target_direction.y = 0.0
    if math.isnan (target_direction.z):
        target_direction.z = 0.0
    if target_direction.x == 0.0 and target_direction.z == 0.0:
        return target.pos
    # Target movement speed
    target_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_speed * duration
    return target.pos.add (target_direction.scale (distance_to_travel))
############################


#########Sylas##############
def sylas_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    

    if sylas_E1_combo and IsReady(game, e_spell) and game.player.mana >= syl_E1["Mana"] and not getBuff(self, "sylasemanager"):
        target = GetBestTargetsInRange(game, syl_E2["Range"] + 350)
        if target:
            e_spell.trigger(False)

    if sylas_E2_combo and IsReady(game, e_spell) and getBuff(self, "sylasemanager"):
        target = GetBestTargetsInRange (game, syl_E2['Range'])
        if ValidTarget (target) and not IsCollisioned(game, target):
            E2_travel_time = syl_E2['Range'] / 1600
            predicted_pos = predict_pos (target, E2_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)

    if sylas_q_combo and IsReady(game, q_spell) and game.player.mana >= syl_Q["Mana"]:
        target = GetBestTargetsInRange(game, 625)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
            


    if syl_w_mode == 1 and IsReady(game, w_spell) and game.player.mana >= syl_W_mana[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, syl_W["Range"])
        if target:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))


    percent = (syl_HP * 0.01)
    if syl_w_mode == 2:
        if player.is_alive and player.health < (percent * player.max_health):
            if IsReady(game, w_spell) and game.player.mana >= syl_W_mana[game.player.W.level-1]:
                target = GetBestTargetsInRange(game, syl_W["Range"])
                if target:
                    w_spell.move_and_trigger(game.world_to_screen(target.pos))
                    
def sylas_harass(game):
    q_spell = getSkill(game, "Q")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player

    if sylas_q_harass and IsReady(game, q_spell) and game.player.mana >= syl_Q["Mana"]:
        target = GetBestTargetsInRange(game, 625)#syl_Q["Range"])
        if target:
            #q_spell.move_and_trigger(game.world_to_screen(target.pos))
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
############################


def winstealer_load_cfg(cfg):
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP

    sylas_activate = cfg.get_bool("sylas_activate", False)
    sylas_combo_key = cfg.get_int("sylas_combo_key", 57)
    sylas_harass_key = cfg.get_int("sylas_harass_key", 46)
    sylas_laneclear_key = cfg.get_int("sylas_laneclear_key", 47)

    sylas_q_combo = cfg.get_bool("sylas_q_combo", False)
    sylas_w_combo_always = cfg.get_bool("sylas_w_combo_always", False)
    sylas_E1_combo = cfg.get_bool("sylas_E1_combo", False)
    sylas_E2_combo = cfg.get_bool("sylas_E2_combo", False)

    sylas_q_harass = cfg.get_bool("sylas_q_harass", False)
    sylas_q_laneclear = cfg.get_bool("sylas_q_laneclear", False)
    sylas_w_laneclear = cfg.get_bool("sylas_w_laneclear", False)
    sylas_e_laneclear = cfg.get_bool("sylas_e_laneclear", False)
    sylas_w_cannon_lasthit = cfg.get_bool("sylas_w_cannon_lasthit", False)

    sylas_r_steal_and_use = cfg.get_bool("sylas_r_steal_and_use", False)
    sylas_r_steal_only = cfg.get_bool("sylas_r_steal_only", False)
    syl_w_clear_mode = cfg.get_int("syl_w_clear_mode", syl_w_clear_mode)
    syl_w_mode = cfg.get_int("syl_w_mode", syl_w_mode)
    syl_HP = cfg.get_float("syl_HP", 0)

def winstealer_save_cfg(cfg):
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP
    ###Sylas###
    cfg.set_bool("sylas_activate", sylas_activate)
    cfg.set_int("sylas_combo_key", sylas_combo_key)
    cfg.set_int("sylas_harass_key", sylas_harass_key)
    cfg.set_int("sylas_laneclear_key", sylas_laneclear_key)
    
    cfg.set_bool("sylas_q_combo", sylas_q_combo)
    cfg.set_bool("sylas_w_combo_always", sylas_w_combo_always)
    cfg.set_bool("sylas_E1_combo", sylas_E1_combo)
    cfg.set_bool("sylas_E2_combo", sylas_E2_combo)

    cfg.set_bool("sylas_q_harass", sylas_q_harass)
    cfg.set_bool("sylas_q_laneclear", sylas_q_laneclear)
    cfg.set_bool("sylas_w_laneclear", sylas_w_laneclear)
    cfg.set_bool("sylas_e_laneclear", sylas_e_laneclear)
    cfg.set_bool("sylas_w_cannon_lasthit", sylas_w_cannon_lasthit)

    cfg.set_bool("sylas_r_steal_and_use", sylas_r_steal_and_use)
    cfg.set_bool("sylas_r_steal_only", sylas_r_steal_only)

    cfg.set_int("syl_w_mode", syl_w_mode)
    cfg.set_int("syl_w_clear_mode", syl_w_clear_mode)
    cfg.set_float("syl_HP", syl_HP)
    ###################################################

def winstealer_draw_settings(game, ui):
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP

    jayce_switch_form = True
    JScolorWhite = Color.WHITE
    JScolorWhite.a = 1
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    JScolorYellow = Color.YELLOW
    JScolorYellow.a = 1
    JScolorGray = Color.GRAY
    JScolorGray.a = 1
    JScolorRed = Color.RED
    JScolorRed.a = 1
    JScolorPurple = Color.PURPLE
    JScolorPurple.a = 1
    JScolorOrange = Color.ORANGE
    JScolorOrange.a = 1
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1

    ui.text("")
    ui.text("| JimAIO : Sylas |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯", JScolorPurple)

    if ui.treenode("Combo Settings"):
        #ui.separator()
        sylas_q_combo = ui.checkbox(" Q Combo", sylas_q_combo)
        #sylas_w_combo_always =ui.checkbox("W Combo", sylas_w_combo_always)
        syl_w_mode = ui.listbox("",["Off","W Always","W below % HP"], syl_w_mode)
        if syl_w_mode == 2:
            syl_HP = ui.sliderfloat(" ", syl_HP, 0, 100.0)
        sylas_E1_combo = ui.checkbox(" E1 Combo", sylas_E1_combo)
        sylas_E2_combo = ui.checkbox(" E2 Combo", sylas_E2_combo)
        ui.treepop()
    if ui.treenode("Harass Settings"):
        #ui.separator()
        sylas_q_harass = ui.checkbox(" Q Harass", sylas_q_harass)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        #ui.separator()
        #sylas_q_laneclear = ui.checkbox("Q Laneclear", sylas_q_laneclear)
        #syl_w_clear_mode = ui.listbox("",["W Laneclear","W Lasthit Cannon"], syl_w_clear_mode)
        #sylas_e_laneclear = ui.checkbox("E1,E2 Laneclear", sylas_e_laneclear)
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        #ui.separator()
        sylas_harass_key = ui.keyselect("Harass key", sylas_harass_key)
        sylas_laneclear_key = ui.keyselect("Laneclear Key", sylas_laneclear_key)
        sylas_combo_key = ui.keyselect("Combo Key", sylas_combo_key)
        ui.treepop()
    #ui.labeltextc("                                     Script Version: 1.0.4", "", JScolorGray)

def winstealer_update(game, ui):
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP

    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")

    if self.is_alive:# and game.player.name == "sylas":
        
        if game.is_key_down(sylas_combo_key):
            sylas_combo(game)
        if game.is_key_down(sylas_harass_key):
            sylas_harass(game)