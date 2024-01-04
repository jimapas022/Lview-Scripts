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
    "script": "JimAIO: Jayce",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "jayce",
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

jayce_activate = True
jayce_combo_key = 57
jayce_harass_key = 46
jayce_laneclear_key = 47
jayce_q_melee_combo = True
jayce_w_melee_combo = True
jayce_e_melee_combo = True
jayce_q_ranged_combo = True
jayce_w_ranged_combo = True
jayce_e_ranged_combo = True
jayce_switch_form = True
jayce_q_ranged_harass = True
jayce_e_ranged_harass = True
#JaycePassiveMeleeAttack
#JaycePassiveRangedAttack



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


########Jayce###############
def jayce_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player

    ffff = GetBestTargetsInRange(game, 1600)
    if ffff and game.player.atkRange < 450 and IsReady(game, r_spell):
        r_spell.trigger(False)
        time.sleep(0.1)

    if self.is_alive and game.player.atkRange > 480:
        mana_q_jr = [55, 60, 65, 70, 75, 80]
        mana_w_jr = 40
        mana_e_jr = 50

        if jayce_q_ranged_combo and jayce_e_ranged_combo and IsReady(game, q_spell) and IsReady(game, e_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1] + mana_e_jr:
            target = GetBestTargetsInRange(game, 1600)
            if ValidTarget (target) and not IsCollisioned(game, target):
                q_travel_time = 1600 / 1450
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (old_cursor_pos)
                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
        if jayce_q_ranged_combo and IsReady(game, q_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, 1050)
            if ValidTarget (target) and not IsCollisioned(game, target):
                q_travel_time = 1050 / 1450
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (old_cursor_pos)
        if jayce_w_ranged_combo and IsReady(game, w_spell) and game.player.mana > mana_w_jr and not getBuff(player, "JayceHyperCharge"):
            target = GetBestTargetsInRange(game, 499)
            if target:
                w_spell.trigger(False)
        if game.player.atkRange > 300 and not IsReady(game, q_spell) and not getBuff(player, "JayceHyperCharge") and IsReady(game, r_spell):
            target = GetBestTargetsInRange(game, 500)
            if target:
                r_spell.trigger(False)
                time.sleep(0.1)

    if self.is_alive and game.player.atkRange < 450:
        mana_q_jm = 40
        mana_w_jm = 40
        mana_e_jm = 55
        if jayce_q_melee_combo and IsReady(game, q_spell) and game.player.mana > mana_q_jm:
            target = GetBestTargetsInRange(game, 600)
            if target:
                q_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        if jayce_w_melee_combo and IsReady(game, w_spell) and game.player.mana > mana_w_jm:
            target = GetBestTargetsInRange(game, 350)
            if target:
                w_spell.trigger(False)
                time.sleep(0.1)

        if jayce_e_melee_combo and IsReady(game, e_spell) and game.player.mana > mana_e_jm:
            target = GetBestTargetsInRange(game, 360)
            if target:
                e_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        target132 = GetBestTargetsInRange(game, 240)
        if game.player.atkRange < 450 and not IsReady(game, q_spell) and not IsReady(game, e_spell) and IsReady(game, r_spell) and not target132:
            r_spell.trigger(False)
            time.sleep(0.1)
def jayce_harass(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    mana_q_jr = [55, 60, 65, 70, 75, 80]
    mana_e_jr = 50
    if player.atkRange < 450 and IsReady(game, r_spell):
        r_spell.trigger(False)

    if jayce_q_ranged_harass and jayce_e_ranged_harass and IsReady(game, q_spell) and IsReady(game, e_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1] + mana_e_jr:
        target = GetBestTargetsInRange(game, 1600)
        if ValidTarget (target) and not IsCollisioned(game, target):
            q_travel_time = 1600 / 1450
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)
                e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

    if jayce_q_ranged_harass and IsReady(game, q_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, 1050)
        if ValidTarget (target) and not IsCollisioned(game, target):
            q_travel_time = 1050 / 1450
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)
############################


