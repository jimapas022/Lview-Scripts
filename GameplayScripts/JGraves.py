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
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "JimAIO: Graves",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "graves"
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
JScolorCyan = Color.CYAN
JScolorCyan.a = 1
###########GRAVES###########
graves_activate = True
graves_combo_key = 57
graves_harass_key = 46
graves_laneclear_key = 47
graves_combo_q = True
graves_combo_w = True
graves_combo_e = True
graves_combo_r = True
graves_harass_q = True
graves_clear_q = True
graves_clear_e = True


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




########Graves##############
RLvLDamage = [250, 400, 550]

def ggHP(game, target):
    global unitRes, unitHP, EffJungleHP

    if get_onhit_physical(game.player, target) > (get_onhit_magical(game.player, target)):
        unitRes = target.armour
    else:
        unitRes = target.armour

    unitHP = target.health
    
    return (
        (((1+(unitRes / 100))*unitHP)))
def grav_r_dmg(game, target):
    global RLvLDamage
    phys = (get_onhit_physical(game.player, target) * 1.20)
    return (RLvLDamage[game.player.R.level - 1] + phys)

def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [250, 400, 550]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + ap)

    # Reduce damage based on target's magic resist
    mr = target.armour
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage


def graves_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    player = game.player
    self = game.player

    if graves_combo_r and IsReady(game, r_spell) and game.player.mana >= 100:
        target = GetBestTargetsInRange (game, 1300)
        if ValidTarget (target) and RDamage(game,target) >= target.health:
            r_travel_time = 1300 / 2100
            predicted_pos = predict_pos (target, r_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                r_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor(old_cursor_pos)

    if graves_combo_q and IsReady(game, q_spell) and game.player.mana >= 80:
        target = GetBestTargetsInRange(game, 800)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_combo_w and IsReady(game, w_spell) and game.player.mana >= 70:
        target = GetBestTargetsInRange(game, 950)
        if target:# and not getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, w_spell, game.player, target)))
            time.sleep (0.01)
            w_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_combo_e and IsReady(game, e_spell) and game.player.mana >= 40:
        target = GetBestTargetsInRange(game, 800)
        target2 = GetBestTargetsInRange(game, 950)
        if not target and target2:
            e_spell.trigger (False)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)
def graves_clear(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()

    if graves_clear_q and IsReady(game, q_spell) and game.player.mana >= 80:
        target = GetBestMinionsInRange(game, 800)
        target3 = GetBestJungleInRange(game, 800)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
        if target3 and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target3)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_clear_e and IsReady(game, e_spell) and game.player.mana >= 40:
        target = GetBestMinionsInRange(game, 800)
        target2 = GetBestJungleInRange(game, 800)
        if target2 and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)

def winstealer_load_cfg(cfg):
    ###Graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global graves_clear_q, graves_clear_e
    ###Graves###
    graves_activate = cfg.get_bool("graves_activate", False)
    graves_combo_key = cfg.get_int("graves_combo_key", 57)
    graves_harass_key = cfg.get_int("graves_harass_key", 46)
    graves_laneclear_key = cfg.get_int("graves_laneclear_key", 47)

    graves_combo_q = cfg.get_bool("graves_combo_q", True)
    graves_combo_w = cfg.get_bool("graves_combo_w", True)
    graves_combo_e = cfg.get_bool("graves_combo_e", True)
    graves_combo_r = cfg.get_bool("graves_combo_r", True)
    graves_harass_q = cfg.get_bool("graves_harass_q", True)
    graves_clear_q = cfg.get_bool("graves_clear_q", True)
    graves_clear_e = cfg.get_bool("graves_clear_e", True)

def winstealer_save_cfg(cfg):
    ###graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global graves_clear_q, graves_clear_e
    ###Graves###
    cfg.set_bool("graves_activate", graves_activate)
    cfg.get_int("graves_combo_key", 57)
    cfg.get_int("graves_harass_key", 46)
    cfg.get_int("graves_laneclear_key", 47)

    cfg.set_bool("graves_combo_q", graves_combo_q)
    cfg.set_bool("graves_combo_w", graves_combo_w)
    cfg.set_bool("graves_combo_e", graves_combo_e)
    cfg.set_bool("graves_combo_r", graves_combo_r)
    cfg.set_bool("graves_harass_q", graves_harass_q)

    cfg.set_bool("graves_clear_q", graves_clear_q)
    cfg.set_bool("graves_clear_e", graves_clear_e)

def winstealer_draw_settings(game, ui):
    ###graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global graves_clear_q, graves_clear_e
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
    ui.text("| JimAIO : Graves |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    if ui.treenode("Graves Combo"):
        graves_combo_q = ui.checkbox("Combo Q", graves_combo_q)
        ui.sameline()
        ui.tool_tip("When ammo : 1")
        graves_combo_w = ui.checkbox("Combo W", graves_combo_w)
        graves_combo_e = ui.checkbox("Combo E", graves_combo_e)
        ui.sameline()
        ui.tool_tip("Logic: Gain ammo")
        graves_combo_r = ui.checkbox("Combo R", graves_combo_r)
        ui.sameline()
        ui.tool_tip("ks")
        ui.treepop()
    if ui.treenode("Jungle/Wave Clear"):
        graves_clear_q = ui.checkbox("Clear Q", graves_clear_q)
        graves_clear_e = ui.checkbox("Clear E", graves_clear_e)
        ui.treepop()
    if ui.treenode("Script keybinds"):
        graves_laneclear_key = ui.keyselect("Graves Clear Key", graves_laneclear_key)
        graves_harass_key = ui.keyselect("Graves Harass Key", graves_harass_key)
        graves_combo_key = ui.keyselect("Graves Combo key", graves_combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.2", "", JScolorGray)

def winstealer_update(game, ui):
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global graves_clear_q, graves_clear_e
    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")

    if self.is_alive:
        if game.is_key_down(graves_combo_key):
            graves_combo(game)
        if game.is_key_down(graves_laneclear_key):
            graves_clear(game)
