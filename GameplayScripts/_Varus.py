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
    "script": "JimAIO: Varus",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "varus"
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

########VARUS###############
varus_activate = True
varus_combo_key = 57
varus_harass_key = 46
varus_laneclear_key = 47
varus_q_combo = True
varus_w_combo = True
varus_e_combo = True
varus_r_combo = True
varus_q_harass = True
varus_e_harass = True
varus_q_mana = [65, 70, 75, 80, 85]
varus_e_mana = 80
varus_r_mana = 100
varus_max_q = 1600
varus_q_speed = 1900
charging_varq = False
############################

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


#########Varus##############
def varq_range(charge_time):
    if charge_time <= 0.0:
        return 895
    if charge_time >= 1.75:
        return 1480 # -15
    return 350 + 140.0*(charge_time - 0.25)*10
def charge_varq(q_spell):
    global charging_varq, charge_start_time_var
    q_spell.trigger(True)
    charging_varq = True
    charge_start_time_var = time.time()
def release_varq(q_spell):
    global charging_varq
    q_spell.trigger(False)
    charging_varq = False
def varus_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    global charge_start_time_var
    self = game.player
    player = game.player

    if varus_q_combo and IsReady(game, q_spell) and game.player.mana > varus_q_mana[game.player.Q.level-1]:
        
        target2 = GetBestTargetsInRange(game, 850)
        if ValidTarget(target2):
            if target2:
                #current_charge_time_var = time.time() - charge_start_time_var
                current_q_range_var = 895 #varq_range(current_charge_time_var) - 550
                current_q_travel_time_var = current_q_range_var / varus_q_speed
                predicted_pos = predict_pos(target2, current_q_travel_time_var)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_varq(q_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)

        if not target2:
            target = GetBestTargetsInRange(game, varus_max_q + 300)
            if ValidTarget(target):
                if game.player.pos.distance(target.pos) <= varus_max_q:
                    if ValidTarget(target):
                        if not charging_varq:
                            charge_varq(q_spell)
                        current_charge_time_var = time.time() - charge_start_time_var
                        current_q_range_var = varq_range(current_charge_time_var)
                        current_q_travel_time_var = current_q_range_var / varus_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time_var)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_varq(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if varus_e_combo and IsReady(game, e_spell) and game.player.mana > varus_e_mana and not getBuff(player, "VarusQ") and not getBuff(player, "VarusQLaunch"):
        target = GetBestTargetsInRange(game, 1100)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, e_spell, game.player, target)))
            time.sleep (0.01)
            e_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
def varus_harass(game):
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    global charge_start_time_var
    if varus_q_harass and IsReady(game, q_spell) and game.player.mana > varus_q_mana[game.player.Q.level-1]:
        
        target2 = GetBestTargetsInRange(game, 850)
        if ValidTarget(target2):
            if target2:
                #current_charge_time_var = time.time() - charge_start_time_var
                current_q_range_var = 895 #varq_range(current_charge_time_var) - 550
                current_q_travel_time_var = current_q_range_var / varus_q_speed
                predicted_pos = predict_pos(target2, current_q_travel_time_var)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_varq(q_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)

        if not target2:
            target = GetBestTargetsInRange(game, varus_max_q + 300)
            if ValidTarget(target):
                if game.player.pos.distance(target.pos) <= varus_max_q:
                    if ValidTarget(target):
                        if not charging_varq:
                            charge_varq(q_spell)
                        current_charge_time_var = time.time() - charge_start_time_var
                        current_q_range_var = varq_range(current_charge_time_var)
                        current_q_travel_time_var = current_q_range_var / varus_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time_var)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_varq(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if varus_e_harass and IsReady(game, e_spell) and game.player.mana > varus_e_mana and not getBuff(player, "VarusQ") and not getBuff(player, "VarusQLaunch"):
        target = GetBestTargetsInRange(game, 1100)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, e_spell, game.player, target)))
            time.sleep (0.01)
            e_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
############################

def winstealer_load_cfg(cfg):
    ###Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Varus###
    varus_activate = cfg.get_bool("varus_activate", False)
    varus_combo_key = cfg.get_int("varus_combo_key", 57)
    varus_harass_key = cfg.get_int("varus_harass_key", 46)
    varus_laneclear_key = cfg.get_int("varus_laneclear_key", 47)
    varus_q_combo = cfg.get_bool("varus_q_combo", True)
    varus_w_combo = cfg.get_bool("varus_w_combo", True)
    varus_e_combo = cfg.get_bool("varus_e_combo", True)
    varus_r_combo = cfg.get_bool("varus_r_combo", True)
    varus_q_harass = cfg.get_bool("varus_q_harass", True)
    varus_e_harass = cfg.get_bool("varus_e_harass", True)
    ######################################################

def winstealer_save_cfg(cfg):
    ##Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Varus###
    cfg.set_bool("varus_activate", varus_activate)
    cfg.set_int("varus_combo_key", varus_combo_key)
    cfg.set_int("varus_harass_key", varus_harass_key)
    cfg.set_int("varus_laneclear_key", varus_laneclear_key)
    cfg.set_bool("varus_q_combo", varus_q_combo)
    cfg.set_bool("varus_w_combo", varus_w_combo)
    cfg.set_bool("varus_e_combo", varus_e_combo)
    cfg.set_bool("varus_r_combo", varus_r_combo)
    cfg.set_bool("varus_q_harass", varus_q_harass)
    cfg.set_bool("varus_e_harass", varus_e_harass)
    ###################################################

def winstealer_draw_settings(game, ui):
    ##Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
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
    if ui.treenode("Combo Settings"):
        #ui.separator()
        varus_q_combo = ui.checkbox("Q Combo", varus_q_combo)
        varus_w_combo = ui.checkbox("W Combo if Tank", varus_w_combo)
        ui.tool_tip("Only long range to CHARGE DAMAGE | Tank => 1500+HP atleast")
        varus_e_combo = ui.checkbox("E Combo", varus_e_combo)
        ui.treepop()
    if ui.treenode("Harass Settings"):
        #ui.separator()
        varus_q_harass = ui.checkbox("Q Harass", varus_q_harass)
        varus_e_harass = ui.checkbox("E Harass", varus_e_harass)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        #ui.separator()
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        #ui.separator()
        varus_harass_key = ui.keyselect("Harass key", varus_harass_key)
        varus_laneclear_key = ui.keyselect("Laneclear Key", varus_laneclear_key)
        varus_combo_key = ui.keyselect("Combo Key", varus_combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)

def winstealer_update(game, ui):
    ###Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")

    if self.is_alive:
        if game.is_key_down(varus_combo_key):
            varus_combo(game)
        if game.is_key_down(varus_harass_key):
            varus_harass(game)