def winstealer_load_cfg(cfg):
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass

    jayce_activate = cfg.get_bool("jayce_activate", False)
    jayce_combo_key = cfg.get_int("jayce_combo_key", 57)
    jayce_harass_key = cfg.get_int("jayce_harass_key", 46)
    jayce_laneclear_key = cfg.get_int("jayce_laneclear_key", 47)
    jayce_q_melee_combo = cfg.get_bool("jayce_q_melee_combo", True)
    jayce_w_melee_combo = cfg.get_bool("jayce_w_melee_combo", True)
    jayce_e_melee_combo = cfg.get_bool("jayce_e_melee_combo", True)
    jayce_q_ranged_combo = cfg.get_bool("jayce_q_ranged_combo", True)
    jayce_w_ranged_combo = cfg.get_bool("jayce_w_ranged_combo", True)
    jayce_e_ranged_combo = cfg.get_bool("jayce_e_ranged_combo", True)

    jayce_q_ranged_harass = cfg.get_bool("jayce_q_ranged_harass", True)
    jayce_e_ranged_harass = cfg.get_bool("jayce_e_ranged_harass", True)

def winstealer_save_cfg(cfg):
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass

    cfg.set_bool("jayce_activate", jayce_activate)
    cfg.get_int("jayce_combo_key", jayce_combo_key)
    cfg.get_int("jayce_harass_key", jayce_harass_key)
    cfg.get_int("jayce_laneclear_key", jayce_laneclear_key)

    cfg.set_bool("jayce_q_melee_combo", jayce_q_melee_combo)
    cfg.set_bool("jayce_w_melee_combo", jayce_w_melee_combo)
    cfg.set_bool("jayce_e_melee_combo", jayce_e_melee_combo)

    cfg.set_bool("jayce_q_ranged_combo", jayce_q_ranged_combo)
    cfg.set_bool("jayce_w_ranged_combo", jayce_w_ranged_combo)
    cfg.set_bool("jayce_e_ranged_combo", jayce_e_ranged_combo)

    cfg.set_bool("jayce_q_range_harass", jayce_q_ranged_harass)
    cfg.set_bool("jayce_e_range_harass", jayce_e_ranged_harass)

def winstealer_draw_settings(game, ui):
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    global jayce_switch_form
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
    ui.text("| JimAIO : Jayce |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    if ui.treenode("Combo Settings"):   
        #jayce_switch_form = ui.checkbox("Auto Switch Forms", jayce_switch_form)
        ui.sameline()
        ui.tool_tip("Full Logic")
        if ui.treenode("Melee Form"): 
            jayce_q_melee_combo = ui.checkbox("Q Melee Combo", jayce_q_melee_combo)
            jayce_w_melee_combo = ui.checkbox("W Melee Combo", jayce_w_melee_combo)
            jayce_e_melee_combo = ui.checkbox("E Melee Combo", jayce_e_melee_combo)
            ui.treepop()
        if ui.treenode("Ranged Form"):  
            jayce_q_ranged_combo = ui.checkbox("Q Ranged Combo", jayce_q_ranged_combo)
            jayce_w_ranged_combo = ui.checkbox("W Ranged Combo", jayce_w_ranged_combo)
            jayce_e_ranged_combo = ui.checkbox("E Ranged Combo", jayce_e_ranged_combo)
            ui.treepop()
        ui.treepop()
    if ui.treenode("Harass Settings"):
        jayce_q_ranged_harass = ui.checkbox("Ranged Form Q Harass", jayce_q_ranged_harass)
        jayce_e_ranged_harass = ui.checkbox("Ranged Form E Harass", jayce_e_ranged_harass)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        jayce_harass_key = ui.keyselect("Harass key", jayce_harass_key)
        jayce_laneclear_key = ui.keyselect("Laneclear Key", jayce_laneclear_key)
        jayce_combo_key = ui.keyselect("Combo Key", jayce_combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)
    
def winstealer_update(game, ui):
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player

    if self.is_alive:# and game.player.name == "jayce":
        if game.is_key_down(jayce_combo_key):
            jayce_combo(game)
        if game.is_key_down(jayce_harass_key):
            jayce_harass(game)